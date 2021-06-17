from flask import Flask, render_template, jsonify, request, make_response #BSD License
import requests #Apache 2.0

#StdLibs
import json
from os import path

import csv

###################################################
#Programmato da Alex Prosdocimo e Matteo Mirandola#
###################################################

application = Flask(__name__)


@application.route("/")  # Index
def index():
    return make_response(render_template("index.html"))


@application.route("/getGraph", methods=["POST", "GET"])
def getgraph():
    #Metodo POST: responsabile di ottnere i dati in formato json dal server. 
    #Il server si aspetta un campo data che contenga il nome di un file esistente nel server nella cartella /static/json/
    #Se non trova il file da un 404
    #Se non trova il campo data da un 400
    if request.method == "POST":
        if('data' in request.form):
            if(path.exists("static/jsons/" + request.form['data'] + ".json")):
                with open("static/jsons/" + request.form['data'] + ".json", "r") as file:
                    jsonStr = file.read()
                jsonStr = json.loads(jsonStr)
                return jsonify(jsonStr)
            else:
                return "<h1>404 NOT FOUND"
        else:
            return "<h1>400 BAD REQUEST"
    else:
        #Metodo GET:
        #si aspetta un campo graph che contenga uno dei nomi sotto presenti
        #nel caso di mf e emig si aspetta anche un secondo campo che specifichi
        #l'università o la provincia-
        #Inoltre, iscrittiAtn e mf POSSONO (ma non devono necessariamente) avere
        #un campo aggiuntivo che filtri i dati di uno specifico anno o per uno specifico sesso2
        if 'graph' in request.args:

            # HBar Graph per la paga oraria provinciale a seconda del livello di istruzione
            if(request.args['graph'] == "pagaOra"):
                return make_response(render_template("graphs/pagaOra.html"))

            # Line Graph per gli iscritti alle università nel veneto per anno
            elif(request.args['graph'] == "iscrittiAtn"):
                if('sex' in request.args):
                    return make_response(render_template("graphs/iscrittiAtn.html", sex=int(request.args['sex'])))
                else:
                    return make_response(render_template("graphs/iscrittiAtn.html", sex=0))

            elif(request.args['graph'] == "disoccupati"):
                return make_response(render_template("graphs/disoccupatiGraph.html"))

            elif(request.args['graph'] == "iscrittiProv"):
                return make_response(render_template("graphs/iscrittiProv.html"))

            # Donut Graph per la distribuzione di m/f nelle università in veneto
            elif(request.args['graph'] == "mf" and 'atn' in request.args):
                dir = "graphs/mf/mf" + request.args['atn'] + ".html"
                print(dir)
                if(path.exists("templates/" + dir)):
                    if('year' in request.args):
                        return make_response(render_template(dir, year=int(request.args['year'])))
                    else:
                        return make_response(render_template(dir, year=0))

            # Polar Area Graph per gli studenti emigrati in altre regioni
            elif(request.args['graph'] == "emig" and "prov" in request.args):
                dir = "graphs/emig/iscrittiEmig" + \
                    request.args['prov'] + ".html"
                if(path.exists("templates/" + dir)):
                    return make_response(render_template(dir))

    return "<h1>400 BAD REQUEST"

#Per aggiornare i dataset:
#A causa di un errore nella creazione del file riguardante gli iscritti per ogni ateneo da parte del MIUR il file
#riguardante gli iscritti per ateneo non sono scaricabili dinamicamente e va sostituito manualmente.
#Allo stesso modo, i dati ottenuti tramite l'istat non sono scaricabili dinamicamente tramite la api in quanto
#le sue prestazioni sono limitate (oltre a non permettere i filtri necessari per ottenere i file).
#Il dataset delle provincie viene aggiornato automaticamente ogni settimana. Gli altri vanno sostituiti manualmente.

#I dataset statici vanno inseriti nella cartella /static/notUpdating/
#Il dataset riguardante gli iscritti per ateneo va scaricato a questo link http://dati.ustat.miur.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/32d26e28-a0b5-45f3-9152-6072164f3e63/download/iscrittixateneo.csv
#e rinominato iscrittiAteneo.csv

#Il dataset riguardante gli iscritti emigrati dalla regione è stato creato manualmente a partire da altri dati e non può essere aggiornato

#I dataset riguardanti la percentuale di disoccupazione e la retribuzione oraria media sono reperibili a questo portale http://dati.istat.it/
#Sfortunatamente la funzione di ricerca del sito è molto lenta e limitata, comunque sia i due data set sono "Tasso di Disoccupazione - Dati Provinciali"
#e "Retribuzione oraria media per titolo di studio". In entrambi i casi, è necessario filtrare i risultati per le sole provincie del Veneto.
#I file vanno rinominati retribuzioneMedia.csv e taxDisocc.csv

#Fortunatamente, si aggiornano solo annualmente

@application.route("/doUpdate")
def updateData():
    #File iscritti per ateneo
    #I dati vengono inseriti in un dizionario come array, il formato è più sotto
    with open('static/notUpdating/iscrittiAteneo.csv', newline='') as f: #Qui si può cambiare il nome del file se necessario, basta che sia in formato csv corretto
        reader = csv.reader(f)
        data = list(reader)[1:]
        iscrittiAteneo = {
            'Venezia CF': [],
            'Verona': [],
            'Venezia IUAV': [],
            'Padova': []}

        for row in data:
            row = row[0].split(';')
            if row[1] == 'Padova' or 'Venezia C' in row[1] or row[1] == 'Venezia Iuav' or row[1] == 'Verona':
                tmp = row[1]
                if 'Venezia C' in row[1]:
                    tmp = 'Venezia CF'
                if tmp == 'Venezia Iuav':
                    tmp = 'Venezia IUAV'
                iscrittiAteneo[tmp].append(
                    row[0] + ';' + row[3] + ';' + row[4])

        iscrittiAteneoJson = json.dumps(iscrittiAteneo)
        # Formato: {"nomeAteneo" : ["annoScolastico;numeroIscrittiMaschi;numeroIscrittiFemmine",...,...],...,...}
        open('static/jsons/iscrittiAteneo.json',
             "wb").write(iscrittiAteneoJson.encode())

    # File iscritti emigrati in altre regioni
    with open('static/notUpdating/iscrittiEmig.json', newline='') as f: #Qui si può cambiare il nome del file se necessario, basta che sia in formato csv corretto

        reader = json.load(f)
        iscrittiEmig = {
            'vicenza': [],
            'verona': [],
            'venezia': [],
            'padova': [],
            'treviso': [],
            'belluno': [],
            'rovigo': []}

        for row in reader['records']:
            if row[4].lower() == 'padova' or row[4].lower() == 'vicenza' or row[4].lower() == 'venezia' or row[4].lower() == 'verona' or row[4].lower() == 'treviso' or row[4].lower() == 'belluno' or row[4].lower() == 'rovigo':
                iscrittiEmig[row[4].lower()].append(
                    row[1] + ';' + row[4] + ';' + row[2] + ';' + str(row[6]))
        lista = {
            'vicenza': [],
            'verona': [],
            'venezia': [],
            'padova': [],
            'treviso': [],
            'belluno': [],
            'rovigo': []
        }
        count = 0

        for key in iscrittiEmig.keys():
            while len(iscrittiEmig[key]) > 2:
                tmp = iscrittiEmig[key].pop(0).split(';')
                if count == 0:
                    count = int(tmp[3])
                tmp2 = iscrittiEmig[key][0].split(';')[2]
                if tmp[2] == tmp2:

                    count += int(tmp[3])

                else:
                    lista[tmp[1].lower()].append(
                        tmp[0] + ';' + tmp[2] + ';' + str(count))
                    count = 0

    iscrittiEmigJson = json.dumps(lista)
    # Formato: {"cittàInMinuscolo" : ["annoScolastico;CittàDiProvenienzaInMaiuscolo;RegioneDiEsodo;NumeroStudenti",...,...],...,...}
    open('static/jsons/iscrittiEmig.json',
         "wb").write(iscrittiEmigJson.encode())
    # File paga media oraria per titolo di studio
    with open('static/notUpdating/retribuzioneMedia.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)[1:]
        retribuzione = {
            'Vicenza': [],
            'Verona': [],
            'Venezia': [],
            'Padova': [],
            'Treviso': [],
            'Belluno': [],
            'Rovigo': []}

        for row in data:
            if (row[1] == 'Padova' or row[1] == 'Vicenza' or row[1] == 'Venezia' or row[1] == 'Verona' or row[1] == 'Treviso' or row[1] == 'Belluno' or row[1] == 'Rovigo') and (row[5] != 'totale') and 'media)' in row[3]:
                # La lista è divisa in titolo di studio, reddito medio orario
                tmp = row[5]
                if 'nessun' in tmp:
                    tmp = 'nessuno'
                retribuzione[row[1]].append(tmp + ';' + str(row[8]))

        retribuzioneMediaJson = json.dumps(retribuzione)
        # Formato: {"nomeCittà" : ["laurea;media", "diploma;media", "nulla;media"],...,...}
        open('static/jsons/retribuzioneMedia.json',
             "wb").write(retribuzioneMediaJson.encode())

    # File %disoccupazione
    with open('static/notUpdating/taxDisocc.csv', newline='') as f: #Qui si può cambiare il nome del file se necessario, basta che sia in formato csv corretto
        reader = csv.reader(f)
        data = list(reader)[1:]
        lavoro = {
            'Vicenza': [],
            'Verona': [],
            'Venezia': [],
            'Padova': [],
            'Treviso': [],
            'Belluno': [],
            'Rovigo': []}

        for row in data:
            if (row[7] == '15-24 anni') and row[5] != 'totale':
                if row[5] == 'femmine':
                    lavoro[row[1]].append(str(row[10]))
                else:
                    lavoro[row[1]].append(str(row[8]) + ';' + str(row[10]))
        for key in lavoro.keys():
            tmp = lavoro[key][0] + ';' + lavoro[key][2]
            tmp2 = lavoro[key][1] + ';' + lavoro[key][3]
            lavoro[key].clear()
            lavoro[key].append(tmp)
            lavoro[key].append(tmp2)

        disoccupazioneJson = json.dumps(lavoro)
        # Formato: {"nomeCittà" : ["anno;percMaschi;percFemmine","anno;percMaschi;percFemmine"x],...,...}
        open('static/jsons/disoccupazione.json',
             "wb").write(disoccupazioneJson.encode())

    # File iscritti totali per provincia
    iscritti = requests.get(
        'http://dati.ustat.miur.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/eae4ee94-0797-41d2-b007-bc6dad3ef3e2/download/iscrittixresidenza.csv', allow_redirects=True)
    open('static/iscrittiProvincia.csv', 'wb').write(iscritti.content) #Qui si può cambiare il nome del file se necessario, basta che sia in formato csv corretto
    with open('static/iscrittiProvincia.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)[1:]

        iscrittiProvincia = {
            'vicenza': [],
            'verona': [],
            'venezia': [],
            'padova': [],
            'treviso': [],
            'belluno': [],
            'rovigo': []}

        for row in data:
            row = row[0].split(';')
            if row[2].lower() == 'padova' or row[2].lower() == 'vicenza' or row[2].lower() == 'venezia' or row[2].lower() == 'verona' or row[2].lower() == 'treviso' or row[2].lower() == 'belluno' or row[2].lower() == 'rovigo':
                iscrittiProvincia[row[2].lower()].append(
                    str(row[0]) + ';' + str(int(row[3])+int(row[4])))
        iscrittiProvinciaJson = json.dumps(iscrittiProvincia)
        # Formato: {"nomeCittà" : ["anno;numero"],...,...}
        open('static/jsons/iscrittiProvincia.json',
             "wb").write(iscrittiProvinciaJson.encode())
    return "200"

#########
#Startup#
#########

#Ad ogni riavvio forzato dell'applicazione, i dati vengono aggiornati (ci impiega qualche secondo al maassimo)

updateData()

if __name__ == '__main__':
    application.run(debug=True, port=80)
