import urllib.request
import gui
import gui.alert

# Check if all URIs are valid, else exit program
def check_valid_config_uris(config):
    for target in config["Videos"]:
        src = config["Videos"][target]["Source"]
        try:
            urllib.request.urlopen(src)
            print(f"[uri.py] Found URI: {src}")
        except:
            print(f"[uri.py] Malformed Source URI: {src}")
            gui.alert.show_alert(f"Malformed Source URI for {target}\n{src}", config)
            exit(-1)

def preload_uris(config, vlc):
    uris = {}
    for target in config["Videos"]:
        src = config["Videos"][target]["Source"]
        print(f"[uri.py] Loading {target}({src})")
        uris[target] = vlc.media_new(src)
    
    return uris
