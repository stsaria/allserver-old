import configparser, ctypes, socket, os

check_path_list = ["lang", "config", "data", "minecraft", "config/basic.ini", "config/minecraftserver.ini"]
make_list = ["data?dir", "minecraft?dir"]

def network(check_host = "www.google.com", check_port = 80):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((check_host,check_port))
        client.close()
        return 0
    except:
        return 1

def file_dir(path : list, make : list):
    for i in path:
        if not os.path.exists(i):
            if i+"?dir" in make:
                try:
                    os.mkdir(i)
                except:
                    return 2, i
            elif i+"?file" in make:
                try:
                    f = open(i, mode="w")
                    f.close()
                except:
                    return 2, i
            else:
                return 1, i
    return 0, ""

def ini():
    try:
        ini = configparser.ConfigParser()
        ini.read('config/basic.ini', 'UTF-8')
        _ = ini['lang']['spare_lang']
        _ = ini['lang']['lang']
        _ = ini['team']['team_list']
        
        ini = configparser.ConfigParser()
        ini.read('config/minecraftserver.ini', 'UTF-8')
        _ = ini['basic']['version']
        _ = ini['basic']['port']
    except:
        return 1
    return 0

def lang():
    ini = configparser.ConfigParser()
    ini.read('config/basic.ini', 'UTF-8')
    lang_file = ""
    if os.path.isfile(f"lang/{ini['lang']['lang']}.json"):
        lang_file = f"{ini['lang']['lang']}.json"
    elif os.path.isfile(f"lang/{ini['lang']['spare_lang']}.json"):
        lang_file = f"{ini['lang']['spare_lang']}.json"
    else:
        return 1
    return 0

def check():
    # allserver path check
    result, error_path = file_dir(check_path_list, make_list)
    if result == 1:
        print(f"Error : Not found pass({error_path})")
        return 2
    elif result == 2:
        print(f"Error : Fail make pass({error_path})")
        return 3
    # Network check
    result = network()
    if result != 0:
        print("Error : Not connected to network")
        return 4
    # Check ini file
    result = ini()
    if result != 0:
        print("Error : Fail load ini file")
        return 5
    # Check lang file
    result = lang()
    if result != 0:
        print("Error : Fail load lang file")
        return 6
    return 0

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False