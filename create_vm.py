import libvirt

xml_file = "minimal_vm.xml"

with open(xml_file, 'r') as f:
    xml_config = f.read()

conn = libvirt.open('qemu:///system')
if conn is None:
    print("Failed to open connection to qemu:///system")
    exit(1)

try:
    domain = conn.defineXML(xml_config)
    print(f"VM '{domain.name()}' defined.")
    domain.create()
    print("VM started.")
except libvirt.libvirtError as e:
    print(f"Failed to define/start VM: {e}")

conn.close()
