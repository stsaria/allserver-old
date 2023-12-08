import minecraft_server, list_server, client, check, etc, sys

def main(args : list):
    lang = etc.load_lang()
    if len(args) >= 2:
        if "--help" in args:
            print("\n".join(lang["Message"]["Main"]["HelpMessage"]))
        elif "--start-minecraft-server" in args:
            minecraft_server.socket_server()
        elif "--start-list-server" in args:
            list_server.start_server()
        elif "--search" in args[1] and len(args[1].split("/")) == 2:
            client.search_servers(args[1].split("/")[1])
    else:
        print("\n".join(lang["Message"]["Main"]["ModeSelectMessage"]))
        while True:
            mode = input("[1,2,3,4] :")
            if mode == "1":
                client.start()
            elif mode == "2":
                minecraft_server.start()
            elif mode == "3":
                list_server.start()
            elif mode == "4":
                break
            else:
                continue
            print("\n".join(lang["Message"]["Main"]["ModeSelectMessage"]))
    return 0

if __name__ == "__main__":
    print("AllServer\n")
    result = check.check()
    if result != 0:
        sys.exit(int("0"+str(result)))
    sys.exit(int("1"+str(main(sys.argv))))