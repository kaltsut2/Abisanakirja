# Ruotsin sanasto

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

## Ääntäminen

Pelkkä `lang: "sv-SE"` ei riitä – ilman nimettyä ääntä selain lausuu ruotsin
suomalaisittain. Sovellus hakee ruotsinkielisen äänen erikseen ja kertoo
asetuksissa, jos sitä ei ole asennettuna.

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
