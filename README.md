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

## Tilanne

Rakennusjärjestys on `SPEC.md` luvussa 9.

- [x] 1 `sanasto.json` – tietomalli
- [x] 2 Teoria-välilehti – JSON renderöitynä
- [x] 3 Alapalkki ja välilehtinavigaatio
- [x] Skrivtavlan 7.9.2026 erä luokiteltu (32 uutta sanaa, 11 päällekkäistä)
- [ ] 4 Kortti-UI
- [ ] 5 Välitoisto ja edistymisen tallennus
- [ ] 6 Molemmat suunnat erillisinä kortteina
- [ ] 7 Learn-tila
- [ ] 8 Teorian haku ja lukunavigaatio
- [ ] 9 Taivutustreeni
- [ ] 10 Vie/tuo edistyminen
