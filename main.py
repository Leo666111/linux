import virtualbox
import time

def create_vm(vm_name, os_type, ram_size_mb, vcpu_count, iso_path, vdi_path):
    vbox = virtualbox.VirtualBox()
    session = virtualbox.Session()

    # Create VM object
    vm = vbox.create_machine(settings_file='', name=vm_name, os_type_id=os_type,
                             groups=[], flags="")

    # Set RAM and VCPU
    vm.memory_size = ram_size_mb  # MB
    vm.cpu_count = vcpu_count

    # Set VirtualBox machine settings
    vm.storage_controller_names = ['SATA']
    storage_controller = vm.add_storage_controller(name="SATA", controller_type="IntelAHCI")
    
    # Add ISO as optical drive (for installation)
    iso_device = vm.add_medium(iso_path, type="dvd", access_mode="read-only")
    vm.attach_device("SATA", 0, 0, "dvd", iso_device)

    # Create VDI disk
    vdi = vbox.create_hard_disk("vdi", vdi_path)
    vm.attach_device("SATA", 0, 1, "hdd", vdi)

    # Register VM
    vbox.register_machine(vm)

    # Start the VM
    vm.launch_vm_process(session, "gui", [])
    print(f"VM {vm_name} is starting...")

    # Wait for VM to finish installation (could be automated with cloud-init)
    time.sleep(60)
    print(f"VM {vm_name} created and started successfully.")

if __name__ == "__main__":
    # VM configuration
    vm_name = "MyLinuxVM"
    os_type = "Ubuntu_64"  # You can replace this with the appropriate OS type
    ram_size_mb = 2048  # 2 GB RAM
    vcpu_count = 2
    iso_path = "/path/to/linux_iso.iso"  # Path to the installation ISO
    vdi_path = "/path/to/vdi_file.vdi"  # Path to the VDI disk file

    # Create and start the VM
    create_vm(vm_name, os_type, ram_size_mb, vcpu_count, iso_path, vdi_path)
