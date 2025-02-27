import urllib.request
import gui
import gui.alert

# Check if all URIs are valid, else exit program
def check_valid_config_uris(config):
    for gpio in config["Videos"]:
        src = config["Videos"][gpio]["Source"]
        try:
            urllib.request.urlopen(src)
            print(f"[uri.py] Found URI: {src}")
        except:
            print(f"[uri.py] Malformed Source URI: {src}")
            gui.alert.show_alert(f"Malformed Source URI for {gpio}\n{src}", config)
            exit(-1)