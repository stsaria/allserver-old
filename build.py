import subprocess, platform, shutil, os

make_list = ["lang?dir", "config?dir", "README.md?file", "README.ja.md?file", "figure.drawio.png?file"]

def copy_need_file():
    for i in make_list: 
        if "?dir" in i:
            shutil.copytree(i.split("?")[0], "bin/"+i.split("?")[0])
        elif "?file" in i:
            shutil.copy(i.split("?")[0], "bin/"+i.split("?")[0])

def pyinstall():
    subprocess.run("pyinstaller allserver.py --onefile --distpath=bin --uac-admin", shell=True)

def install():
    user_use_platform = platform.system()
    if os.path.isdir("bin"): shutil.rmtree("bin")
    pyinstall()
    copy_need_file()
    if user_use_platform == "Windows":
        shutil.make_archive('allserver-win-bin', 'zip', root_dir='./bin')
    elif user_use_platform == "Linux":
        shutil.make_archive('allserver-linux-bin', 'gztar', root_dir='./bin')