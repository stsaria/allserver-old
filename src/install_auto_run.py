import subprocess, platform, shutil, check, etc, sys, os

lang = etc.load_lang()

def register_auto_run(start_program : str, argv : str):
    start_command = ""
    user_use_platform = platform.system()
    absolute_path = os.getcwd().replace("\\", "/")
    if ".py" in start_program:
        if shutil.which("python3"):
            start_command = f"python3 -u {start_program} "+argv
        else:
            start_command = f"python -u {start_program} "+argv
    else:
        start_command = absolute_path+"/"+os.path.basename(start_program.replace("./", ""))+" "+argv
    argv = argv.replace("--start-", "")
    if user_use_platform == "Linux":
        if not shutil.which("systemctl"):
            print(lang["Message"]["InstallAutoRun"]["Message"][1])
            print(lang["Message"]["InstallAutoRun"]["Message"][3])
            return 1
        try:
            with open("/etc/systemd/system/allserver-"+argv+".service", encoding="utf-8", mode="w") as f:
                f.write(f"""[Unit]
Description=AllServer Systemd
After=network.target
[Service]
WorkingDirectory={absolute_path}
Restart=always
ExecStart={start_command}
[Install]
WantedBy=multi-user.target""")
            subprocess.run("systemctl daemon-reload && systemctl enable allserver-"+argv+".service && systemctl start allserver-"+argv+".service", shell=True)
            print(f"Systemd name -> allserver-"+argv+".service")
        except:
            print(lang["Message"]["InstallAutoRun"]["Message"][3])
            return 2
    elif user_use_platform == "Windows":
        try:
            file = open(f"C:/ProgramData/Microsoft/Windows/Start Menu/Programs/StartUp/allserver-"+argv+".bat", mode='w')
            file.write(f"""cd {absolute_path}
{start_command}
pause""")
        except:
            print(lang["Message"]["InstallAutoRun"]["Message"][3])
            return 2
        file.close()
    print(lang["Message"]["InstallAutoRun"]["Message"][2])
    return 0

def install():
    if not check.is_admin():
        print(lang["Message"]["InstallAutoRun"]["Message"][0])
        return 1
    print("\n".join(lang["Message"]["InstallAutoRun"]["AutoRunSystemSelectMessage"]))
    while True:
        choice = input("[1,2,3] :")
        if choice == "1":
            register_auto_run(sys.argv[0], "--start-minecraft-server")
        elif choice == "2":
            register_auto_run(sys.argv[0], "--start-list-server")
        elif choice == "3":
            break
        else:
            continue
        print("\n".join(lang["Message"]["InstallAutoRun"]["AutoRunSystemSelectMessage"]))
    return 0