import subprocess
import time

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
##########################################################################################
def get_system_info():
    commands = {
        "Hostname": "hostname -f",
        "Total Physical Memory": "free -h | grep 'Mem:' | awk '{print $2}'",
        "Total Number of Cores": "nproc",
        "Total Number of Hard Disks": "lsblk -d -o NAME,TYPE | grep 'disk' | wc -l"
##        "Top 5 processes in terms of CPU": "ps -eo pid,%cpu,comm --sort=-%cpu | head -n 6"
    }

    for desc, cmd in commands.items():
        output = run_command(cmd)
        if output:
            print("{}: {}".format(desc, output))
            print("\n")
            time.sleep(2)
   
    print("Top 5 processes in terms of CPU:")
    print(run_command("ps -eo pid,%cpu,comm --sort=-%cpu | head -n 6"))


if __name__ == "__main__":
    get_system_info()

