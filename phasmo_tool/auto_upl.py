#!/usr/bin/env python3
import requests
import shutil
import sys
import os

UPL_Link = "https://upl.crossroadsactua.repl.co/UPL.zip"

def download(url):
    get_responce = requests.get(url, stream=True)
    filename = url.split('/')[-1]
    
    with open(filename, "wb") as f:
        for chunk in get_responce.iter_content(chunk_size=1024):
            f.write(chunk)
            
    return filename

if __name__ == "__main__":
    py_ver = sys.version.split('.',2)[:2]
    
    if int(py_ver[0]) >= 3 and int(py_ver[1]) >= 7:
        os.system(f"{sys.executable} -m pip install --upgrade pip")
        print("Installing UPL")
        filename = download(UPL_Link)
        print("UPL installed\nCreating UPL Directory")
        pySitepath = ''
        for path in sys.path:
            if path.endswith("\\lib\\site-packages"):
                pySitepath = path
                
        if not os.path.exists(f'{pySitepath}/UPL'):
            os.mkdir(f'{pySitepath}/UPL')
        else:
            print("UPL Directory exists")
            
        print("Extracting UPL")
        shutil.unpack_archive(filename, f'{pySitepath}/UPL')
        print("Cleaning up")
        os.remove("UPL.zip")
        
        print("Installing UPL dependencies")
        os.system(f"{sys.executable} -m pip install cryptocode")
        os.system(f"{sys.executable} -m pip install pyautogui")
        os.system(f"{sys.executable} -m pip install playsound")
        os.system(f"{sys.executable} -m pip install pydub")
        os.system(f"{sys.executable} -m pip install pyttsx3")
        os.system(f"{sys.executable} -m pip install ffmpeg")      
        print("Done!")
    else:
        raise Exception("You are too out dated for this library.")
    
else:
    raise ImportError("This script cannot be imported")
