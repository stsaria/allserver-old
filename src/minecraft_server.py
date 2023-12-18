import configparser, subprocess, traceback, requests, datetime, logging, shutil, socket, json, etc, os

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter("%(asctime)s@ %(message)s"))
os.makedirs('./log', exist_ok=True)

file_handler = logging.FileHandler("./log/minecraftserver.log", encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s '%(funcName)s'")
)

logging.basicConfig(level=logging.NOTSET, handlers=[stream_handler, file_handler])
logger = logging.getLogger(__name__)

ini = configparser.ConfigParser()
ini.read('config/minecraftserver.ini', 'UTF-8')

def replace_func(fname, replace_set):
    target, replace = replace_set
    with open(fname, 'r', encoding='utf-8') as f1:
        tmp_list =[]
        for row in f1:
            if row.find(target) != -1:
                tmp_list.append(replace)
            else:
                tmp_list.append(row)
    with open(fname, 'w') as f2:
        for i in range(len(tmp_list)):
            f2.write(tmp_list[i])

def file_identification_rewriting(file_name, before, after):
    replace_setA = (before, after)
    replace_func(file_name, replace_setA)

def exec_java(dir_name, jar_name, xms : int, xmx : int, java_argument=""):
    try:
        result = subprocess.run(["java", f"-Xmx{str(xmx)}G", f"-Xms{str(xms)}G", "-jar", jar_name]+java_argument.split(" "), cwd=f"{dir_name}/", timeout=3600).returncode
        print(result)
    except subprocess.TimeoutExpired:
        return 0
    except:
        return 1
    return result

def download_file(url : str, save_name : str, user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"):
    try:
        if "http" in url == False:
            url = "http://"+url
        header = {
            'User-Agent': user_agent
        }
        response = requests.get(url, headers=header)
        if not str(response.status_code)[:1] in ["2","3"]:
            return False
        with open(save_name ,mode='wb') as f:
            f.write(response.content)
        return True
    except:
        return False

def get_minecraft_versions():
    if download_file("http://mcversions.net/mcversions.json", "minecraft/version.json") == False:
        return 1, [[]], [[]]
    try:
        file = open('minecraft/version.json', 'r')
        json_object = json.load(file)
        minecraft_editions = ["stable", "snapshot"]
        minecraft_versions = [[], []]
        for i in range(len(minecraft_editions)):
            for j in range(len(list(json_object[minecraft_editions[i]]))):
                if 'server' in json_object[minecraft_editions[i]][list(json_object[minecraft_editions[i]])[j]]:
                    minecraft_versions[i].append(list(json_object[minecraft_editions[i]])[j])
    except Exception as e:
        print(e)
        return 2, [[]], [[]]
    return 0, minecraft_versions[0], minecraft_versions[1]

def get_minecraft_url(version):
    if download_file("http://mcversions.net/mcversions.json", "minecraft/version.json") == False:
        return 1, "not"
    try:
        file = open('minecraft/version.json', 'r')
        json_object = json.load(file)
        minecraft_editions = ["stable", "snapshot"]
        successs = []
        for minecraft_edition in minecraft_editions:
            try:
                minecraft_server_url = json_object[minecraft_edition][version]["server"]
                successs.append(True)
            except KeyError:
                successs.append(False)
    except:
        return 2, "not"
    if not successs[0] and not successs[1]:
        return 2, "not"
    return 0, minecraft_server_url

def start_minecraft_server(ip : str, mcid : str, motd = "The minecraft server"):
    logger.info(f"IP:{ip} Start")
    dt_now        = datetime.datetime.now()
    dt_now_utc    = datetime.datetime.now(datetime.timezone.utc)
    try:
        os.makedirs(f"minecraft/{ip}", exist_ok=True)
        result, stable_versions, snapshot_versions = get_minecraft_versions()
        if result != 0:
            logger.error(f"IP:{ip} Error : Fail get minecraft versions")
            return 2
        if download_file("https://server.properties", f"minecraft/{ip}/server.properties") == False:
            logger.error(f"IP:{ip} Error : Fail server.properties download")
            return 3
        file_identification_rewriting(f"minecraft/{ip}/server.properties", "motd=", f"motd="+motd+"\n")
        with open(f"minecraft/{ip}/eula.txt", mode='a', encoding='utf-8') as f:
            f.write("#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n#"+dt_now_utc.strftime('%a')+" "+dt_now_utc.strftime('%b')+" "+dt_now_utc.strftime('%d')+" "+dt_now_utc.strftime('%H:%M:%S')+" "+str(dt_now_utc.tzinfo)+" "+dt_now_utc.strftime('%Y')+"\neula=true")
        if not ini['basic']['version'] in stable_versions:
            logger.error(f"IP:{ip} Error : Not found version in ini file")
            return 4
        result, url_minecraft_server = get_minecraft_url(ini['basic']['version'])
        if result != 0:
            logger.error(f"IP:{ip} Error : Fail get minecraft server url")
            return 5
        if download_file(url_minecraft_server, f"minecraft/{ip}/server.jar") == False:
            logger.error(f"IP:{ip} Error : Fail download minecraft server")
            return 3
        if download_file(f"https://api.mojang.com/users/profiles/minecraft/{mcid}", f"minecraft/{ip}/mcid.json") == False:
            logger.error(f"IP:{ip} Error : Fail download mojang api json")
            return 3
        with open(f"minecraft/{ip}/mcid.json", encoding="utf-8") as f:
            json_dict = json.load(f)
            if not 'id' in json_dict:
                logger.error(f"IP:{ip} Error : Unknow MCID")
                return 6
        with open(f"minecraft/{ip}/ops.txt", encoding="utf-8", mode="w") as f:
            f.write(f"{mcid}")
        result = exec_java(f"minecraft/{ip}", f"server.jar", 2, 2, java_argument=f"nogui --port {ini['basic']['port']}")
        if result != 0:
            logger.error(f"IP:{ip} Error : Error minecraft server")
            return 7
        logger.info("Minecraft server STOP!!")
        return 0
    except:
        error = traceback.format_exc()
        logger.error(f"IP:{ip} Error : Unknow\n\n{error}")
        return 1

def socket_server(host = "0.0.0.0", port = 50385):
    lang = etc.load_lang()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    server_socket.settimeout(0.1)
    logger.info("Start Server")
    print(lang["Message"]["MinecraftServer"]["Message"][0])
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            data = client_socket.recv(1024).decode("utf-8")
            if not data:
                client_socket.close()
                continue
            elif not len(data.split(",")) == 2:
                client_socket.close()
                continue
            motd, mcid = data.split(",")
            send_data = ini['basic']['version']+","+ini['basic']['port']
            client_socket.sendall(send_data.encode("utf-8"))
            result = start_minecraft_server(client_address[0], mcid, motd = motd)
            if result == 0:
                client_socket.sendall("0".encode())
            else:
                print(result)
                client_socket.sendall("1".encode())
            if os.path.isdir(f"minecraft/{client_address[0]}"):
                shutil.rmtree(f"minecraft/{client_address[0]}")
            client_socket.close()
        except KeyboardInterrupt:
            logger.info("STOP!!")
            return 0
        except socket.timeout:
            continue
        except:
            error = traceback.format_exc()
            logger.error(f"Error : Unknow\n\n{error}")
            continue

def register_server(port = 50384):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        ini = configparser.ConfigParser()
        ini.read('config/basic.ini', 'UTF-8')
        lang = etc.load_lang()
        ip = input(lang["Message"]["MinecraftServer"]["Message"][2]+" :")
        name = input(lang["Message"]["MinecraftServer"]["Message"][3]+" :").replace(",", "").replace("\n", "")
        message = input(lang["Message"]["MinecraftServer"]["Message"][4]+" :").replace(",", "").replace("\n", "")
        if len(name) >= 10: name = name[:10]
        if len(message) >= 20: message = message[:20]
        send_data = f"1,{name},"+ini["lang"]["lang"].replace(",", "")+","+ini["team"]["team_list"].replace(",", "")+","+message
        client_socket.connect((ip, port))
        client_socket.sendall(send_data.encode('utf-8'))
        data = client_socket.recv(1024)
        if int(data.decode("utf-8")) == 0:
            print(lang["Message"]["MinecraftServer"]["Message"][5])
        else:
            print(lang["Message"]["MinecraftServer"]["Message"][6])
    except:
        error = traceback.format_exc()
        print(lang["Message"]["MinecraftServer"]["Message"][6]+"\n"+error)

def start():
    lang = etc.load_lang()
    if not shutil.which('java'):
        print(lang["Message"]["MinecraftServer"]["Message"][1])
        return 1
    print("\n".join(lang["Message"]["MinecraftServer"]["ModeSelectMessage"]))
    while True:
        choice = input("[1,2,3] :")
        if choice == "1":
            try:
                socket_server("0.0.0.0")
            except KeyboardInterrupt:
                logger.info("STOP!!")
                return 0
        elif choice == "2":
            register_server()
        elif choice == "3":
            break
        else:
            continue
        print("\n".join(lang["Message"]["MinecraftServer"]["ModeSelectMessage"]))
    return 0