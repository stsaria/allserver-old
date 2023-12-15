import shutil, os

make_list = ["lang?dir", "config?dir", "README.md?file", "README.ja.md?file", "figure.drawio.png?file"]

def copy_src_file():
    os.mkdir("dist/src")
    for i in os.listdir(): #拡張子を指定して検索、コピー
        if i.endswith(".py"):
            shutil.copy(i, "dist/src/"+i)

def copy_need_file():
    for i in make_list: 
        if "?dir" in i:
            shutil.copytree(i.split("?")[0], "dist/"+i.split("?")[0])
        elif "?file" in i:
            shutil.copy(i.split("?")[0], "dist/"+i.split("?")[0])

def pyinstall():
    os.system("wsl pyinstaller allserver.py --onefile")
    os.system("pyinstaller allserver.py --onefile")

def install():
    if os.path.isdir("dist"): shutil.rmtree("dist")
    pyinstall()
    copy_need_file()
    copy_src_file()