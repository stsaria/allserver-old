import configparser, requests, pickle, random, socket, check, time, etc
import traceback

def is_socket_closed(sock):
    try:
        sock.fileno()
        return False
    except socket.error:
        return True

def get_ip():
    try:
        res = requests.get('http://api.ipify.org/')
        return str(res.text)
    except:
        return ""

def search_servers(host, port = 50384, mode = "00", isprint = True, select_lang = ""):
    ini = configparser.ConfigParser()
    ini.read('config/basic.ini', 'UTF-8')
    lang = etc.load_lang()
    word = lang["Message"]["Client"]["WordMessage"]
    servers = []
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))

        send_data = ","
        if mode[0] == "0":
            if select_lang == "":
                send_data = ini['lang']['lang']+"/"+ini['lang']['spare_lang']+send_data
            else:
                send_data = select_lang+"/"+select_lang+send_data
        if mode[1] == "0":
            send_data = send_data+ini['team']['team_list']
        send_data = "0,"+send_data
        client_socket.sendall(send_data.encode('utf-8'))

        data = client_socket.recv(1024)
        if isprint == True:
            if int(data.decode('utf-8')) == 0:
                print(lang["Message"]["Client"]["Message"][0])
            else:
                print(lang["Message"]["Client"]["Message"][1])
        if int(data.decode('utf-8')) != 0:
            return 1, servers
        
        client_socket.sendall("next".encode())
        data = client_socket.recv(1024)
        
        if isprint == True:
            print(word[0]+f" : {len(pickle.loads(data))}\n")
            for i in pickle.loads(data):
                print(word[1]+f":{i[0]} IP:{i[1]} "+word[2]+f":{i[2]} "+word[3]+f":{i[3]} "+word[4]+f":{i[4]}")
            input()
        servers = pickle.loads(data)
    except:
        if isprint == True:
            error = traceback.format_exc()
            print(lang["Message"]["Client"]["Message"][1]+"\n"+error)
        return 1, servers
    finally:
        client_socket.close()
    return 0, servers

def input_ip():
    lang = etc.load_lang()
    ip = input(lang["Message"]["Client"]["Message"][2]+" :")
    return ip

def start_server(port = 50385, mode = 0):
    lang = etc.load_lang()
    servers = ip = ""
    if mode == 0:
        print(lang["Message"]["Client"]["WordMessage"][6], end = "")
        result, servers = search_servers(input_ip(), isprint = False)
        if result != 0:
            print(lang["Message"]["Client"]["Message"][1])
            return 1
        if len(servers) == 1:
            ip = servers[0][1]
        elif len(servers) < 1:
            print(lang["Message"]["Client"]["Message"][1])
            return 2
        elif ip == get_ip():
            print(lang["Message"]["Client"]["Message"][1])
            return 3
        else:
            ip = servers[random.randint(0,len(servers)-1)][1]
    elif mode == 1:
        print(lang["Message"]["Client"]["WordMessage"][5], end = "")
        ip = input_ip()
        if ip == get_ip():
            print(lang["Message"]["Client"]["Message"][10]+"\n\n"+lang["Message"]["Client"]["WordMessage"][5], end = "")
            ip = input_ip()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            client_socket.connect((ip, port))
            motd = input(lang["Message"]["Client"]["Message"][3]+" :").replace("\n", "").replace(",", "")
            mcid = input(lang["Message"]["Client"]["Message"][8]+" :").replace("\n", "").replace(",", "")
            client_socket.sendall(f"{motd},{mcid}".encode('utf-8'))
            data = client_socket.recv(1024)
            if not data:
                return 1
            server_version, server_port = data.decode("utf-8").split(",")
            print()
            print("\n".join(lang["Message"]["Client"]["StartServerMessage"]))
            print(lang["Message"]["Client"]["Message"][6]+" ",end="")
            while True:
                print(".",end="",flush=True)
                if check.network(ip, server_port):
                    break
                time.sleep(2)
            print("OK\n")
            print(lang["Message"]["Client"]["Message"][4].replace("@version@", server_version).replace("@port@", server_port))
            print(f"\nServerIP : {ip}",end="")
            if not server_port == "25565":
                print(f":{server_port}")
            else:
                print()
            data = client_socket.recv(1024)
            if int(data) == 0:
                print(lang["Message"]["Client"]["Message"][5])
            else:
                print(lang["Message"]["Client"]["Message"][9])
        except ConnectionRefusedError:
            print(lang["Message"]["Client"]["Message"][1])
            print(lang["Message"]["Client"]["Message"][7])
            if mode == 0:
                continue
        except:
            error = traceback.format_exc()
            print(lang["Message"]["Client"]["Message"][1]+"\n"+error)
            return 1
        finally:
            if not is_socket_closed(client_socket):
                client_socket.close()
        break
    return 0

def start():
    lang = etc.load_lang()
    print()
    print("\n".join(lang["Message"]["Client"]["ModeSelectMessage"]))
    while True:
        choice = input("[1,2,3,4] :")
        if choice == "1":
            print(lang["Message"]["Client"]["WordMessage"][6], end = "")
            search_servers(input_ip())
        elif choice == "2":
            start_server(mode = 0)
        elif choice == "3":
            start_server(mode = 1)
        elif choice == "4":
            break
        else:
            continue
        print("\n".join(lang["Message"]["Client"]["ModeSelectMessage"]))
    return 0