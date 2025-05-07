import libvirt

vm_name = "dynamic-vm"
memory_mib = 512
vcpus = 1
disk_path = "/home/anas/dynamic-vm-disk.qcow2"
disk_size = "5G"

# Create disk if not exists
import os
if not os.path.exists(disk_path):
    os.system(f"qemu-img create -f qcow2 {disk_path} {disk_size}")

# Generate XML string
xml = f"""
<domain type='kvm'>
  <name>{vm_name}</name>
  <memory unit='MiB'>{memory_mib}</memory>
  <vcpu>{vcpus}</vcpu>
  <os>
    <type arch='x86_64'>hvm</type>
  </os>
  <devices>
    <emulator></emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='{disk_path}'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <interface type='network'>
      <source network='default'/>
      <model type='virtio'/>
    </interface>
    <graphics type='vnc' port='-1'/>
    <console type='pty'/>
  </devices>
</domain>
"""

# Connect and define VM
conn = libvirt.open('qemu:///system')
if conn is None:
    print("Failed to connect to hypervisor")
    exit(1)

try:
    domain = conn.defineXML(xml)
    print(f"VM '{domain.name()}' defined.")
    domain.create()
    print("VM started.")
except libvirt.libvirtError as e:
    print(f"Error: {e}")

conn.close()
