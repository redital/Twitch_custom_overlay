from config import *
import json
from config import PUNTI_CANALE_FILE

def load_punti_canale_info():
    try:
        with open(PUNTI_CANALE_FILE, "r") as file:
            info_punti_canale = json.load(file)
            global total_cost, max_cost, show_progress_bar
            total_cost = info_punti_canale["total_cost"]
            max_cost = info_punti_canale["max_cost"]
            show_progress_bar = info_punti_canale["show_progress_bar"]
            return total_cost, max_cost, show_progress_bar 
    except FileNotFoundError:
        return (0,4_000,False)

def save_punti_canale_info(f_total_cost=None, f_max_cost=None, f_show_progress_bar=None):
    if not f_total_cost:
        f_total_cost = total_cost
    if not f_max_cost:
        f_max_cost = max_cost
    if not f_show_progress_bar:
        f_show_progress_bar = show_progress_bar
    punti_canale_info = {
            "total_cost":f_total_cost, 
            "max_cost":f_max_cost,
            "show_progress_bar":f_show_progress_bar
        }
    with open(PUNTI_CANALE_FILE, "w") as file:
        json.dump(punti_canale_info, file)

def check_goal_completed():
    global total_cost, max_cost, show_progress_bar
    if total_cost >= max_cost:
        print("Obiettivo punti canale raggiunto: {}/{}".format(total_cost, max_cost))
        total_cost = 0
        show_progress_bar = False

def update_punti_canale_info(cost_to_add):
    global total_cost, max_cost, show_progress_bar
    if show_progress_bar:
        total_cost += cost_to_add
    check_goal_completed()
    save_punti_canale_info()

total_cost, max_cost, show_progress_bar = load_punti_canale_info()
