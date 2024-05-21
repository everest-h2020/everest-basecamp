#!/bin/env bash
################################################################################
# Copyright (c) 2023-2024 Virtual Open Systems SAS - All rights reserved.
#
# This source code is free software; you can redistribute it and/or modify it
# under the terms and conditions of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# File Name   : qdma_manager.sh
# Author      : STEFANO CIRICI <s.cirici@virtualopensystems.com>
# Description : This file composes the QDMA manager functionalities allowing
#               unbinding of PCI devices from their driver, removing PCI devices
#               and their VF from the PCI bus, and rescanning the PCI bus for
#               new devices.
################################################################################

# Fail fast
set -E
#set -e  # check if command fail, disabled for using err_check
set -u
set -o pipefail

# Register trap function to interr()
trap interr SIGINT SIGQUIT

## FUNCTIONS ###################################################################

# usage()
#   Print usage of the script
function usage() {
cat <<EOF
Utility to remove FPGA PCI devices and rescan the PCI bus

Usage: $(basename $0) <command> [options]

Available commands:
  unbind                Unbind PCI device from its driver
  bind-vfio             Bind PCI device to $VFIO_DRV driver
  remove                Unbind and remove PCI devices and their VF
  rescan                Rescan PCI bus for new devices

Available options:
  -b, --base_dev        Specify the base device slot in the format
                          DDDD:BB:DD Domain:Bus:Device (omit .Function)
                          default is $BASE_DEV_DEFAULT
  -h, --help            Print this help and exit
  -q, --quiet           Do not print info messages
  -v, --verbose         Print script debug info
  -y, --yes             Automatic yes to remove prompt
EOF
}

# interr()
#   Trap function
function interr {
    trap - SIGINT SIGQUIT
    echo
    echo "Process interrupted"
    exit 2
}

# root_check()
#   Check if root, if not, exit with an error
function root_check {
    if [ "$(id -u)" != "0" ]; then
        echo "You must run \"$(basename $0)\" as root"
        exit 1
    fi
}

# msg(message string)
#   Print log and errors if not in quiet mode
#   $1 message string to print
function msg() {
    if [ $QUIET -eq 0 ] ; then
        echo -e "${1-}"
    fi
}

# err_check(ERR code, ERR msg)
#   Check error code, eventually printing the message, and exit if error
#   $1 error code, 0 if no error
#   $2 optional message to print if error occurs (error != 0)
function err_check() {
    if [ $1 != 0 ]; then
        if [ -n "$2" ]; then
            echo "ERROR $1: $2"
        else
            echo "ERROR $1"
        fi
        exit $1
    fi
}

# get_dev_list()
#   Get list of devices with dev base id BASE_DEV
function get_dev_list() {
    find ${DEVICE_PATH}/${BASE_DEV}* 2> /dev/null
}

# unbind(dev_id)
#   Unbind device from its driver
#   $1 device ID
function unbind() {
    if [ $# -ne 1 ] ; then
        err_check 2 "Invalid parameters ${FUNCNAME[0]}()"
    fi
    local dev_id=$1

    # Check if device is bound to driver, if not return
    DEV_DRV=$(basename "$(readlink ${DEVICE_PATH}/${dev_id}/driver)")
    if [ -z "$DEV_DRV" ] ; then
        msg "DEV $dev_id not bound to any drv"
        return
    fi

    msg "Unbinding $dev_id from $DEV_DRV driver"
    echo "${dev_id}" | sudo tee ${DEVICE_PATH}/${dev_id}/driver/unbind > /dev/null 2>&1
    err_check $? "Failed unbinding $dev_id"
}

# remove(dev_id)
#   remove device from PCI bus
#   $1 device ID
function remove() {
    if [ $# -ne 1 ] ; then
        err_check 2 "Invalid parameters ${FUNCNAME[0]}()"
    fi
    local dev=$1

    msg "Removing device $dev"
    echo 1 | sudo tee ${dev}/remove > /dev/null 2>&1
    err_check $? "Failed removing dev $(basename $dev) from PCI bus"
}

# unbind_only()
#   Check device existance and call unbind(BASE_DEV)
function unbind_only() {
    # Get the list of currently connected devices
    DEV_LIST=$(get_dev_list)
    if [ -z "$DEV_LIST" ] ; then
        msg "WARNING: No device with base id \"${BASE_DEV}\" found!"
        exit 0
    fi

    unbind $BASE_DEV
}

# bind_vfio()
#   Bind device to $VFIO_DRV
function bind_vfio() {
    DEV_LIST=$(get_dev_list)
    if [ -z "$DEV_LIST" ] ; then
        msg "WARNING: No device with base id \"${BASE_DEV}\" found!"
        exit 0
    fi

    # Check if device is already bound or bound to different driver
    DEV_DRV=$(basename "$(readlink ${DEVICE_PATH}/${BASE_DEV}/driver)")
    if [ "$DEV_DRV" == "$VFIO_DRV" ] ; then
        msg "DEV $BASE_DEV already bound to $VFIO_DRV"
        return
    elif [ -n "$DEV_DRV" ] ; then
        msg "DEV $BASE_DEV bound to $DEV_DRV, unbinding"
        unbind $BASE_DEV
    fi

    msg "Binding $BASE_DEV to $VFIO_DRV driver"

    local vfio_id="10ee a03f"
    echo ${vfio_id} | sudo tee ${DRIVER_PATH}/${VFIO_DRV}/new_id > /dev/null 2>&1
    echo ${BASE_DEV} | sudo tee ${DRIVER_PATH}/${VFIO_DRV}/bind > /dev/null 2>&1
    #err_check $? "Failed binding $BASE_DEV to $VFIO_DRV"
    echo ${vfio_id} | sudo tee ${DRIVER_PATH}/${VFIO_DRV}/remove_id > /dev/null 2>&1
}

# unbind_remove()
#   Unbind and remove BASE_DEV device and all their VF devices
function unbind_remove() {
    # Get the list of currently connected devices
    DEV_LIST=$(get_dev_list)
    if [ -z "$DEV_LIST" ] ; then
        msg "WARNING: No device with base id \"${BASE_DEV}\" found!"
        exit 0
    fi

    # Get number of devices connected
    DEV_NUM=$(echo "$DEV_LIST" | wc -l)

    if [ $ASSUME_YES -eq 0 ] ; then
        echo "Found $DEV_NUM devices"
        # Ask to remove
        while true; do
            read -p "Are you sure you want to remove them? [y/N] " yn
            case $yn in
                [Yy]* ) break;;
                * )     echo "Exiting"; exit 0;;
            esac
        done
    fi

    # For each PF device
    for dev in $DEV_LIST
    do
        # Compute dev name from path
        DEV_NAME=$(basename $dev)

        NUM_VF=$(cat ${DEVICE_PATH}/${DEV_NAME}/sriov_numvfs 2> /dev/null)
        if [ -n "$NUM_VF" ] && [ $NUM_VF -gt 0 ] ; then
            msg "Device $DEV_NAME has $NUM_VF VF, removing them"

            # Get PCI device id of VF devices
            VF_DEV_ID=$(cat ${DEVICE_PATH}/${DEV_NAME}/sriov_vf_device)

            # get list of devices with this VF id
            VF_DEV_LIST=$(lspci -D -d :$VF_DEV_ID: | awk '{print $1}')

            # For each VF, unbind
            for vf_dev_name in $VF_DEV_LIST
            do
                unbind $vf_dev_name
            done

            # Remove VF for current PF
            msg "Removing $NUM_VF VF from $DEV_NAME"
            echo 0 | sudo tee ${DEVICE_PATH}/${DEV_NAME}/sriov_numvfs > \
                        /dev/null 2>&1
            err_check $? "Failed setting to 0 sriov_numvfs of dev $DEV_NAME"
        fi

        # Unbind PF from its driver
        unbind $DEV_NAME
    done

    # Re-compute dev list to exclude removed VF
    DEV_LIST=$(get_dev_list)
    for dev in $DEV_LIST
    do
        # Remove PF from PCI bus
        remove $dev
    done
}

# rescan()
#   Re-scan PCI bus and check devices
function rescan() {
    msg "Rescanning for PCI devices"
    echo 1 | sudo tee /sys/bus/pci/rescan > /dev/null 2>&1
    err_check $? "Failed rescanning PCI devices!"

    NEW_DEV_LIST=$(get_dev_list)

    if [ -z "$NEW_DEV_LIST" ]; then
        msg "No ${BASE_DEV}* devices found!"
    else
        NEW_DEV_NUM=$(echo "$NEW_DEV_LIST" | wc -l)
        msg "Found $NEW_DEV_NUM devices"
        msg "$NEW_DEV_LIST"
    fi
}

################################################################################

declare -r DRIVERS_LIST=("qdma-pf" "qdma-vf" "vfio-pci" "xclmgmt")
declare -r DRIVER_PATH="/sys/bus/pci/drivers"
declare -r DEVICE_PATH="/sys/bus/pci/devices"
declare -r VFIO_DRV="vfio-pci"
BASE_DEV_DEFAULT="0000:e1:00"

# Default parameters
BASE_DEV=$BASE_DEV_DEFAULT
REMOVE=0
RESCAN=0
UNBIND=0
BINDVFIO=0
QUIET=0
ASSUME_YES=0

# Parse input parameters
while [[ $# -gt 0 ]]
do
    case ${1-} in
        -h | --help)        usage && exit 0 ;;
        -v | --verbose)     set -x ;;
        -q | --quiet)       QUIET=1 ;;
        -y | --yes)         ASSUME_YES=1 ;;
        -b | --base_dev)    BASE_DEV=${2-}; shift;;
        unbind)             UNBIND=1 ;;
        bind-vfio)          BINDVFIO=1;;
        remove)             REMOVE=1 ;;
        rescan)             RESCAN=1 ;;
        *)
            echo "Unknown option: ${1}"
            usage
            exit 1
        ;;
    esac
    shift
done

# Check if only one between unbind, bind-vfio, remove and rescan is selected
if [ $UNBIND -eq 1 ] &&
    [ $BINDVFIO -eq 0 ] &&
    [ $REMOVE -eq 0 ] &&
    [ $RESCAN -eq 0 ]
then
    unbind_only
elif [ $UNBIND -eq 0 ] &&
    [ $BINDVFIO -eq 1 ] &&
    [ $REMOVE -eq 0 ] &&
    [ $RESCAN -eq 0 ]
then
    bind_vfio
elif [ $UNBIND -eq 0 ] &&
    [ $BINDVFIO -eq 0 ] &&
    [ $REMOVE -eq 1 ] &&
    [ $RESCAN -eq 0 ]
then
    unbind_remove
elif [ $UNBIND -eq 0 ] &&
    [ $BINDVFIO -eq 0 ] &&
    [ $REMOVE -eq 0 ] &&
    [ $RESCAN -eq 1 ]
then
    rescan
else
    echo "Error: Select only one option!"
    usage
    exit 1
fi

exit 0
