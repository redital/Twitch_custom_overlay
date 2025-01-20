from config import *
import json
from config import PUNTI_CANALE_FILE

def load_punti_canale_info():
    try:
        with open(PUNTI_CANALE_FILE, "r") as file:
            info_punti_canale = json.load(file)
            total_cost = info_punti_canale["total_cost"]
            max_cost = info_punti_canale["max_cost"]
            return total_cost, max_cost
    except FileNotFoundError:
        return (0,4_000)

def save_punti_canale_info(f_total_cost=None, f_max_cost=None):
    if not f_total_cost:
        f_total_cost = total_cost
    if not f_max_cost:
        f_max_cost = max_cost
    punti_canale_info = {
            "total_cost":f_total_cost, 
            "max_cost":f_max_cost
        }
    with open(PUNTI_CANALE_FILE, "w") as file:
        json.dump(punti_canale_info, file)

total_cost, max_cost = load_punti_canale_info()
