# Ruotsin sanaston opiskelusovellus – määrittely

Tämä tiedosto on konteksti Claude Codelle. Se kuvaa mitä rakennetaan, missä
järjestyksessä ja mitä *ei* rakenneta.

## Tavoite

Sovellus, jolla yksi käyttäjä opiskelee ruotsin sanastoa keskipitkän ruotsin
ylioppilaskoetta (B1) varten. Ei monikäyttäjätuotetta, ei julkaistavaa palvelua.

Lähdeaineisto on olemassa oleva sanasto, jossa on noin 400 sanaa ja ilmausta:
kaikki taivutusmuodot, taivutusluokka, aihepiirikategoria, vastakohtaparit,
verbi-/adjektiivi-/substantiivirektiot sekä esimerkkilauseita.

---

## 1. Tietomalli — tee tämä ensin

Sanasto asuu **erillisessä JSON-tiedostossa**, ei koodin sisällä. Tämä on koko
projektin tärkein ratkaisu: jos rakenne on kunnossa, jokainen harjoitustyyppi
syntyy samasta datasta. Jos ei, sanasto pitää kirjoittaa uudestaan joka kerta
kun keksitään uusi harjoitusmuoto.

```jsonc
{
  "id": "undvika",
  "sanaluokka": "verbi",          // verbi | substantiivi | adjektiivi | adverbi | ilmaus
  "ruotsi": "undvika",
  "suomi": ["välttää"],           // aina lista – synonyymit hyväksytään vastauksina
  "taivutus": ["undviker", "undvek", "undvikit"],
  "luokka": "IV",                 // verbeillä I/IIa/IIb/III/IV, substantiiveilla 1–5
  "suku": null,                   // substantiiveilla "en" | "ett"
  "kategoria": "Verbit",
  "alakategoria": "Muutos, vaikuttaminen ja seuraukset",
  "vastakohta": null,             // toisen sanan id
  "rektio": null,                 // esim. "av", "för", "på"
  "esimerkit": [
    { "sv": "Han undvek att svara.", "fi": "Hän vältti vastaamasta." }
  ],
  "muistiinpano": null
}
```

### Yksi lähde, ei kahta

Sanasto ei ole pelkkä lista kortteja. Alkuperäisessä aineistossa on myös
kielioppisääntöjä, prepositio-ohjeita, sanapesueita ja korjausmerkintöjä —
sisältöä, josta ei synny korttia mutta joka pitää päästä lukemaan
(ks. luku 4, Teoria-välilehti).

Älä tee tästä kahta tiedostoa. `sanasto.json` on **lukurakenne**, ja kortit
johdetaan siitä:

```jsonc
{
  "luvut": [{
    "otsikko": "1 Verbit",
    "alaluvut": [{
      "otsikko": "1.6 Muutos, vaikuttaminen ja seuraukset",
      "sisalto": [
        { "tyyppi": "sana", "ruotsi": "undvika", ... },
        { "tyyppi": "teksti", "teksti": "Näissä pareissa kannattaa…" },
        { "tyyppi": "korjaus", "teksti": "\"förbättre\" → förbättra" },
        { "tyyppi": "huomio", "teksti": "Vrt. adjektiivi verklig…" }
      ]
    }]
  }]
}
```

Kortit generoidaan käynnistyksessä: jokainen `tyyppi: "sana"`, jolla on sekä
`ruotsi` että `suomi`, muuttuu kahdeksi kortiksi. `teksti`, `korjaus` ja
`huomio` näkyvät vain Teoria-välilehdellä.

Näin sanan korjaaminen yhdessä paikassa korjaa sekä kortin että teorian, eikä
kahta versiota pääse syntymään.

Huomioita:

- `suomi` on lista, koska monella sanalla on useampi hyväksyttävä käännös
  (`märka` = huomata / havaita). Tuottavassa suunnassa mikä tahansa niistä
  kelpaa.
- `taivutus` sisältää vain perusmuodon jälkeiset muodot. Verbeillä 3
  (preesens, imperfekti, supiini), substantiiveilla 3 (yks. määräinen, mon.
  epämääräinen, mon. määräinen), adjektiiveilla 2 (ett-muoto, monikko).
- `vastakohta` on kaksisuuntainen: jos A osoittaa B:hen, B osoittaa A:han.
- Deponenttiverbit (`lyckas`, `umgås`) merkitään luokalla `"dep."`.

Erillinen tiedosto **edistymiselle** — sanastoa ja opiskeluhistoriaa ei
sekoiteta keskenään. Edistyminen elää `localStorage`issa, sanasto ei.

Edistymismerkintä on korttikohtainen, ei sanakohtainen. Yhdestä sanasta
syntyy kaksi korttia (suunnat, ks. 2.2), ja kummallakin on oma tilansa:

```jsonc
{
  "cardId": "undvika:fi→sv",
  "stage": 3,           // 0–4 Learn-tilassa, null kun valmistunut
  "graduated": false,   // true = siirtynyt välitoistoon
  "interval": 0, "easeFactor": 2.5, "repetitions": 0,
  "nextReview": null, "lapses": 0
}
```

---

## 2. Ydintoiminnot

Nämä neljä ovat vaatimuksia. Ilman niitä sovellusta ei kannata rakentaa.

### 2.1 Välitoisto (spaced repetition)

Ainoa ominaisuus, joka oikeasti ratkaisee muistamisen. Toteuta **FSRS** tai
**SM-2**; molemmat mahtuvat noin 50 riviin. Sana palaa kertaukseen sitä
harvemmin, mitä paremmin se menee.

Tallenna jokaisesta kortista: `interval`, `easeFactor`, `repetitions`,
`nextReview`, `lapses`.

### 2.2 Suunnat erikseen

`ruotsi → suomi` on tunnistamista ja helppoa.
`suomi → ruotsi` on tuottamista, ja juuri sitä ylioppilaskoe vaatii.

Nämä ovat **kaksi eri korttia samasta sanasta**, omilla välitoistotiedoillaan.
Sama sana voi olla hallussa toiseen suuntaan ja hukassa toiseen.

### 2.3 Vastaus kirjoittamalla

Kirjoittaminen on **oletus kaikelle kertaukselle**. Monivalinta antaa väärän
tunteen osaamisesta, eikä se harjoita tuottamista, jota koe vaatii.

Poikkeus: uusi, täysin tuntematon sana. Silloin monivalinta toimii
väliaikaisena tukena — ks. luku 3, Learn-tila. Kun sana on kertaalleen
läpäissyt Learn-vaiheet, se ei enää koskaan palaa monivalintaan.

Vertailussa:

- jätä huomiotta isot/pienet kirjaimet ja ylimääräiset välilyönnit
- **älä** hyväksy `a`/`o` kun oikea on `å`/`ä`/`ö` — näytä sen sijaan erillinen
  huomautus ("oikein muuten, mutta tarkista ä/ö")
- artikkeli (`en`/`ett`) tarkistetaan, jos se on osa vastausta

### 2.4 Taivutustreeni omana harjoitustyyppinään

Näytä `undvika (IV)`, pyydä kaikki puuttuvat muodot omiin kenttiinsä.
Substantiiveilla neljä muotoa, adjektiiveilla kolme.

Tämä on se osa, jonka useimmat sovellukset jättävät tekemättä ja joka tuottaa
eniten pisteitä kokeessa.

---

## 3. Learn-tila — uuden sanan sisäänajo

Välitoisto (2.1) hoitaa **kertauksen**: sanat, jotka on jo joskus osattu.
Se ei hoida ensikohtaamista. Täysin tuntematonta sanaa on turha kysyä
kirjoittamalla — vastaus on aina tyhjä, ja kortti kiertää turhaan.

Learn-tila on erillinen putki, jonka läpi jokainen uusi sana kulkee kerran.
Sama pieni sanajoukko toistuu nopeasti peräkkäin, vaikeutuva askel kerrallaan,
niin että sanat ehtivät kiinnittyä työmuistiin ennen kuin ne siirtyvät
välitoistoon.

### 3.1 Vaiheet

Kortilla on `stage`-kenttä, 0–4:

| Vaihe | Tehtävä | Tarkoitus |
|---|---|---|
| **0** | Esittely: näytä `ruotsi + suomi + taivutus`, ei arvausta. Nappi "seuraava". | Ensikohtaaminen |
| **1** | Monivalinta `ruotsi → suomi`, 4 vaihtoehtoa | Tunnistaminen |
| **2** | Monivalinta `suomi → ruotsi`, 4 vaihtoehtoa | Suunnan kääntö |
| **3** | Kirjoittaminen `ruotsi → suomi` | Palautus muistista |
| **4** | Kirjoittaminen `suomi → ruotsi` | Tuottaminen — kokeen taso |

Vaiheen 4 läpäisyn jälkeen sana **valmistuu** ja siirtyy välitoiston piiriin
(2.1). Sen jälkeen se ei enää palaa Learn-tilaan eikä monivalintaan, vaikka
menisi myöhemmin väärin.

### 3.2 Etenemissäännöt

- Oikein → `stage + 1`
- Väärin → `stage − 1`, ei koskaan alle 1 (vaiheeseen 0 ei palata)
- Kaksi peräkkäistä väärin samassa vaiheessa → näytä vastaus vaiheen 0
  tyyliin, säilytä `stage` ennallaan

### 3.3 Erä ja rytmitys

Learn-tila toimii **erissä, ei jonona**. Yksi erä = 7 uutta sanaa.

- Erän sanoja kysellään vuorotellen, kunnes kaikki 7 ovat vaiheessa 4
- **Samaa sanaa ei kysytä kahdesti peräkkäin** — väliin vähintään 2 muuta
- Kun erä on valmis, tarjoa seuraavaa erää tai paluuta kertaukseen

Seitsemän on tässä olennaista: se on suunnilleen työmuistin kapasiteetti.
Isommalla erällä alkupään sanat ehtivät unohtua ennen kuin ne palaavat, ja
tila muuttuu tehottomaksi.

### 3.4 Häiriövaihtoehdot (distractors)

Monivalinnan laatu ratkeaa vääristä vastausvaihtoehdoista. Poimi ne
järjestyksessä:

1. saman `alakategoria`n sanat
2. jos ei riitä, saman `kategoria`n sanat
3. jos ei vieläkään, sama `sanaluokka`

Kolme vaihtoehtoa neljästä on siis samaa aihepiiriä ja sanaluokkaa. Jos
vaihtoehdot poimitaan satunnaisesti koko sanastosta, oikean tunnistaa
arvaamalla eikä tehtävä opeta mitään.

Sanan `vastakohta` on erityisen hyvä häiriövaihtoehto — se pakottaa erottamaan
`rättvis`/`orättvis`-tyyppiset parit toisistaan.

---

## 4. Sovelluksen rakenne ja navigaatio

Alapalkissa neljä välilehteä. Tila säilyy välilehteä vaihdettaessa: kesken
jäänyt istunto jatkuu siitä mihin se jäi.

| Välilehti | Sisältö |
|---|---|
| **Opi** | Learn-tila (luku 3) — uudet sanat, erä kerrallaan |
| **Kertaa** | Välitoisto (2.1) — tänään erääntyvät kortit |
| **Harjoitukset** | Taivutustreeni, rektiot, prepositiot, vastakohdat (luku 5) |
| **Teoria** | Koko sanasto luettavana sellaisenaan |

### 4.1 Teoria-välilehti

Koko `sanasto.json` renderöitynä alkuperäisessä järjestyksessään: luvut,
väliotsikot, sanat taivutuksineen, esimerkkilauseet, huomiot ja korjaukset.
Sama sisältö kuin Word-dokumentissa, mutta selattavana ja haettavana.

Tämä ei ole toissijainen "lisäsivu". Iso osa aineistosta — kielioppisäännöt,
prepositio-ohjeet, `lycka`-sanapesue, sidosteisuussanat — ei taivu
korttimuotoon lainkaan, ja Teoria on ainoa paikka jossa se on olemassa.

**Vaatimukset:**

- **Haku** on tärkein yksittäinen toiminto. Hakee sekä ruotsista että
  suomesta, osumat korostettuna. Tähän palataan kesken harjoittelun, kun
  jokin sana ei muistu mieleen.
- **Lukunavigaatio** — sisällysluettelo tai kokoontaitettavat luvut. 30
  sivullista sisältöä ei selata rullaamalla.
- **Korjaukset erottuvin värein**, kuten alkuperäisessä dokumentissa.
- **Osaamismerkki jokaisen sanan kohdalla** — pieni pallo tai väri, joka
  kertoo onko sana uusi, Learn-tilassa vai valmistunut. Näin selailu toimii
  samalla edistymisen yleiskuvana.
- **"Harjoittele tämä luku" -nappi** jokaisen alaluvun otsikossa. Käynnistää
  istunnon, joka on rajattu kyseiseen alalukuun. Tämä sitoo Teorian takaisin
  opiskeluun sen sijaan, että se jäisi erilliseksi lukusaliksi.
- **Linkki kortista teoriaan** — vastauksen näytön yhteydessä pääsee
  katsomaan sanan omassa asiayhteydessään, naapurisanojen ja
  esimerkkilauseiden keskellä.

---

## 5. Ylioppilaskokeeseen tähtäävät harjoitustyypit

Rakennetaan ydintoimintojen jälkeen. Kaikki syntyvät samasta JSON-datasta.

| Harjoitus | Miten toimii | Mistä data |
|---|---|---|
| **Rektioaukot** | `Jag är rädd ___ att misslyckas.` | `rektio`-kenttä + esimerkit |
| **Prepositiotreeni** | i / på / om / för…sedan -erottelu lauseissa | prepositioluvun esimerkit |
| **Vastakohtaparit** | Näytä `rättvis`, pyydä vastakohta | `vastakohta`-kenttä |
| **Lauseesta sana** | Suomenkielinen lause → ruotsinnos | `esimerkit` |
| **en vai ett** | Nopea nappiharjoitus | `suku`-kenttä |

Rektioaukot ja prepositiotreeni ovat käytännössä yo-kokeen aukkotehtävä
sellaisenaan — sanastossa on jo noin 80 rektiota valmiina.

---

## 6. Lisättävää, kun perusta toimii

Prioriteettijärjestyksessä:

1. **Kategoriasuodatin** — "vain verbit", "vain hyvinvointisanasto"
2. **Vie/tuo edistyminen JSON-tiedostona** — ks. varoitus kohdassa 6
3. **Ääntäminen** — selaimen `SpeechSynthesis`, `lang: "sv-SE"`, ilmainen,
   käytännössä yksi rivi koodia
4. **Leech-tunnistus** — sana joka on mennyt väärin 5+ kertaa nostetaan esiin
   erikseen; se pitää yleensä opetella eri tavalla, ei vain toistaa useammin
5. **Virheloki** — mitä kirjoitit vs. mikä oli oikein, jotta toistuvat
   virhetyypit näkyvät (ö/o, en/ett, väärä taivutusluokka)
6. **Istunnon pituus** — 20 korttia kerralla, ei loputonta virtaa

---

## 7. Mitä EI rakenneta

- käyttäjätilit, kirjautuminen, palvelin, tietokanta, pilvisynkronointi
- pisteet, sarjat (streak), saavutusmerkit, tasot — siirtävät huomion
  opiskelusta pelaamiseen
- monivalinta kertauksessa. Monivalinta on olemassa **vain** Learn-tilan
  vaiheissa 1–2 (luku 3). Valmistunut sana kysytään aina kirjoittamalla.
- mobiilisovellus tai asennuspaketti

---

## 8. Tekniset reunaehdot

- **Yksi HTML-tiedosto** + erillinen `sanasto.json`. Ei build-vaihetta, ei
  npm-riippuvuuksia, ei bundleria.
- Tila `localStorage`issa. Toimii offline ja lentokoneessa.
- Toimii puhelimen selaimessa — vastauskentät ja napit riittävän isoiksi.
- Tumma ja vaalea teema `prefers-color-scheme`n mukaan.

> **Varoitus:** `localStorage` katoaa, jos selaimen tiedot tyhjennetään tai
> käytetään yksityistä ikkunaa. Tee **vie/tuo edistyminen** -nappi heti
> ensimmäisten ominaisuuksien joukossa, älä myöhemmin.

---

## 9. Rakennusjärjestys

1. `sanasto.json` — sanasto lukurakenteeksi, tämä ensin
2. **Teoria-välilehti** — renderöi JSON sellaisenaan, ilman hakua
3. Alapalkki ja välilehtinavigaatio
4. Kortti-UI: näytä kysymys, ota vastaus, kerro oikein/väärin
5. Välitoistoalgoritmi ja edistymisen tallennus
6. Molemmat suunnat erillisinä kortteina
7. **Learn-tila** (luku 3) — vaiheet, erälogiikka, häiriövaihtoehdot
8. Teorian haku ja lukunavigaatio
9. Taivutustreeni
10. Vie/tuo edistyminen
11. Kategoriasuodatin, "harjoittele tämä luku", osaamismerkit
12. Rektio- ja prepositioharjoitukset
13. Loput luvusta 6 sitä mukaa kun huomaa mitä oikeasti käyttää

Teoria on toisena tarkoituksella. Se on koko sovelluksen yksinkertaisin osa —
pelkkä JSON:in renderöinti — ja se paljastaa heti, onko tietomalli oikein.
Jos teoria näyttää alkuperäiseltä dokumentilta, rakenne kestää; jos jotain
puuttuu, se korjataan ennen kuin sen päälle on rakennettu mitään.

Learn-tila tulee vasta seitsemäntenä: se riippuu kortti-UI:sta ja edistymisen
tallennuksesta, ja erälogiikka on helpompi rakentaa kun peruskortti toimii.
