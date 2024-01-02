import sys, os

if "src" in os.path.abspath(os.path.dirname(os.path.abspath(sys.argv[0]))).replace("\\", "/").split("/") and os.getcwd().replace("\\", "/").split("/")[-1] == "src":
    os.chdir('../')
elif not "src" in os.path.abspath(os.path.dirname(os.path.abspath(sys.argv[0]))):
    os.chdir(os.path.abspath(os.path.dirname(os.path.abspath(sys.argv[0]))))
else:
    os.chdir(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), '..')))

import install_auto_run, minecraft_server, list_server, check, build, etc
import logging

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
            try:
                list_server.start_server()
            except KeyboardInterrupt:
                pass
        elif "--install-auto-run" in args:
            install_auto_run.install()
        elif "--build" in args:
            build.install()
    else:
        print("\n".join(lang["Message"]["Main"]["ModeSelectMessage"]))
        while True:
            mode = input("[1,2,3,4] :")
            if mode == "1":
                minecraft_server.start()
            elif mode == "2":
                list_server.start()
            elif mode == "3":
                install_auto_run.install()
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