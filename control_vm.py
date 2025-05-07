import libvirt
import sys

# Connect to system-level libvirt
conn = libvirt.open('qemu:///system')
if conn is None:
    print("Failed to open connection to qemu:///system")
    exit(1)

if len(sys.argv) != 3:
    print("Usage: python3 control_vm.py [Function:(start/stop)] [VM name]")
    sys.exit(1)

vm_name = sys.argv[2] # VM name

try:
    domain = conn.lookupByName(vm_name)
except libvirt.libvirtError:
    print(f"VM '{vm_name}' not found")
    conn.close()
    exit(1)

# Start the VM if it’s shut off
if domain.isActive() == 0: # shutdown
    if sys.argv[1] == "start":
        print(f"Starting VM '{vm_name}'...")
        domain.create()
    else:
        print(f"VM '{vm_name}' is already shutdown")

# stop the VM
elif domain.isActive() == 1: # running
    if sys.argv[1] == "stop":
        print(f"Stoping VM '{vm_name}'")
        domain.shutdown()
    else:
        print(f"VM '{vm_name}' is already running")

else:
    print("something went wrong")

conn.close()
