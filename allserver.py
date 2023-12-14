import minecraft_server, list_server, logging, client, check, etc, sys, os

def main(args : list):
    lang = etc.load_lang()
    if len(args) >= 2:
        if "--help" in args:
            print("\n".join(lang["Message"]["Main"]["HelpMessage"]))
        elif "--start-minecraft-server" in args:
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
            try:
                minecraft_server.socket_server()
            except KeyboardInterrupt:
                logger.info("STOP!!")
                return 0
        elif "--start-list-server" in args:
            list_server.start_server()
        elif "--search" in args[1] and len(args[1].split("/")) == 2:
            mode_list = ["0", "0"]
            if "--plus-not-lang" in args:
                mode_list[0] = "1"
            if "--not-plus-team" in args:
                mode_list[1] = "1"
            mode = "".join(mode_list)
            client.search_servers(args[1].split("/")[1], mode = mode)
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