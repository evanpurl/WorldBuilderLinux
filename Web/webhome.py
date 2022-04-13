import sys
from waitress import serve
from flask import Flask, render_template, request
import os

app = Flask(__name__)


@app.route("/")
def login():
    return render_template('login.html')


@app.route(f'/server/', methods=['POST', 'GET'])
def data():
    if request.method == 'POST':
        os.chdir(f"{sys.path[0]}")
        os.chdir("../")
        data2 = request.form['sid']
        playerslist = []
        if os.path.exists(f"World/{data2}"):
            os.chdir(f"World/{data2}")
            playernum = os.listdir(os.getcwd() + "/Players")
            for a in playernum:
                if os.path.exists(os.getcwd() + f"/Players/{str(a)}/name.txt"):
                    with open(os.getcwd() + f"/Players/{str(a)}/name.txt", 'r') as f:
                        playerslist.append(a + " " + f.readline())
                        f.close()
                else:
                    playerslist.append(a)
            yield render_template('serverdata.html', id=data2, players=playerslist)
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route(f'/player', defaults={'serverid': '0', 'playerid': '0'})
@app.route(f'/player/<serverid>/<playerid>', methods=['POST', 'GET'])
def player(serverid, playerid):
    os.chdir(f"{sys.path[0]}")
    os.chdir("../")
    if os.path.exists(f"World/{str(serverid)}"):
        os.chdir(f"World/{str(serverid)}")
        if os.path.exists(os.getcwd() + f"/Players/{playerid}/wallet.txt"):
            with open(os.getcwd() + f"/Players/{playerid}/wallet.txt", "r") as f:
                mon = f.readline()
                f.close()
        if os.path.exists(os.getcwd() + f"/Players/{playerid}/name.txt"):
            with open(os.getcwd() + f"/Players/{playerid}/name.txt", "r") as f:
                name = f.readline()
                f.close()
        elif not os.path.exists(os.getcwd() + f"/Players/{playerid}/wallet.txt"):
            mon = str(0)
        elif not os.path.exists(os.getcwd() + f"/Players/{playerid}/name.txt"):
            name = "Player not found"
        return render_template('playerhouse.html', playername=name, money=mon)
    else:
        return "Error"


@app.route('/townhall', defaults={'serverid': '0'})
@app.route('/townhall/<serverid>')
def townhall(serverid):
    servstats = []
    os.chdir(f"{sys.path[0]}")
    os.chdir("../")
    if os.path.exists(f"World/{serverid}"):
        os.chdir(f"World/{serverid}")
        if os.path.exists(os.getcwd() + "/upgrades"):
            upgrades = os.listdir(os.getcwd() + "/upgrades")
            servstats.append("Number of upgrades: " + str(len(upgrades)))
            servstats.append("-------------------")
            for a in upgrades:
                servstats.append(a.replace(".txt", ""))
            servstats.append("-------------------")
        playernum = os.listdir(os.getcwd() + "/Players")
        servstats.append(str(len(playernum)) + " Players")
        if os.path.exists("minemultiply.txt"):
            with open("minemultiply.txt", "r") as f:
                servstats.append(f"Mining Multiplier: {str(float(f.readline()))}x")
                f.close()
        if os.path.exists("lumbermultiply.txt"):
            with open("lumbermultiply.txt", "r") as f:
                servstats.append(f"Lumber Multiplier: {str(float(f.readline()))}x")
                f.close()
        if os.path.exists("taxrate.txt"):
            with open("taxrate.txt", "r") as f:
                servstats.append(f"Tax Rate: {(str(round(float(f.readline()) * 100)))}%")
                f.close()
        if os.path.exists("tier.txt"):
            with open("tier.txt", "r") as f:
                servstats.append("Server Tier: " + f.readline())
                f.close()
        if os.path.exists("treasury.txt"):
            with open("treasury.txt", "r") as f:
                servstats.append("Server treasury: " + f'{str(format(float(f.readline()), ","))}')
                f.close()
        return render_template('townhall.html', stats=servstats)


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=27017)
