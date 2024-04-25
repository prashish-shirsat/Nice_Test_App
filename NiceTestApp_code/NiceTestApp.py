import platform
import subprocess
import sys
import os

def main():
    os_type = platform.system()
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get current directory

    # Check if valid arguments are provided
    valid_args = ["-logInfo", "-help"]
    passed_args = set(sys.argv[1:])  # Remove script name from args and convert to set for efficient lookup

    if not passed_args or passed_args == {"-logInfo"} or passed_args == {"-help"}:
        log_info_arg = "-logInfo" in passed_args
        help_arg = "-help" in passed_args

        if help_arg:
            print("This application 'NiceTestApp' will help you to get the current system information. \nYou can use 'NiceTestApp -logInfo' to get the information in NiceTestApp.log file")

        else:
            if os_type == "Windows":
                windows_code_path = os.path.join(current_dir, "windows_code.py")
                cmd = ["python", windows_code_path]
                if log_info_arg:
                    cmd.append("-logInfo")
                run_command(cmd, log_info_arg)

            elif os_type == "Linux":
                linux_code_path = os.path.join(current_dir, "linux_code.py")
                cmd = ["python", linux_code_path]
                if log_info_arg:
                    cmd.append("-logInfo")
                run_command(cmd, log_info_arg)

            else:
                print('Unsupported OS')

    else:
        unsupported_args = passed_args - set(valid_args)
        print(f"Unsupported argument(s) passed: {', '.join(unsupported_args)}")
        print("Use 'NiceTestApp -help' for more information.")

def run_command(cmd, log_info_arg):
    # If "-logInfo" argument is provided, redirect the output to "NiceTestApp.log"
    # Otherwise, print the output to terminal
    if log_info_arg:
        with open("NiceTestApp.log", "w") as log_file:
            process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            log_file.write(process.stdout.decode())
            print(process.stdout.decode())  # Manually print to terminal
    else:
        subprocess.run(cmd, stdout=sys.stdout, stderr=subprocess.STDOUT)

if __name__ == "__main__":
    main()
