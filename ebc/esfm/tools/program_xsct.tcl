# tcl script to program Alveo U55C with bitstream as first argument
# using Xilinx Software Command-Line Tool

set target_name xcu280_u55c
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

connect

if { [lindex [ta] 1] != $target_name } {
    puts "ERROR: Cannot find target $target_name"
    exit -1
}

targets 1

puts ""
puts "XSCT: programming $target_name with $bitstream_file"
fpga $bitstream_file
puts "DONE"

disconnect

exit 0
