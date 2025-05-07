import libvirt

conn = libvirt.open('qemu:///system')
if conn is None:
    print("Failed to open connection to qemu:///system")
    exit(1)

print("Connected to libvirt")

# List running VMs
domains = conn.listDomainsID()
print("Running VMs:")
for domain_id in domains:
    dom = conn.lookupByID(domain_id)
    print(f"- {dom.name()} (ID: {domain_id})")

# List defined (but not running) VMs
defined = conn.listDefinedDomains()
print("Defined but not running VMs:")
for name in defined:
    print(f"- {name}")

conn.close()
