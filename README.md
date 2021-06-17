# UniStats: Opendata riguardanti il mondo universitario

Unistats è una webapp programmata in Python, con frontend in HTML/CSS/JavaScript, che permette di visualizzare in maniera comoda e pratica gli opendata forniti dal MIUR e dall'ISTAT, con una spiegazione pertinente di ciò che significano. L'installazione è facile e veloce e non richiede quasi alcuna modifica al codice.

  ![](/static/assets/logos.png)
  

## Installazione

  

Per installare la webapp è necessario un server con Python 3.8 installato. Le librerie necessarie per il funzionamento della webapp sono segnate nel file `requirements.txt` che può essere passato come parametro a pip. Infine, basta impostare che il file `application.py` venga avviato automaticamente all'avvio del server.

  
Si consiglia di configurare un cronjob che ogni settimana mandi una richiesta GET alla pagina /doUpdate per eseguire l'update automatico di parte dei dataset

  

La webapp dovrebbe funzionare in maniera completamente automatica.

  
  

## Aggiornamento dei dataset

  

Per aggiornare i dataset, far riferimento alle istruzioni sotto riportate (estratte da `application.py`):

  

> #A causa di un errore nella creazione del file riguardante gli

> iscritti per ogni ateneo da parte del MIUR il file

> #riguardante gli iscritti per ateneo non sono scaricabili dinamicamente e va sostituito manualmente.

> #Allo stesso modo, i dati ottenuti tramite l'istat non sono scaricabili dinamicamente tramite la api in quanto

> #le sue prestazioni sono limitate (oltre a non permettere i filtri necessari per ottenere i file).

> #Il dataset delle provincie viene aggiornato automaticamente ogni settimana. Gli altri vanno sostituiti manualmente.

>

> #I dataset statici vanno inseriti nella cartella /static/notUpdating/

> #Il dataset riguardante gli iscritti per ateneo va scaricato a questo link

> http://dati.ustat.miur.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/32d26e28-a0b5-45f3-9152-6072164f3e63/download/iscrittixateneo.csv

> #e rinominato iscrittiAteneo.csv

>

> #Il dataset riguardante gli iscritti emigrati dalla regione è stato creato manualmente a partire da altri dati e non può essere aggiornato

>

> #I dataset riguardanti la percentuale di disoccupazione e la retribuzione oraria media sono reperibili a questo portale

> http://dati.istat.it/

> #Sfortunatamente la funzione di ricerca del sito è molto lenta e limitata, comunque sia i due data set sono "Tasso di Disoccupazione -

> Dati Provinciali"

> #e "Retribuzione oraria media per titolo di studio". In entrambi i casi, è necessario filtrare i risultati per le sole provincie del

> Veneto.

> #I file vanno rinominati retribuzioneMedia.csv e taxDisocc.csv

>

> #Fortunatamente, si aggiornano solo annualmente
