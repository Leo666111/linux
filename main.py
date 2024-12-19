import subprocess
import os
import time

# Function to create VM
def create_vm(vm_name, iso_path, vdi_path, ram_size_mb=2048, vcpu_count=2):
    # Ensure VirtualBox's VBoxManage is in the PATH
    vboxmanage = "VBoxManage"  # Use full path if needed

    # Step 1: Create the Virtual Machine
    subprocess.run([vboxmanage, "createvm", "--name", vm_name, "--ostype", "Ubuntu_64", "--register"], check=True)
    
    # Step 2: Set memory and CPU
    subprocess.run([vboxmanage, "modifyvm", vm_name, "--memory", str(ram_size_mb), "--cpus", str(vcpu_count)], check=True)

    # Step 3: Create a Virtual Disk (VDI)
    subprocess.run([vboxmanage, "createhd", "--filename", vdi_path, "--size", "10240"], check=True)  # 10 GB size
    
    # Step 4: Attach the Virtual Disk
    subprocess.run([vboxmanage, "storagectl", vm_name, "--name", "SATA", "--add", "sata", "--controller", "IntelAHCI"], check=True)
    subprocess.run([vboxmanage, "storageattach", vm_name, "--storagectl", "SATA", "--port", "0", "--device", "0", "--type", "hdd", "--medium", vdi_path], check=True)
    
    # Step 5: Attach ISO (for OS installation)
    subprocess.run([vboxmanage, "storageattach", vm_name, "--storagectl", "SATA", "--port", "1", "--device", "0", "--type", "dvddrive", "--medium", iso_path], check=True)
    
    # Step 6: Start the Virtual Machine
    subprocess.run([vboxmanage, "startvm", vm_name, "--type", "headless"], check=True)
    print(f"VM {vm_name} created and started successfully!")

# Usage
if __name__ == "__main__":
    vm_name = "MyUbuntuVM"
    iso_path = "/path/to/ubuntu.iso"  # Path to your ISO file (Linux distro)
    vdi_path = "/path/to/vdi/MyUbuntuVM.vdi"  # Path for the virtual hard disk

    create_vm(vm_name, iso_path, vdi_path)
