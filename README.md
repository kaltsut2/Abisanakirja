# Abisanakirja

Sanaston opiskelusovellus keskipitkän ruotsin ylioppilaskoetta varten.
Rakennetaan `SPEC.md`:n mukaan. Ei palvelinta, ei tunnuksia, ei build-vaihetta.

## Tiedostot

| Tiedosto | Mitä |
|---|---|
| `index.html` | Koko sovellus – ainoa koodi |
| `sanasto.json` | Sanasto lukurakenteena. **Generoitu, älä muokkaa käsin** |
| `lahde/sanasto.txt` | Sanaston alkuperäinen lähde – muokkaukset tehdään tänne |
| `lahde/Ruotsin_sanasto.docx` | Sama sisältö Word-muodossa, luettavaksi |
| `tyokalut/rakenna_sanasto.py` | Muuntaa lähteen JSONiksi |
| `tyokalut/tee_ikonit.sh` | Tekee kotinäytön ikonit `ikoni-lahde.png`:stä |
| `manifest.webmanifest` | Kotinäyttöasennuksen tiedot |
| `ikoni.svg` | Ikoni vektorina (selaimen välilehti) |
| `ikoni-*-v1.png` | Kotinäytön ikonit, **generoituja** |

## Sanaston päivittäminen

Lisää tai korjaa rivi `lahde/sanasto.txt`:ssä ja aja:

```bash
python3 "tyokalut/rakenna_sanasto.py"
```

Skripti tulostaa tilastot ja varoittaa riveistä, joita se ei ymmärtänyt.

## Lähdemuoto

Lähde on OneNotesta kopioitua tekstiä sellaisenaan. Jäsennin tunnistaa rivit
niiden muodosta, ei erillisistä merkeistä:

| Rivi | Tulkinta |
|---|---|
| Lyhyt rivi, jota seuraa päiväys tai alaluvun numero | luku (OneNote-sivu) |
| `1.1 Ajattelu, ymmärtäminen ja mielipide` | alaluku |
| Lyhyt rivi ilman erotinta | väliotsikko |
| Yli 60 merkkiä tai päättyy pisteeseen | kappale |
| `tycka, tycker, tyckte, tyckt  (IIb)  –  olla jotain mieltä` | sana – **kaksi välilyöntiä** ajatusviivan molemmin puolin |
| `i förväg = etukäteen` | sana lyhyemmässä muodossa (Skrivtavla, luku 6.9) |
| *sisennetty* `Menar du allvar? = Oletko tosissasi?` | esimerkki |
| *sisennetty* `Korjaus: …` | korjaus (punainen) |
| *sisennetty* muu teksti | huomio (harmaa) |

Erotin `  –  ` on merkitsevä: yksi välilyönti ei riitä, koska ajatusviiva
esiintyy myös sanojen sisällä (`i dag – i går – i morgon`).

Muuntimen päättelemät asiat:

- **Sanaluokka** tulee taivutusluokasta, `en`/`ett`-alusta tai luvun otsikosta.
- **Rektio** tulee sulkeista (`klaga (på/över)`, `skydda (mot)`) tai luvun
  6.3–6.6 ilmauksista.
- **Vastakohta** syntyy `↔`-merkistä: rivi jaetaan kahdeksi sanaksi, jotka
  linkitetään toisiinsa molempiin suuntiin.
- **Päällekkäisyys**: sama sana useassa luvussa näkyy Teoriassa joka paikassa,
  mutta kortteja tehdään vain ensimmäisestä.

Sisennetty rivi tulkitaan esimerkiksi, jos siinä on yhtäsuuruusmerkki. Jos
haluat sen huomioksi, aloita rivi sanalla `Huomaa:`, `Vrt.`, `Sääntö:`,
`Verbi:`, `Muistisääntö:` tai muulla `HUOMION_ALUT`-listan sanalla.

## Skrivtavla – uusien sanojen välivarasto

Lähteen ensimmäinen luku `Skrivtavla` on tyhjä välivarasto. Liitä sinne uudet
sanat OneNotesta missä muodossa tahansa, ja pyydä minua luokittelemaan ne:
ne siirretään oikeisiin lukuihin ja Skrivtavla tyhjennetään taas.

## Varmuuskopiot ja omat sanat

Asetuksissa on oma näkymänsä (**Asetukset → Varmuuskopiot ja omat sanat**):

- **Vie edistyminen** – tiedostona tai kopioitavana tekstinä. Edistyminen elää
  vain selaimen `localStorage`ssa ja katoaa selaimen tietoja tyhjentäessä.
- **Palauta varmuuskopiosta** – liitetystä tekstistä tai tiedostosta.
- **Lisää sanoja JSONilla** – liitä ja paina *Sijoita sanastoon*.
- **Peru viimeisin lisäys** – nappi ilmestyy liittämislaatikon alle heti
  lisäyksen jälkeen ja poistaa koko erän kerralla. Se katoaa, kun erä on
  peruttu tai sen sanat on poistettu yksitellen.

Sanojen lisäys hyväksyy kolme muotoa:

| Muoto | Esimerkki |
|---|---|
| Koko dokumentti | `{"luvut": [{"otsikko": "1 Verbit", "alaluvut": [...]}]}` |
| Lista sanoja | `[{"ruotsi": "en glass", "suomi": ["jäätelö"]}]` |
| Yksi sana | `{"ruotsi": "kanske", "suomi": "ehkä"}` |

Pakollisia ovat vain `ruotsi` ja `suomi`; `suomi` saa olla lista tai
pilkuilla eroteltu merkkijono. Muut kentät (`sanaluokka`, `luokka`, `suku`,
`taivutus`, `rektio`, `esimerkit`) täydentävät korttia ja harjoituksia.

**Sijoitus:** jos sanassa on `alakategoria`, joka täsmää olemassa olevaan
alalukuun, sana menee sinne – muuten lukuun **Omat sanat**. Näin
sanastodumppi-skillin tuloste menee suoraan oikeisiin lukuihin.

Omat sanat elävät `localStorage`ssa, eivät `sanasto.json`issa, ja kulkevat
mukana varmuuskopiossa. Pysyväksi osaksi sanastoa ne saa lisäämällä ne
`lahde/sanasto.txt`:hen ja ajamalla muuntimen.

## Kategorian harjoittelu

Teoriassa jokaisen luvun ja alaluvun otsikon oikealla on **Harjoittele**-nappi
(näkyy, kun kohdassa on vähintään kolme korttikelpoista sanaa). Siitä avautuu
koko ruudun valinta, jossa on neljä tapaa:

| Tapa | Suunta | Mitä tekee |
|---|---|---|
| **Flashcards** | molemmat | Näytä vastaus, arvioi itse osasitko |
| **Kirjoita ruotsiksi** | suomi → ruotsi | Kirjoitettu vastaus, tarkistus |
| **Kirjoita suomeksi** | ruotsi → suomi | Kirjoitettu vastaus, tarkistus |
| **Monivalinta** | molemmat | Neljä vaihtoehtoa 2×2-ruudukossa |

Kategoriaharjoittelu on **vapaata**: se ei muuta välitoiston aikataulua sanoilla,
joita ei ole vielä opittu Opi-välilehdellä. Jo valmistuneilla korteilla arvio
otetaan normaalisti huomioon. Virheet kirjautuvat aina virhelokiin.

## Lukurakenne

| Luku | Sisältö | Kortteja |
|---|---|---|
| Skrivtavla | Välivarasto uusille sanoille | – |
| 1–6 | Verbit, substantiivit, adjektiivit, ilmaukset, sidesanat, prepositiot | kyllä |
| 7 Kielioppisäännöt | Pronominit, vertailumuodot, adjektiivi + substantiivi, sanajärjestys, taivutusluokat, deklinaatiot | **ei** |
| 8 Pienet kielioppiknopit | Yksittäiset säännöt: apuverbi + infinitiivi, X av Y, adjektiivista adverbi, välkommen/välkomna, pronominien objektimuodot | ei |
| 9 Muistilista ja tehtävät | Omat muistiinpanot opiskeltavasta | ei |

Luku 7 on **luettavaa teoriaa**, ei korttiharjoittelua: `kelpaaKortiksi`
sulkee pois luvut, joiden otsikko alkaa `7 `. Luvun 94 sanariviä näkyvät
Teoriassa ja löytyvät haulla, mutta niistä ei synny kortteja eivätkä ne
päädy harjoituspooleihin. Jos jokin luvun 7 sana halutaan korteiksi, se
lisätään erikseen lukuun 1–6.

## Kehitys

`fetch` ei toimi `file://`-osoitteesta, joten sivu avataan palvelimen kautta:

```bash
python3 -m http.server 8777 --directory "/Users/kalletaskinen/Kallen paikallinen kansio/Ruotsin sanasto"
```

## Ulkoasu

Yksi ainoa tiedosto, ei riippuvuuksia, ei build-vaihetta. Tumma ja vaalea teema
seuraavat järjestelmän asetusta.

**Siniset** kantavat käyttöliittymän. Kirkas `#1e96fc` on pintaa – edistyspalkki,
valittu välilehti, tarkennuskehä – koska se jää valkoista vasten alle luettavan
kontrastin. Syvä `#00509d` ja `#003f88` kantavat tekstin ja painikkeiden täytöt.
Vaalea `#a2d6f9` on tumman teeman korostusteksti.

Tausta on laivastonsininen (`#04203f` tummana, `#f1f5fb` vaaleana), ja
painikkeen täyttö vaihtuu teeman mukana: vaalealla `#003f88` valkoisella
tekstillä, tummalla `#1e96fc` tummansinisellä tekstillä. Molemmat yltävät
luettavaan kontrastiin, kumpikaan suunta yksinään ei yltäisi.

**Keltainen** `#ffc600` on huomioväri: hakuosumat, lukumääräpillerit,
kertausmerkki alapalkissa ja "melkein oikein" -palaute.

**Sanaluokilla on omat värinsä.** Niitä käytetään vain pintoina – laattoina,
pisteinä ja lippuina – ei koskaan tekstin värinä, koska useimmat niistä eivät
yllä luettavaan kontrastiin.

| Sanaluokka | Väri |
|---|---|
| verbi | `#82e1df` |
| substantiivi | `#a486d5` |
| adjektiivi | `#fa442a` |
| adverbi | `#6fcf5f` |
| prepositio | `#ff65b3` |
| ilmaus | `#ffc600` |

Luvun tunnusväri tulee luvun **aiheesta**, ei sen sanojen enemmistöstä: luvun 6
sanat ovat sanaluokaltaan kaikkea, mutta luku on prepositioita. Ks. `LUKUVARIT`.

## Liike

Liikettä on vähän ja se on perusteltua. Kortti vaihtuu välittömästi – istunnossa
on 20–35 korttia, ja siirtymä kortista korttiin tekisi siitä hitaan.

- **Jousi-luokka** (`vaimennus`, `vaste`) hoitaa kaiken keskeytettävän liikkeen.
  Vaimennus 1.0 on oletus: ylitystä käytetään vain, kun eleessä itsessään oli
  liike-energiaa.
- **Vastauslomake** pitää toimintonapin paikallaan: kenttä ja palaute jakavat
  saman ruudun, ja nappi vaihtaa vain nimensä. Nappi on lukossa 320 ms, jottei
  pohjaan jäänyt Enter ohita palautetta.
- **Asetuslevyn** voi vetää kiinni. Veto seuraa sormea 1:1, ylärajalla on
  kumilenkki, ja heiton lepopiste projisoidaan nopeudesta.
- `prefers-reduced-motion` korvaa siirtymät häivytyksillä, ei poista palautetta.

## Asetukset

Asetuslevy avautuu ylärivin rattaasta. Siellä on harjoittelun rajaus luvuittain
tai sanaluokittain, **taivutusluokan piilotus** (taivutustreeni ilman kaavan
paljastavaa I/IIb/3/5-merkintää), ääntämisnappi, edistymisen vienti ja tuonti,
vaikeat sanat, virheloki ja nollaus.

## Ikoni

Kotinäytön ikoni tehdään yhdestä lähdekuvasta:

```bash
sh "tyokalut/tee_ikonit.sh"
```

Skripti lukee `ikoni-lahde.png`:n ja tekee kaikki koot. Lähdekuvan on oltava
**neliö, jossa ikoni ulottuu reunoihin asti** – iOS lisää oman pyöristyksensä
ja varjonsa, joten kuvassa ei saa olla omaa kehystä tai marginaalia.

> **Safari välimuistittaa kotinäytön ikonin tiedostonimen mukaan** eikä huomaa
> sisällön muuttumista. Kun ikoni vaihdetaan, nosta versionumero (`v1` → `v2`)
> skriptissä, `index.html`:ssä ja `manifest.webmanifest`-tiedostossa.

## Ääntäminen

Ruotsin ääntäminen kaatuu neljästä eri syystä, ja kaikki neljä on hoidettu:

1. **Pelkkä `lang: "sv-SE"`** antaa selaimen valita oletusäänen, joka on tällä
   koneella suomalainen (Satu). Ääni haetaan nimeltä.
2. **`cancel()` ja `speak()` samalla tikillä** – WebKit pudottaa uuden lausuman
   äänivalinnan. Uusi lausuma siirretään omalle tikilleen.
3. **`lang`, joka ei täsmää valitun äänen kanssa** – `lang` asetetaan äänen omasta
   `lang`-kentästä, ei kovakoodattuna.
4. **Äänilista, joka ei ollut valmis sivun latautuessa** – ääni haetaan uudestaan
   jokaisella puhekerralla, ei vain käynnistyksessä.

Asetuksissa voi valita äänen, jos niitä on useampi, ja kokeilla sitä napista.
Jos ruotsin ääntä ei ole lainkaan, asetukset kertoo mistä sen asentaa.

## Tilanne

Rakennusjärjestys on `SPEC.md` luvussa 9.

- [x] 1 `sanasto.json` – tietomalli
- [x] 2 Teoria-välilehti – JSON renderöitynä
- [x] 3 Alapalkki ja välilehtinavigaatio
- [x] Skrivtavlan 7.9.2026 erä luokiteltu (32 uutta sanaa, 11 päällekkäistä)
- [x] 4 Kortti-UI
- [x] 5 Välitoisto (SM-2) ja edistymisen tallennus
- [x] 6 Molemmat suunnat erillisinä kortteina
- [x] 7 Learn-tila: vaiheet, erälogiikka, häiriövaihtoehdot
- [x] 8 Teorian haku ja lukunavigaatio
- [x] 9 Taivutustreeni
- [x] 10 Vie/tuo edistyminen
- [x] 11 Kategoriasuodatin, "harjoittele tämä luku", osaamismerkit
- [x] 12 Rektio- ja prepositioharjoitukset
- [x] 13 Ääntäminen, leech-tunnistus, virheloki, istunnon pituus

Rakentamatta jäi tarkoituksella se, mitä `SPEC.md` luvussa 7 kielletään:
tunnukset, palvelin, pisteet ja sarjat, monivalinta kertauksessa.
