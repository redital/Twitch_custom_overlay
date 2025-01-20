import os
import random
import barra_punti_canale

pending_requests = []

def add_request(request):
    barra_punti_canale.total_cost += int(request["reward"]["cost"])
    barra_punti_canale.save_punti_canale_info()
    info = {}
    info["user_name"]=request["user_name"]
    info["user_input"]=request["user_input"]
    info["reward_id"]=request["reward"]["id"]
    info["reward_title"]=request["reward"]["title"]
    info["reward_prompt"]=request["reward"]["prompt"]
    info["reward_cost"]=request["reward"]["cost"]
    info["data"]={}
    try:
        info = handlers[info["reward_title"]](info)
    except KeyError:
        print("Ricompensa punti canale {} non gestita".format(info["reward_title"]))
        return
    pending_requests.append(info)

def pop_request():
    if len(pending_requests)==0:
        print("Nessuna richiesta in pending")
        return None
    else:
        print("processiamo la richiesta di {} per {}".format(pending_requests[0]["user_name"],pending_requests[0]["reward_title"]))
        return pending_requests.pop(0)

def random_imperium_handler(info):

    cartelle = next(os.walk("static/Imperium"))[1]

    cartella = random.choice(cartelle)


    files = next(os.walk("static/Imperium/{}".format(cartella)))[2]
    mp3_files = [i for i in files if i.split(".")[-1].lower() == "mp3"]

    audio = random.choice(mp3_files)
    image = "greenscreen_antialiased.png"

    info["data"]["image_src"]="static/Imperium/{}/{}".format(cartella,image)
    info["data"]["audio_src"]="static/Imperium/{}/{}".format(cartella,audio)
    info["data"]["testo"]="{} scende sul campo di battaglia".format(info["user_name"])
    info["data"]["costo"]=int(info["reward_cost"])
    return info

def poo_bee_handler(info):
    info["data"]["image_src"]="static/PooBee/Senza titolo-1.png"
    info["data"]["audio_src"]="static/PooBee/poo-bee.mp3"
    info["data"]["testo"]=""
    info["data"]["costo"]=int(info["reward_cost"])
    return info

def a_munnezz_handler(info):
    info["data"]["image_src"]="static/A munnezz da gent/kid-meme.gif"
    info["data"]["audio_src"]="static/A munnezz da gent/A-munnezza-d_a-gente.mp3"
    info["data"]["testo"]=""
    info["data"]["costo"]=int(info["reward_cost"])
    return info

def lurk_handler(info):
    info["data"]["image_src"]="static/Lurk/GDKO9u9FvYohBJQ16UDpg1673339942807.gif"
    info["data"]["audio_src"]="static/Lurk/1-second-and-500-milliseconds-of-silence.mp3"
    info["data"]["testo"]=""
    info["data"]["costo"]=int(info["reward_cost"])
    return info

def poesia_handler(info):
    info["data"]["image_src"]="static/Poesia/libro.png"
    info["data"]["audio_src"]="static/Poesia/Notifica-Poesia.mp3"
    info["data"]["testo"]=""
    info["data"]["costo"]=int(info["reward_cost"])
    return info

def triplo_venti_handler(info):
    info["data"]["image_src"]="static/TRIPLO VENTI/il nulla.png"
    info["data"]["audio_src"]="static/TRIPLO VENTI/TRIPLO_VENTI.mp3"
    info["data"]["testo"]=""
    info["data"]["costo"]=int(info["reward_cost"])
    return info

handlers = {
    "Random Imperium" : random_imperium_handler,
    "Poo Bee" : poo_bee_handler,
    "A munnezz d'a gent" : a_munnezz_handler,
    "Lurkino <3 " : lurk_handler,
    "Leggiamo una poesia" : poesia_handler,
    "TRIPLO VENTI" : triplo_venti_handler
}