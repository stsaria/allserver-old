import threading, traceback, logging, pickle, socket, check, etc, csv, os

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter("%(asctime)s@ %(message)s"))
os.makedirs('./log', exist_ok=True)

file_handler = logging.FileHandler("./log/listserver.log", encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s '%(funcName)s'")
)

logging.basicConfig(level=logging.NOTSET, handlers=[stream_handler, file_handler])
logger = logging.getLogger(__name__)

def is_socket_closed(sock):
    try:
        sock.fileno()
        return False
    except socket.error:
        return True

def search_servers(location = ["", ""], team = [""]):
    servers = []
    result = None
    try:
        with open("data/listserver.csv", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if len(row) == 6:
                    if int(row[5]) < 30 and row[2] in location or int(row[5]) < 30 and location[0] == "" and location[1] == "":
                        if row[3].split("/") in team:
                            servers.append(row)
                        elif len(team) <= 0:
                            servers.append(row)
                        elif team[0] == "":
                            servers.append(row)
        if len(servers) > 20:
            servers = servers[-20:]
        result = 0
    except:
        error = traceback.format_exc()
        logger.error(f"Error : Unknow\n\n{error}")
        result = 1
    finally:
        return result, servers

def register_server(name : str, ip : str, country : str, team : str, message : str):
    try:
        ips = []
        with open("data/listserver.csv", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                if len(row) == 6:
                    ips.append(row[1])
        if ip in ips: return 0
        if team == "": team = "everyone/Everyone"
        with open("data/listserver.csv", mode="a", encoding="utf-8") as f:
            f.write(f"{name},{ip},{country},{team},{message},0\n")
        return 0
    except:
        error = traceback.format_exc()
        logger.error(f"Error : Unknow\n\n{error}")
        return 1

def handle_client(client_socket, address):
    logger.info(f"Connect : {address}")
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            logger.info(f"Receive : {address}")
            if data.decode('utf-8').split(',')[0] == "0":
                location = data.decode('utf-8').split(",")[1].split("/")
                if len(location) != 2:
                    location = ["", ""]
                if len(data.decode('utf-8').split(',')) != 3:
                    client_socket.sendall("1".encode('utf-8'))
                    logger.info(f"Send : {address}")
                    break
                result, servers = search_servers(location = location, team = data.decode('utf-8').split(",")[2].split("/"))
                if result != 0:
                    client_socket.sendall("2".encode('utf-8'))
                    logger.info(f"Send : {address}")
                    break
                client_socket.sendall("0".encode('utf-8'))
                logger.info(f"Send : {address}")
                data = client_socket.recv(1024)
                if not data:
                    break
                if data.decode('utf-8') == "next":
                    client_socket.sendall(pickle.dumps(servers))
                    logger.info(f"Send : {address}")
            elif data.decode('utf-8').split(',')[0] == "1":
                if len(data.decode('utf-8').split(',')) != 5:
                    client_socket.sendall("1".encode('utf-8'))
                    logger.info(f"Send : {address}")
                    break
                info = data.decode('utf-8').split(',')
                result = register_server(info[1], address[0], info[2], info[3], info[4])
                if result != 0:
                    client_socket.sendall("2".encode('utf-8'))
                    logger.info(f"Send : {address}")
                    break
                client_socket.sendall("0".encode('utf-8'))
            break
        except socket.timeout:
            continue
        except:
            error = traceback.format_exc()
            logger.error(f"Error : Unknow\n\n{error}")
            return
    logger.info(f"Close : {address}")
    if not is_socket_closed(client_socket):
        client_socket.close()

def start_server(host = "0.0.0.0", port = 50384):
    lang = etc.load_lang()
    if not os.path.isfile("data/listserver.csv"):
        try:
            with open("data/listserver.csv", mode="w") as f:
                f.write("Name,IP,Country,Team,Message,Badcount\n")
        except:
            logger.error(f"Error : Cant start server\nFail make file(data/listserver.csv)")
            return 2
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)
        server_socket.settimeout(0.7)
        logger.info("Start Server")
        print(lang["Message"]["ListServer"]["Message"][0])
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.start()
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        logger.error(f"STOP!!")
        return 0
    except:
        error = traceback.format_exc()
        logger.error(f"Error :\n{error}")
        return 1

def start():
    lang = etc.load_lang()
    if not os.path.isfile("data/listserver.csv"):
        print("\n".join(lang["Message"]["ListServer"]["SetupMessage"]))
        choice = input("[1,2] :")
        if choice != "1":
            return 0
        try:
            with open("data/listserver.csv", mode="w") as f:
                f.write("Name,IP,Country,Team,Message,Badcount\n")
        except:
            logger.error(f"Error : Cant start server\nFail make file(data/listserver.csv)")
            return 2
    if check.network(check_host="0.0.0.0", check_port=50384) == 0:
        logger.error(f"Error :Cant start server")
        return 3
    try:
        if start_server() != 0:
            print("Error")
            return 1
    except KeyboardInterrupt:
        pass
    return 0