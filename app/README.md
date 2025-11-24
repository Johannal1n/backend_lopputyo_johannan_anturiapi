# Johannan AnturiAPI
* REST API tehdashallin lämpötila-antureiden hallintaan ja mittausdatan keräämiseen.


## Vaatimukset
* Python 3.13 tai 3.11+
* pip (Python-paketinhallinta)


## Asennus

* Aktivoi virtuaaliympäristö: Windows venv\Scripts\activate tai Linux source venv/bin/activate
* Asenna tarvittavat riippuvuudet: pip install -r requirements.txt


## Käynnistys juurikansiossa

* fastapi dev app/main.py
* Avaa selaimessa API-dokumentaatio http://127.0.0.1:8000/docs
* Tietokanta luonti tapahtuu automaattisesti sovelluksen ensimmäisen käynnistyksen yhteydessä ja tiedosto luodaan nimellä sensors.db