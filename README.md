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

Rivin ensimmäinen merkki kertoo tyypin:

| Merkki | Muoto | Esimerkki |
|---|---|---|
| `#` `##` `###` | luku, alaluku, väliotsikko | `## 1.1 Ajattelu` |
| `p` | kappale | `p Taivutusluokat: …` |
| `*` | sana taivutuksineen: `ruotsi\|luokka\|suomi` | `* tycka, tycker, tyckte, tyckt\|IIb\|olla jotain mieltä` |
| `=` | ilmaus ilman taivutusta: `ruotsi\|suomi` | `= tänka på ngt\|ajatella jotakin` |
| `>` | esimerkki, `sv = fi`, useampi erotettuna ` / ` | `> Menar du allvar? = Oletko tosissasi?` |
| `!` | korjaus muistiinpanoihin (punainen) | `! "Värdesetta" – oikea muoto on värdesätta` |
| `~` | huomio (harmaa) | `~ Vrt. adjektiivi verklig = todellinen` |

Muuntimen päättelemät asiat:

- **Sanaluokka** tulee `en`/`ett`-alusta, taivutusluokasta tai luvun otsikosta.
- **Rektio** tulee sulkeista (`klaga (på/över)`) tai luvun 6.3–6.6 ilmauksista.
- **Vastakohta** syntyy `↔`-merkistä: rivi jaetaan kahdeksi sanaksi, jotka
  linkitetään toisiinsa molempiin suuntiin.
- **Päällekkäisyys**: sama sana useassa luvussa (esim. `lycka`-pesue luvussa 8)
  näkyy Teoriassa joka paikassa, mutta kortteja tehdään vain ensimmäisestä.

## Kehitys

`fetch` ei toimi `file://`-osoitteesta, joten sivu avataan palvelimen kautta:

```bash
python3 -m http.server 8777 --directory "/Users/kalletaskinen/Kallen paikallinen kansio/Ruotsin sanasto"
```

## Tilanne

Rakennusjärjestys on `SPEC.md` luvussa 9.

- [x] 1 `sanasto.json` – tietomalli
- [x] 2 Teoria-välilehti – JSON renderöitynä
- [x] 3 Alapalkki ja välilehtinavigaatio
- [ ] 4 Kortti-UI
- [ ] 5 Välitoisto ja edistymisen tallennus
- [ ] 6 Molemmat suunnat erillisinä kortteina
- [ ] 7 Learn-tila
- [ ] 8 Teorian haku ja lukunavigaatio
- [ ] 9 Taivutustreeni
- [ ] 10 Vie/tuo edistyminen
