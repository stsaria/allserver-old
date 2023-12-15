import shutil, os
import subprocess

make_list = ["lang?dir", "config?dir", "README.md?file", "README.ja.md?file", "figure.drawio.png?file"]

def copy_src_file():
    os.mkdir("bin/src")
    for i in os.listdir(): #拡張子を指定して検索、コピー
        if i.endswith(".py"):
            shutil.copy(i, "bin/src/"+i)

def copy_need_file():
    for i in make_list: 
        if "?dir" in i:
            shutil.copytree(i.split("?")[0], "bin/"+i.split("?")[0])
        elif "?file" in i:
            shutil.copy(i.split("?")[0], "bin/"+i.split("?")[0])

def pyinstall():
    #--hidden-import=minecraft_server
    subprocess.call("pyinstaller allserver.py --onefile --distpath=bin --uac-admin")

def install():
    if os.path.isdir("bin"): shutil.rmtree("bin")
    pyinstall()
    copy_need_file()
    copy_src_file()
    shutil.make_archive('allserver-win-bin', 'zip', root_dir='./bin')