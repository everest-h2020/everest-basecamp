# tcl script to program Alveo U55C with bitstream as first argument
# using Vivado HW manager

set target_name xcu280_u55c_0
set memory_part mt25qu01g-spi-x1_x2_x4

if { $argc != 1 } {
    puts "ERROR: Missing bitstream file as first agrument"
    exit -1
}
set bitstream_file [lindex $argv 0]

if { [file exists $bitstream_file] != 1 } {
    puts "ERROR: Invalid bitstream $bitstream_file"
    exit -1
}

open_hw_manager
connect_hw_server -allow_non_jtag
open_hw_target

#create_hw_cfgmem -hw_device [get_hw_devices $target_name] -mem_dev [lindex [get_cfgmem_parts {$memory_part}] 0]

set_property PROBES.FILE {} [get_hw_devices $target_name]
set_property FULL_PROBES.FILE {} [get_hw_devices $target_name]
set_property PROGRAM.FILE $bitstream_file [get_hw_devices $target_name]

puts ""
puts "Vivado: programming $target_name with $bitstream_file"
program_hw_devices [get_hw_devices $target_name]
puts "DONE"

refresh_hw_device [lindex [get_hw_devices $target_name] 0]

close_hw_target
disconnect_hw_server localhost:3121

exit 0
