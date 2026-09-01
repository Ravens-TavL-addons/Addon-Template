


from .logger import *
import os
import threading
import time

from server.core.data_store import CONSOLE_TOKEN_FILE # type: ignore
from tavern_shared.ws_console_client import WsConsoleClient # type: ignore



'''
addon Example code for a mod that connects to the console and sends commands. This is a template for creating your own server addon.



'''





logger = Logger("MyAddon.log")

addon_name = author_data.get("name", "Unknown")
_stop_event = threading.Event()


    





def on_shutdown():
    global _ws_client
    _stop_event.set()
    
    if _ws_client is not None:
        _ws_client.disconnect()
        _ws_client = None
    logger._log(f"[{addon_name}] Logger shutting down.")


def on_line(line):
    return  # This is for subscriptions do with this as you wish
        

def on_disc(reason=""):
    global _ws_client
    if reason:
        logger._log(f"[{addon_name}] disconnected from console: {reason}")
       
       
        if _ws_client is not None: #ignore 
            _ws_client.disconnect() #ignore
            _ws_client = None
            logger._log("[{addon_name}] websocket client disconnected, attempting to reconnect...")
            threading.Thread(target=startup, daemon=True).start()   
    else:
        logger._log("[{addon_name}] disconnected from console.")
        _stop_event.clear()
        
        if _ws_client is not None:
            _ws_client.disconnect()
            _ws_client = None
            logger._log("[{addon_name}] websocket client disconnected, attempting to reconnect...")
            threading.Thread(target=startup, daemon=True).start()


def _wait_for_token(check_every=1.0):
    while not _stop_event.is_set():
        try:
            if os.path.isfile(CONSOLE_TOKEN_FILE):
                token = open(CONSOLE_TOKEN_FILE, "r").read().strip()
                if token:
                    return token
        except Exception:
            pass
        time.sleep(check_every)
    return ""



def startup():
    global _ws_client

    token = _wait_for_token()
    if not token:
        logger._log("[{addon_name}] startup canceled before token became available.")
        return

    logger._log(f"Console token: {token}")
    logger._new_line()
    logger._log("[{addon_name}] starting up and attempting to connect to console...")

    if _ws_client is None:
        _ws_client = WsConsoleClient()
    
    while not _stop_event.is_set():
        client = _ws_client
        if client is None:
            logger._log("[{addon_name}] websocket client unavailable; stopping startup loop.")
            return
        logger._log("[{addon_name}] attempting to connect to console...")
        try:
            success, msg = client.connect("127.0.0.1", token,on_line=on_line, on_disc=on_disc)
        except Exception as e:
            logger._log(f"[{addon_name}] connect RAISED: {type(e).__name__}: {e}")
            time.sleep(2.0)
            continue
        logger._log(f"[{addon_name}] connect attempt result: {success}, message: {msg}")
        if not success:
            logger._log(f"[{addon_name}] console not ready yet ({msg}); retrying in 2s...")
            time.sleep(2.0)
            continue
        if success:
            logger._log(f"[{addon_name}] connected to console: {msg}")

            logger._new_line()
            
            ## you can send commands to the console here if you want, for example:
            client.send("Player message Hello from MyAddon!")






        logger._log(f"[{addon_name}] console not ready yet ({msg}); retrying in 2s...")
        time.sleep(2.0)


threading.Thread(target=startup, daemon=True).start()
