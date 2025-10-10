import time
import vitis
from xsdb import *


s = start_debug_session()

print("Start the loading procedure")

# connecting to the target
print("Connecting to the Xilinx hw_server")
s.connect(url="TCP:127.0.0.1:3121")

# Disable Security gates to view PMU MB target
print("Switch to PSU")
s.targets("--set", filter="name =~ PSU")
# By default, JTAG security gates are enabled
# This disables security gates for DAP, PLTAP and PMU.
print("Disabling JTAGsecurity gates")
s.mwr(0xffca0038, words=0x1ff)
time.sleep(0.5)

# Load and run PMU FW
print("Downloading PMU firmware")
s.targets("--set", filter="name =~ MicroBlaze PMU")
s.dow('pmufw.elf')
s.con()
time.sleep(0.5)

# Reset A53
print("Reset A53 processor")
s.targets("--set", filter="name =~ Cortex-A53 #0")
s.targets()
s.rst(type='processor')

#load and run FSBL
print("Downloading FSBL")
s.dow('fsbl.elf')
s.con()
time.sleep(0.5)
s.stop()

#load and run the ARM trusted-firmware (TF-A/BL31)
print("Downloading the ARM Trusted-firmware (TF-A/BL31)")
s.dow('tfa.elf')
s.con()
time.sleep(0.5)
s.stop()

# load system devicetree
print("Downloading system device tree")
s.dow('system.dtb', '-d', addr=0x100000)
time.sleep(0.5)

print("Downloading the u-boot")
s.dow('uboot.elf')


print("\nIf you want to load the kernel/rootfs via tftp, prepare to interrupt the auto-boot count down!!")

time.sleep(1)
print("Starting u-boot")
s.con()

print("Script Ended.")

vitis.dispose()