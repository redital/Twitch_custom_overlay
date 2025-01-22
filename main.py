from flask import Flask, jsonify, make_response,redirect,render_template
from flask import request as flask_request
from urllib.parse import urlencode

import config
from methods import twitch
from methods import rewards_request_handler
from methods import events
from methods import barra_punti_canale

app = Flask(__name__)


# Homepage a http://localhost:443
@app.route("/")
def hello_world():
    twitch.authentication(config.CLIENT_ID,config.SECRET)
    return render_template("home.html")

@app.route("/authorization_code_interceptor")
def authorization_code_interceptor():
    for k,v in flask_request.args.items():
        print(k,v)
    code = flask_request.args.get('code')
    if code == None:
        return "Error {}: {}".format(flask_request.args.get('error'), flask_request.args.get('error_description'))
    twitch.authentication_authorized(config.CLIENT_ID,config.SECRET,config.REDIRECT_URI_AUTHORIZATION_CODE,code,force=True) 
    return "Grazie per aver autorizzato per gli scope {}".format(flask_request.args.get('scope'))

@app.route("/authorize")
def authorize():
    scopes = flask_request.args.getlist('scope')
    url = twitch.get_auth_url(config.CLIENT_ID,config.REDIRECT_URI_AUTHORIZATION_CODE,scopes)
    return '<p>{}</p><a href="{}">Connect with Twitch</a>'.format(" ".join(scopes),url)

@app.route("/custom_rewards_list")
def lista_premi():
    twitch.refresh_token(config.CLIENT_ID,config.SECRET)
    headers = twitch.get_headers(token_tipe="user")
    headers["Content-Type"] = "application/json"
    data = {
        "broadcaster_id": twitch.get_broadcaster_id("redital00")
        }
    res = twitch.send_twitch_request("GET","channel_points/custom_rewards",params=data,headers=headers)
    itemlist = res.json()["data"]
    item_dict = {v["title"]:v for v in itemlist}
    return jsonify(item_dict)

@app.route("/list")
def lista_sottoscrizioni():
    twitch.authentication(config.CLIENT_ID,config.SECRET)
    headers = twitch.get_headers(token_tipe="app")
    res = twitch.send_twitch_request("GET","eventsub/subscriptions",headers=headers)
    return res.json()

#channel.channel_points_custom_reward_redemption.add
@app.route("/subscribe/<service>")
def sottoscrivi_evento(service):
    version = flask_request.args.get('version')
    id = flask_request.args.get('id')
    twitch.refresh_token(config.CLIENT_ID,config.SECRET)
    headers = twitch.get_headers(token_tipe="app")
    headers["Content-Type"] = "application/json"
    data = {
        "type": service,
        "version": version,
        "condition": {
            "broadcaster_user_id": str(twitch.get_broadcaster_id("redital00")),
            "reward_id": id
            },
        "transport": {
            "method": "webhook",
            "callback": config.REDIRECT_URI_CHANNEL_POINT_NOTIFICATION,
            "secret": "s3cre77890ab",
        },
    }
    res = twitch.send_twitch_request("POST","eventsub/subscriptions",body=data,headers=headers)
    
    return jsonify(res.json())

@app.route("/subscribe/punti_canale/<nome_premio>")
def sottoscrivi_evento_riscatto_punti_canale(nome_premio):
    servizio = "channel.channel_points_custom_reward_redemption.add"
    versione = 1
    premi = lista_premi().get_json()
    premio = premi[nome_premio]
    id_premio = premio["id"]
    
    return redirect("/subscribe/{}?version={}&id={}".format(servizio,versione,id_premio))

@app.route("/subscribe/delete/<id>")
def delete_subscription(id):
    #id = flask_request.args.get('id')
    twitch.refresh_token(config.CLIENT_ID,config.SECRET)
    headers = twitch.get_headers(token_tipe="app")
    headers["Content-Type"] = "application/json"
    params = {
        "id" : id
    }
    formatted_params = "?{}".format(urlencode(params))
    res = twitch.send_twitch_request("DELETE","eventsub/subscriptions" + formatted_params,headers=headers)
    if str(res.status_code)[0] == "2":
        return "sottoscrizione con id {} eliminata".format(id)
    else:
        return res.text

@app.route("/channel_point_notification",methods = ['POST'])
def channel_point_notification():
    body = flask_request.get_json()
    # Gestione challenge
    if("challenge" in dict(flask_request.get_json()).keys()):
        res = make_response(body["challenge"],200)
        return res
    # Effettivo intento dell'endpoint
    rewards_request_handler.add_request(body["event"])
    events.handle_incoming_request(rewards_request_handler.pop_request())
    print(body["event"]["reward"]["title"] + " riscattato da " + body["event"]["user_name"])
    return ""


@app.route("/set_new_channel_rewards_goal")
def set_new_channel_rewards_goal():
    goal = flask_request.args.get('goal')
    azzera_punti_attuali = flask_request.args.get('azzera_punti_attuali',True)
    print(azzera_punti_attuali)
    print(not(azzera_punti_attuali.lower() == "false"))
    if not goal:
        return "Bad Request<br><br>Immettere il numero di punti canale da impostare come obiettivo", 400
    try:
        goal = int(goal)
        azzera_punti_attuali = not(azzera_punti_attuali.lower() == "false")
    except TypeError:
        return "Bad Request<br><br>Il goal deve essere un intero e azzera_punti_attuali un booleano", 400
    except ValueError:
        return "Bad Request<br><br>Il goal deve essere un intero e azzera_punti_attuali un booleano", 400
    if azzera_punti_attuali:
        barra_punti_canale.total_cost = 0
    barra_punti_canale.save_punti_canale_info(None,goal,True)
    data = {}
    events.handle_new_goal(data)
    return "Nuovo obbiettivo punti canale impostato a {}".format(goal)

@app.route("/add_points_to_goal_bar")
def add_points_to_goal_bar():
    amount = flask_request.args.get('amount')
    if not amount:
        return "Bad Request<br><br>Immettere il numero di punti canale da impostare come obiettivo", 400
    try:
        amount = int(amount)
    except TypeError:
        return "Bad Request<br><br>Il goal deve essere un intero", 400
    except ValueError:
        return "Bad Request<br><br>Il goal deve essere un intero", 400
    data = {"increment": amount}
    events.handle_points_update(data)
    barra_punti_canale.update_punti_canale_info(amount)
    return "Aggiunti {} punti".format(amount)

# Serviva nell'approccio polling
#@app.route("/get_pending_reward_request")
#def get_pending_reward_request():
#    info = rewards_request_handler.pop_request()
#    if info == None: 
#        status_code = 404
#        return "", status_code
#    else: 
#        status_code = 200    
#        return info, status_code
#

@app.route("/render")
def prova_render():
    barra_punti_canale.load_punti_canale_info()
    total_cost = barra_punti_canale.total_cost
    max_cost = barra_punti_canale.max_cost
    show_progress_bar = barra_punti_canale.show_progress_bar
    return render_template("allert_web_scket_version.html", total_cost=total_cost, max_cost=max_cost, show_progress_bar=show_progress_bar)

@app.route("/fake_request")
def fake_request():
    
    request = {}

    request["user_name"] = "prova user_name"
    request["user_input"] = "prova user_input"
    request["reward"] = {}
    request["reward"]["id"] = "prova reward id"
    request["reward"]["title"] = "Poo Bee"
    request["reward"]["prompt"] = "prova reward prompt"
    request["reward"]["cost"] = "200"
    
    rewards_request_handler.add_request(request)
    events.handle_incoming_request(rewards_request_handler.pop_request())

    return "Fatto"



if __name__ == '__main__':
    events.socketio.init_app(app, async_mode="eventlet", ssl_context="adhoc")
    events.socketio.run(app,**config.flask_app_config)
