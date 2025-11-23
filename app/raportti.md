# Johannan AnturiAPI:n Backend lopputyön raportti


## 1. Tekniset valinnat ja resurssit

Työ toteutettiin Pythonilla ja versio 3.13. 

Projektissa käytetty koodi oli pohjana, jota luennoilla syksyn aikana on viikottain toteutettu harjoitustyössä (shoes/books).

* Framework: FastAPI.Valitsin FastAPIn, koska se ooli käytössä myös luennon harjoitustehtäväissä.
* Tietokanta: SQLite. Tehtävänannon mukaisesti erillisiä tietokantapalvelimia ei saanut asentaa, joten tiedostopohjainen SQLite oli ainoa keksimäni ratkaisu.
* ORM: SQLModel. Käytin SQLModelia, koska sitä käytetty myös harjoitetustehtäävässä (lue: koodin pohja).


## 2. Endpointien suunnittelu

Endpointit suunnittelin seuraavasti:

* `/blocks`: Lohkojen hallinta. Lohkot ovat ylätason käsitteitä ja joihin anturit kuuluvat.
* `/sensors`: Antureiden hallinta. Täällä tehdään lisäykset ja muutokset.
    * `/sensors/{id}/state`: Eriytetty polku tilamuutoksille (PATCH), koska tehtävänannossa oli vaatimuksena, että tilan muuttaminen tulee toimia hallitusti.
* `/measurements`: Mittauksien datan vastaanotto.

Jos anturi on `error`-tilassa, mittaus hylätään (`HTTP 400`), kuten vaatimusmäärittelyssä edellytettiin.


## 3. Tekoälyn käyttö

Käytin tekoälyä (ChatGPT) apuna erityisesti vastaan tulleissa virhetilanteissa ja ohjeistuksena tarkistaa tai mitä tulisi korjata, mm fastiapi docs:n errorit ja toimivuus. Virheet löytyivät koodin pääsääntöisesti syntaxeista tai kirjoitusvirheistä. Pyysin tekoälyä mm. myös selittämään CORS-virheet ja auttamaan requirements-tiedoston sisällön kanssa varmistaen, että on kaikki tarvittava. Varmistin itse, että tekoälyn tuottama koodi noudatti tehtävänannon logiikkaa.


## 4. Oppiminen

Opin työssä erityisesti FastAPI:n ja tietokannan välistä yhteistoimintaa. Ymmärrän nyt paremmin, miten HTTP-metodeja (GET, POST, PATCH) käytetään oikeaoppisesti eri tilanteissa. Myös virhetilanteiden hallinta (`HTTPException`) ja Swagger-dokumentaation hyödyntäminen testauksessa tuli tutuksi.


## 5. Ohjeet Johannan AnturiAPI:n käynnistämiseksi

* Ohjeet README.md -tiedostolta.