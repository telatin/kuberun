import configparser
import os
import sys
# ~/.config/kuberun/config.ini
DEFAULT_CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".config", "kuberun.ini")
USER_NAME = os.environ.get("JUPYTERHUB_USER", os.environ.get("USER", "unknown"))
SYSTEM_TMPDIR = os.environ.get("TMPDIR", "/tmp")
WORKDIRS = [f"/shared/team/kuberun/{USER_NAME}/", os.path.join(os.path.expanduser("~"), "kuberun"), f"/{SYSTEM_TMPDIR}/kuberun"]

def makedatadir(dir=None, default_dirs=WORKDIRS):
    dirs = default_dirs
    if dir is not None:
        # put dir in front of dirs
        dirs = [dir] + dirs

    for directory in dirs:
        # Check if exists
        if os.path.exists(directory):
            return directory
        else:
            try:
                os.makedirs(directory, exist_ok=True)
                return directory
            except Exception as e:
                pass
    return None

def loadconfig(config_file=DEFAULT_CONFIG_FILE):
    # get env var "JUPYTERHUB_USER" if it is set, else $USER
    
    # If file does not exist, create it and return empty config
    if not os.path.exists(config_file):
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        with open(config_file, "w") as f:
            f.write("[kuberun]\n")
            datadir = makedatadir()
            if datadir is not None:
                f.write(f"history_dir = {datadir}\n")
            
        return configparser.ConfigParser()
   
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def saveconfig(config, config_file=DEFAULT_CONFIG_FILE):
    with open(config_file, "w") as f:
        config.write(f)