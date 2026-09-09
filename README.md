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
| **Flashcards** | valittava | Näytä vastaus, arvioi itse osasitko |
| **Kirjoita ruotsiksi** | kiinteä: suomi → ruotsi | Kirjoitettu vastaus, tarkistus |
| **Kirjoita suomeksi** | kiinteä: ruotsi → suomi | Kirjoitettu vastaus, tarkistus |
| **Monivalinta** | valittava | Neljä vaihtoehtoa 2×2-ruudukossa |

Valinnan yläreunassa on **suuntanappi**: *Molemmat · FI → SV · SV → FI*. Se
ohjaa flashcardeja ja monivalintaa; kirjoitustiloilla suunta on osa niiden
nimeä eikä muutu. Sen näkee laatasta: flashcardin ja monivalinnan selite
kertoo aina valitun suunnan, kirjoitustilojen selite oman kiinteän suuntansa.
Valinta säilyy `localStorage`ssa.

Kategoriaharjoittelu on **vapaata**: se ei muuta välitoiston aikataulua sanoilla,
joita ei ole vielä opittu Opi-välilehdellä. Jo valmistuneilla korteilla arvio
otetaan normaalisti huomioon. Virheet kirjautuvat aina virhelokiin.

## Koko taivutuksen hyväksyminen

Suomesta ruotsiin kirjoitettaessa hyväksytään perusmuodon lisäksi **koko
taivutus pilkuilla tai välilyönnein eroteltuna**, oikeassa järjestyksessä:
`pratsam` ja `pratsam, pratsamt, pratsamma` kelpaavat molemmat. Koskee kaikkia
sanaluokkia – substantiivilla myös artikkelin kanssa (`en man, mannen, män,
männen`), mutta väärä artikkeli hylätään edelleen. Väärä järjestys ei kelpaa,
koska silloin ei voi enää päätellä, tunteeko kirjoittaja muotojen merkityksen
vai on vain toistanut ne oikeassa muistijärjestyksessä.

## Teorian navigointi

**Avattava sisällysluettelo.** Teorian yläreunan luettelossa jokainen luku,
jolla on useampi alaluku, avautuu napauttamalla ja näyttää alalukunsa
sanamäärineen. Alaluvun valinta sulkee valikon ja vierittää kohtaan. Valikko
suljetaan **ennen** vieritystä, koska luettelon kutistuminen siirtäisi kohdetta
muuten kesken hypyn.

**Ristiviittaukset ovat linkkejä.** Teoriatekstissä oleva luku- tai
alalukunumero ("ks. 7.4", "sanalista on luvussa 5.2") muuttuu automaattisesti
klikattavaksi. Linkit rakennetaan `lukuAnkkurit`-kartasta, joka kootaan
sanastosta joka latauksella: viittaus muuttuu linkiksi vain jos kohde on
oikeasti olemassa, joten lukuja voi numeroida uudestaan ilman että linkit jäävät
osoittamaan tyhjään. Jos haku on päällä, se tyhjennetään ensin – muuten kohde
ei olisi piirrettynä.

Pitkillä matkoilla vieritys on välitön ja lyhyillä pehmeä: teoria on
kymmeniätuhansia pikseleitä pitkä, ja 95 000 pikselin pehmeä vieritys olisi
pelkkää odottamista.

## Työnjako: luku 7 opettaa, luvut 3 ja 5 harjoituttavat

Luku 7 ei tuota kortteja, joten sinne ei kannata kirjoittaa sanalistoja.
Konjunktiot ja liikkuvat määreet on siksi jaettu kahtia:

| Sisältö | Missä | Miksi |
|---|---|---|
| Konjunktioiden sanalistat | 5.2 Rinnastuskonjunktiot, 5.3 Parikonjunktiot, 5.4 Alistuskonjunktiot, 5.5 Relatiivisanat | kortteja ja harjoituksia |
| Liikkuvien määreiden sanalista | 3.7 Lauseadverbit | kortteja ja harjoituksia |
| Erot, käyttökohteet ja lauserakenne | 7.5, 7.6, 7.7 | luettavaa teoriaa |

Samaa asiaa ei opeteta kahdesti. Kun luvun 7 teoriaan lisätään sivulauseen
kaava KON – SU – KIE – PRE, relatiivilause ja epäsuora kysymyslause siirtyivät
luvusta 7.4 sen alle (7.6), koska ne ovat saman kaavan sovelluksia – muuten
som, vilket, där ja dit olisi selitetty kahdessa peräkkäisessä alaluvussa.

Kun sana kuuluu useaan ryhmään, se on sanastossa kerran ja muut roolit
mainitaan huomiona: `då` on konjunktio luvussa 5.4, mutta relatiivisanana
(jolloin) ja liikkuvana määreenä (silloin) se on vain mainittuna. Sama koskee
`för`-sanaa: rinnastuskonjunktiona (sillä) se on 5.2:ssa ja saa kortit,
prepositiona se on yhä luettavissa luvussa 6.9.

## Sanamäärän valinta

Tapavalinnassa on **MÄÄRÄ**-valitsin ennen suuntaa: **10 · 20 · Kaikki (N)**.
Se rajaa sanoja, ei kortteja – "10" tarkoittaa kymmentä sanaa, vaikka
Flashcards ja Monivalinta molemmat-suunnalla tuottavat niistä 20 korttia.
Valitut sanat arvotaan joka kerta uudestaan kategorian täydestä joukosta.

Kynnys näkyy vain jos aihepiiri on sitä suurempi: alle 10 sanan alaluvussa
näkyy pelkkä *Kaikki (N)* eikä koko valitsinta piirretä lainkaan, koska
kolme vaihtoehtoa jotka tarkoittaisivat samaa olisi vain kohinaa. "Kaikki"
ei enää katkea kertausistunnon oletuspituuteen (20 korttia) – valinta
kunnioitetaan sellaisenaan, myös uudelleenkäynnistyksissä ("Kaikki
uudelleen", "Harjoittele väärin menneet").

## Harjoitusistunnon hallinta

**Paluunuoli** ylävasemmalla vie askeleen taaksepäin kesken harjoituksen:
istunnosta tapavalintaan, tapavalinnasta Teoriaan, harjoituksesta
harjoituslistaan, Opi-erästä erän aloitusnäkymään. Nuoli näkyy vain silloin,
kun paluukohde on olemassa.

**Väärin menneiden uusinta.** Istunto muistaa väärin menneet kortit ja
tehtävät. Yhteenvedossa on kaksi nappia: *Harjoittele väärin menneet (N)* ja
*Kaikki uudelleen*. Uusinta säilyttää istunnon asetukset – suunnan, tavan ja
sen, oliko kyseessä vapaa kategoriaharjoittelu.

**Vastauksen hyväksyminen oikeaksi.** Tarkistus ei voi tuntea kaikkia
kelvollisia käännöksiä: *jotakin* ja *jotain* ovat kumpikin oikein. Väärän
vastauksen palautteessa on nappi **Hyväksy oikeaksi**, joka

1. palauttaa kortin välitoistotilan arvostelua edeltäneeksi (tilannekuva
   otetaan ennen arvostelua),
2. arvostelee sen uudestaan oikeana,
3. poistaa merkinnän virhelokista ja väärin menneiden listalta,
4. korjaa istunnon oikein/väärin-laskurit.

Lopputulos on täsmälleen sama kuin jos vastaus olisi alun perin hyväksytty –
myös helppokerroin ja väli. Nappi näkyy vain kirjoitustiloissa; monivalinnassa
ja flashcardeissa vastaus on jo yksiselitteinen tai itse arvioitu.

## Lukurakenne

| Luku | Sisältö | Kortteja |
|---|---|---|
| Skrivtavla | Välivarasto uusille sanoille | – |
| 1–6 | Verbit, substantiivit, adjektiivit, ilmaukset, sidesanat, prepositiot | kyllä |
| 7 Kielioppisäännöt | Pronominit, vertailumuodot, adjektiivi + substantiivi, sanajärjestys, rinnastus- ja alistuskonjunktiot, liikkuvat määreet, taivutusluokat, deklinaatiot | **ei** |
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
