# Johannan AnturiAPI:n Backend lopputyön raportti

## Johdanto

Tämä raportti käsittelee AnturiAPI-projektin suunnittelua ja toteutusta. Projektin tavoitteena oli luoda REST API kuvitteellisen tehdashallin lämpötila-anturidatan keräämiseen ja hallintaan. Järjestelmä mahdollistaa anturidatan vastaanottamisen, anturien hallinnan sekä historiadatan/lokituksen tarkastelun.


## 1. Tekniset valinnat ja resurssit

Työ toteutettiin Pythonilla ja versio 3.13. 

Projektissa käytetty koodi oli pohjana, jota luennoilla syksyn aikana on viikottain toteutettu harjoitustyössä (shoes/books).

* Ohjelmointikieli: Python 3.13
* Framework: FastAPI.Valitsin FastAPIn, koska se ooli käytössä myös luennon harjoitustehtäväissä.
* Tietokanta: SQLite. Tehtävänannon mukaisesti erillisiä tietokantapalvelimia ei saanut asentaa, joten tiedostopohjainen SQLite oli ainoa keksimäni ratkaisu.
* ORM: SQLModel. Käytin SQLModelia, koska sitä käytetty myös harjoitetustehtäävässä (lue: koodin pohja).
* Dokumentaatio: Swagger UI (automaattinen)


## 2. Endpointien suunnittelu

Endpointit suunnittelin seuraavasti:

* `/blocks`: Lohkojen hallinta. Lohkot ovat ylätason käsitteitä ja joihin anturit kuuluvat.
* `/sensors`: Antureiden hallinta. Täällä tehdään lisäykset ja muutokset.
    * `/sensors/{id}/state`: Eriytetty polku tilamuutoksille (PATCH), koska tehtävänannossa oli vaatimuksena, että tilan muuttaminen tulee toimia hallitusti.
* `/measurements`: Mittauksien datan vastaanotto.

* Jos anturi on `error`-tilassa, mittaus hylätään (`HTTP 400`), kuten vaatimuksien määrittelyssä edellytetty.

* Esimerkiksi uuden anturin luonti tapahtuu `POST /sensors/` -kutsulla ja tietyn anturin haku `GET /sensors/{id}` -kutsulla. 

* Erityishuomiona toteutin `/sensors/{id}/measurements` -endpointin, joka mahdollistaa mittaushistorian haun aikaleimojen perusteella (query parameters `start_time` ja `end_time`).

## 3. Arkkitehtyyri ja projektin rakenne


* main.py -> Sovelluksen käynnistyspiste
    * Database
        * database.py -> Tietokantayhteyden alustus
        * model.py -> SQLmodel-tietomallit
        * sensors_crud.py ->  Antureiden CRUD-operaatiot
        * blocks_crud.py -> Lohkojen CRUD-operaatiot
        * measurements_crud.py -> Mittausten CRUD-operaatiot
    * Routers
        * sensors.py -> Anturi-endpointit
        * blocks.py -> Lohko-endpointit
        * measurements.py -> Mittaus-endpointit
    * requirements-txt -> Python riippuvuudet
    * README.md -> Asennusohjeet
    * Raportti.md -> Tämä raportti
    

## 3. Ominaisuudet

Järjestelmä toteuttaa seuraavat vaatimusmäärittelyn mukaiset toiminnot:

* Anturien hallinta: Uusien anturien luonti, tietojen haku ja listaus lohkoittain.
* Mittausdata: Lämpötilamittausten vastaanotto (yhden desimaalin tarkkuus) ja historian selaus.
* Tilamuutokset: Anturin vikatilojen ja palautumisten automaattinen lokitus.
* Lohkot: Tehtaan fyysisten lohkojen hallinta.
* Suodatukset: Datan haku aikavälin tai anturin tilan perusteella.

## 4. Tietokantarakenne

Tietokanta koostuu kolmesta päätaulusta ja yhdestä historiataulusta:

* Block: Tallentaa lohkon nimen.
* Sensor: Tallentaa anturin tunnisteen, tilan ja viittauksen lohkoon.
* Measurement: Tallentaa lämpötilan ja aikaleiman. Linkittyy anturiin.
* StateChange: Toimii lokina. Aina kun anturin tila muuttuu, tähän tauluun kirjataan muutos ja aikaleima.

## 5. Tekoälyn käyttö

Käytin tekoälyä (ChatGPT) apuna erityisesti vastaan tulleissa virhetilanteissa ja pyytäen ohjeistuksena mitä tarkistaa tai mitä tulisi korjata, mm fastiapi docs:n errorit ja toimivuus. Virheet löytyivät koodin pääsääntöisesti syntaxeista tai kirjoitusvirheistä. Pyysin tekoälyä mm. myös selittämään CORS-virheet ja auttamaan requirements-tiedoston sisällön kanssa varmistaen, että on kaikki tarvittava. Sekä osassa varmistaen, että ymmärrän koodin kohdan/function tmv tarvittavan linkityksen oikeaan kohtaan. Varmistin itse, että tekoälyn tuottama koodi noudatti tehtävänannon logiikkaa. Tehtävän teossa auttoi hyvä koodipohja, jota tein opettajan luentojen mukana jokaisena viikkona (shoes), sekä myös viikkoharjoitukset (books).


## 6. Oppiminen

Opin työssä erityisesti FastAPI:n ja tietokannan välistä yhteistoimintaa. Ymmärrän nyt paremmin, miten HTTP-metodeja (GET, POST, PATCH, DELETE) käytetään oikeaoppisesti eri tilanteissa. Myös virhetilanteiden hallinta (`HTTPException`) ja Swagger-dokumentaation hyödyntäminen testauksessa tuli tutuksi. Virhetilanteissa opin kärsivällisyyttä, sekä luottoa siihen, että vielä keksi virheen ja saan sen korjattua.


## 7. Ohjeet Johannan AnturiAPI:n käynnistämiseksi

* Ohjeet README.md -tiedostolta.