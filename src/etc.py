import configparser, json, os

def load_lang():
    ini = configparser.ConfigParser()
    ini.read('config/basic.ini', 'UTF-8')
    lang_file = ""
    if os.path.isfile(f"lang/{ini['lang']['lang']}.json"):
        lang_file = f"{ini['lang']['lang']}.json"
    elif os.path.isfile(f"lang/{ini['lang']['spare_lang']}.json"):
        lang_file = f"{ini['lang']['spare_lang']}.json"
    with open(f"lang/{lang_file}", encoding="UTF-8") as f:
        lang = json.load(f)
    return lang