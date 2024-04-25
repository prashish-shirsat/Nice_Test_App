import subprocess
import psutil

def run_command(command):
    try:
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = result.communicate()

        if result.returncode != 0:
            print("Error running command {}: {}".format(command, stderr.decode().strip()))
            return None

        return stdout.decode().strip()
    except Exception as e:
        print("Error running command {}: {}".format(command, e))
        return None

def get_top_cpu_processes():
    processes = list(psutil.process_iter(attrs=['pid', 'name', 'cpu_percent']))
    processes.sort(key=lambda x: x.info['cpu_percent'], reverse=True)
    top_processes = processes[:5]

    top_processes_info = []
    for process in top_processes:
        top_processes_info.append(f"PID: {process.info['pid']}, Name: {process.info['name']}, CPU Percent: {process.info['cpu_percent']}%")

    return top_processes_info

def get_total_cores():
    num_physical_processors = psutil.cpu_count(logical=False)  # Number of physical processors
    num_cores_per_processor = psutil.cpu_count(logical=True)  # Number of cores per processor

    total_cores = num_physical_processors * num_cores_per_processor
    return total_cores

def get_number_of_hard_disks():
    # Get all disk partitions
    partitions = psutil.disk_partitions()

    # Filter out partitions that are not physical hard disks
    hard_disks = [partition.device for partition in partitions if 'cdrom' not in partition.opts and partition.fstype != '']

    # Count the number of unique hard disks
    num_hard_disks = len(set(hard_disks))

    return num_hard_disks

def get_total_physical_memory():
    command = "systeminfo | findstr /C:\"Total Physical Memory\""
    output = run_command(command)
    return output.split(":")[1].strip() if output else None

def get_hostname():
    command = "hostname"
    output = run_command(command)
    return output if output else None

def get_system_info():
    commands = {
        "Hostname": get_hostname(),
        "Total Physical Memory": get_total_physical_memory(),
        "Total Number of Cores": get_total_cores(),
        "Total Number of Hard Disks": get_number_of_hard_disks()
    }

    for desc, cmd in commands.items():
        print(f"{desc}: {cmd}")
        print("\n")

    top_processes_info = get_top_cpu_processes()

    print("\nTop 5 processes in terms of CPU:")
    for info in top_processes_info:
        print(info)

if __name__ == "__main__":
    get_system_info()
