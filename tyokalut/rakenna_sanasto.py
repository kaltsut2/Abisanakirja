#!/usr/bin/env python3
"""Muuntaa lahde/sanasto.txt -> sanasto.json (lukurakenne, ks. SPEC.md luku 1).

Lahde on OneNotesta kopioitu teksti sellaisenaan. Muodot:

  Sivun otsikko          oma rivi, jota seuraa paivays tai alaluvun numero
  1.1 Alaluvun nimi      luku ja alaluku numeroista
  Valiotsikko            lyhyt rivi ilman erotinta
  Kappaletta selittava   pitka rivi ilman erotinta
  sana, muodot  (luokka)  -  suomi     kaksi valilyontia ajatusviivan ymparilla
  sana = suomi                          Skrivtavlan ja luvun 6.9 muoto
  <sisennys> ruotsi = suomi             esimerkki
  <sisennys> Korjaus: ...               korjaus
  <sisennys> muu teksti                 huomio
"""
import json
import re
import sys
from pathlib import Path

JUURI = Path(__file__).resolve().parent.parent
LAHDE = JUURI / "lahde" / "sanasto.txt"
KOHDE = JUURI / "sanasto.json"

OTSIKKO = "Ruotsin sanasto"
ALAOTSIKKO = "Kootut OneNote-muistiinpanot – jäsennelty sanaluokittain ja aihepiireittäin"

EROTIN = "  –  "          # kaksi valilyontia, ajatusviiva, kaksi valilyontia
VIIKONPAIVAT = ("maanantai", "tiistai", "keskiviikko", "torstai", "perjantai",
                "lauantai", "sunnuntai")
VERBILUOKAT = {"I", "IIa", "IIb", "III", "IV", "dep.", "dep. IIa", "I / IV"}
ADJLUOKAT = {"adj.", "part.", "taipumaton", "adj. (taipumaton)", "adj. (puhek.)"}
SUBSTLUOKAT = {"1", "2", "3", "4", "5", "epäsäänn.", "adj.subst.", "mon."}
PREPOSITIOT = {
    "på", "för", "till", "av", "med", "om", "efter", "från", "mot", "över",
    "åt", "i", "hos", "genom", "under", "vid", "inför", "utan", "trots",
}
SANALUOKKA_POIKKEUS = {"förbättra": "verbi", "försämra": "verbi"}
VALIOTSIKON_RAJA = 60     # tata pidempi rivi ilman erotinta on kappale, ei otsikko
# Sisennetyt rivit, jotka alkavat naista, ovat huomioita eivatka esimerkkeja,
# vaikka niissa olisi yhtasuuruusmerkki.
HUOMION_ALUT = ("Muistisääntö", "Muistiinpanoissa", "Huomaa", "Huom.", "Vrt.",
                "Sääntö", "Johdos", "Johdokset", "Adjektiivi", "Verbi",
                "Muodostuu", "Etuliite", "Prepositio", "Vuosiluku",
                "Kellonajassa", "Vastakohtapari", "Sama pätee")

varoitukset = []


def jaa_pilkuilla(teksti):
    """Jakaa pilkuista ja puolipisteista, mutta ei sulkeiden sisalta."""
    osat, nyk, syvyys = [], [], 0
    for merkki in teksti:
        if merkki == "(":
            syvyys += 1
        elif merkki == ")":
            syvyys = max(0, syvyys - 1)
        if merkki in ",;" and syvyys == 0:
            osat.append("".join(nyk).strip())
            nyk = []
        else:
            nyk.append(merkki)
    osat.append("".join(nyk).strip())
    return [o for o in osat if o]


def irrota_loppusulut(teksti):
    """Palauttaa (teksti ilman loppusulkuja, sulkujen sisalto tai None)."""
    teksti = teksti.rstrip()
    if not teksti.endswith(")"):
        return teksti, None
    syvyys = 0
    for i in range(len(teksti) - 1, -1, -1):
        if teksti[i] == ")":
            syvyys += 1
        elif teksti[i] == "(":
            syvyys -= 1
            if syvyys == 0:
                return teksti[:i].rstrip(), teksti[i + 1:-1].strip()
    return teksti, None


def erota_luokka(ruotsi_raaka):
    """Erottaa lopun suluista taivutusluokan. Taivutusmuodot jaavat sanaan."""
    runko, sulut = irrota_loppusulut(ruotsi_raaka)
    if sulut is None:
        return ruotsi_raaka.strip(), None
    if "," in sulut and sulut not in ADJLUOKAT:
        return ruotsi_raaka.strip(), None      # (står, stod, stått) = taivutus
    if sulut in {"–", "-", ""}:
        return runko, None
    return runko, sulut


def tee_tunnus(ruotsi, kaytetyt):
    perus = re.sub(r"[^0-9a-zåäöéü]+", "-", ruotsi.lower()).strip("-") or "sana"
    tunnus, n = perus, 2
    while tunnus in kaytetyt:
        tunnus = f"{perus}-{n}"
        n += 1
    kaytetyt.add(tunnus)
    return tunnus


def jaa_muodot(ruotsi_raaka):
    """Palauttaa (perusmuoto, [taivutusmuodot], suku)."""
    teksti = ruotsi_raaka.strip()
    suku = None
    osui = re.match(r"^(en|ett)\s+(.*)$", teksti)
    if osui:
        suku, teksti = osui.group(1), osui.group(2)
    if "→" in teksti or "↔" in teksti:
        return teksti, [], suku          # johdospari tai vastakohta: ei jaeta
    osat = jaa_pilkuilla(teksti)
    return osat[0], osat[1:], suku


def poimi_rektio(perusmuoto):
    """Erottaa perusmuodosta sulkeissa olevan rektion: klaga (på/över)."""
    runko, sulut = irrota_loppusulut(perusmuoto)
    if sulut is None:
        return perusmuoto, None
    palat = [p.strip() for p in re.split(r"[/,]", sulut)]
    if palat and all(p in PREPOSITIOT for p in palat):
        return runko, "/".join(palat)
    return perusmuoto, None


def paattele_sanaluokka(luokka, suku, ctx):
    if luokka in VERBILUOKAT:
        return "verbi"
    if luokka == "adv.":
        return "adverbi"
    if luokka in ADJLUOKAT:
        return "adjektiivi"
    if suku or luokka in SUBSTLUOKAT:
        return "substantiivi"
    otsikko = (ctx["alaluku"] or "").lower()
    for avain, arvo in (("verbi", "verbi"), ("substantiivi", "substantiivi"),
                        ("adjektiivi", "adjektiivi"), ("adverbi", "adverbi")):
        if avain in otsikko:
            return arvo
    return {1: "verbi", 2: "substantiivi", 3: "adjektiivi"}.get(ctx["luku_nro"], "ilmaus")


def jasenna_esimerkki(rivi):
    palat = rivi.split(" / ") if " / " in rivi else [rivi]
    if not all(" = " in p for p in palat):
        palat = [rivi]
    tulos = []
    for pala in palat:
        if " = " in pala:
            sv, fi = pala.split(" = ", 1)
            tulos.append({"sv": sv.strip(), "fi": fi.strip()})
        else:
            tulos.append({"sv": pala.strip(), "fi": None})
    return tulos


def tee_sana(ruotsi_raaka, luokka, suomi_raaka, ctx, kaytetyt):
    perusmuoto, taivutus, suku = jaa_muodot(ruotsi_raaka)
    perusmuoto, rektio = poimi_rektio(perusmuoto)
    if not rektio and ctx["rektioluku"]:
        loydot = [p for p in re.split(r"[\s/]+", perusmuoto) if p in PREPOSITIOT]
        if loydot:
            rektio = "/".join(dict.fromkeys(loydot))
    sanaluokka = (SANALUOKKA_POIKKEUS.get(perusmuoto)
                  or paattele_sanaluokka(luokka, suku, ctx))
    if not perusmuoto or not suomi_raaka.strip():
        varoitukset.append(f"rivi {ctx['rivi']}: tyhja sana tai kaannos: {ruotsi_raaka!r}")
    return {
        "tyyppi": "sana",
        "id": tee_tunnus(perusmuoto, kaytetyt),
        "sanaluokka": sanaluokka,
        "ruotsi": perusmuoto,
        "suomi": jaa_pilkuilla(suomi_raaka),
        "taivutus": taivutus,
        "luokka": luokka,
        "suku": suku,
        "kategoria": ctx["luku"],
        "alakategoria": ctx["alaluku"],
        "valiotsikko": ctx["valiotsikko"],
        "vastakohta": None,
        "rektio": rektio,
        "esimerkit": [],
        "muistiinpano": None,
        "paallekkainen": False,
    }


def jasenna_merkinta(ruotsi_raaka, luokka, suomi_raaka, ctx, kaytetyt):
    """Palauttaa listan sanoja: 1 kpl, tai 2 kun rivilla on vastakohtapari."""
    if "↔" in ruotsi_raaka and "↔" in suomi_raaka:
        sv_osat = [o.strip() for o in ruotsi_raaka.split("↔")]
        fi_osat = [o.strip() for o in suomi_raaka.split("↔")]
        if len(sv_osat) == len(fi_osat) == 2:
            a = tee_sana(sv_osat[0], luokka, fi_osat[0], ctx, kaytetyt)
            b = tee_sana(sv_osat[1], luokka, fi_osat[1], ctx, kaytetyt)
            a["vastakohta"], b["vastakohta"] = b["id"], a["id"]
            return [a, b]
    if ctx["luku_nro"] == 3 and " / " in ruotsi_raaka and " / " in suomi_raaka:
        sv_osat = [o.strip() for o in ruotsi_raaka.split(" / ")]
        fi_osat = [o.strip() for o in suomi_raaka.split(" / ")]
        if len(sv_osat) == len(fi_osat):
            return [tee_sana(sv, luokka, fi, ctx, kaytetyt)
                    for sv, fi in zip(sv_osat, fi_osat)]
    return [tee_sana(ruotsi_raaka, luokka, suomi_raaka, ctx, kaytetyt)]


def on_yhtasuuruusmerkinta(rivi):
    """Onko rivi muotoa "sana = suomi" (Skrivtavla, luku 6.9)?

    Kieliopin selitysteksteissa esiintyy myos yhtasuuruusmerkki keskella
    virketta, joten hakusanapuoli saa olla vain lyhyt eika sisaltaa
    virkevalimerkkeja.
    """
    if " = " not in rivi:
        return False
    hakusana = rivi.split(" = ", 1)[0]
    return len(hakusana) <= 60 and not any(m in hakusana for m in ".!?:")


def on_paivays(rivi):
    return (rivi.startswith(VIIKONPAIVAT)
            or re.fullmatch(r"\d{1,2}[.:]\d{2}", rivi) is not None)


def on_sivun_otsikko(rivi, seuraava):
    """Sivun otsikko on lyhyt rivi, jota seuraa paivays tai alaluvun numero.

    Pituusehto erottaa otsikon kappaleesta: myos luvun johdantokappaletta
    seuraa alaluvun numero, mutta kappale on aina pitka ja paattyy pisteeseen.
    """
    if not seuraava or len(rivi) > VALIOTSIKON_RAJA or rivi.endswith("."):
        return False
    return on_paivays(seuraava) or re.match(r"^\d+\.\d+\s", seuraava) is not None


def rakenna():
    rivit = LAHDE.read_text(encoding="utf-8").split("\n")
    doc = {"otsikko": OTSIKKO, "alaotsikko": ALAOTSIKKO, "johdanto": [], "luvut": []}
    kaytetyt = set()
    luku = alaluku = None
    ctx = {"luku": None, "luku_nro": 0, "alaluku": None, "valiotsikko": None,
           "rektioluku": False, "muistilista": False, "rivi": 0}
    viime_sana = None

    def seuraava_rivi(i):
        for j in range(i + 1, len(rivit)):
            if rivit[j].strip():
                return rivit[j].strip()
        return None

    def sisalto():
        nonlocal alaluku
        if luku is None:
            return doc["johdanto"]
        if alaluku is None:
            alaluku = {"otsikko": None, "sisalto": []}
            luku["alaluvut"].append(alaluku)
            ctx["alaluku"] = None
        return alaluku["sisalto"]

    for numero, raaka in enumerate(rivit):
        rivi = raaka.rstrip()
        ctx["rivi"] = numero + 1
        if not rivi.strip():
            continue

        sisennetty = raaka[:1] in ("\t", " ")
        teksti = rivi.strip()

        if sisennetty:
            if teksti.startswith("Korjaus:"):
                sisalto().append({"tyyppi": "korjaus",
                                  "teksti": teksti[len("Korjaus:"):].strip(),
                                  "liittyy": viime_sana["id"] if viime_sana else None})
            elif " = " in teksti and not teksti.startswith(HUOMION_ALUT):
                esimerkit = jasenna_esimerkki(teksti)
                if viime_sana is not None:
                    viime_sana["esimerkit"].extend(esimerkit)
                else:
                    sisalto().append({"tyyppi": "esimerkki", "esimerkit": esimerkit})
            else:
                sisalto().append({"tyyppi": "huomio", "teksti": teksti,
                                  "liittyy": viime_sana["id"] if viime_sana else None})
            continue

        if on_paivays(teksti):
            continue

        osui_alaluku = re.match(r"^(\d+)\.(\d+)\s+(.*)$", teksti)
        if osui_alaluku and luku is not None:
            if ctx["luku_nro"] == 0:
                ctx["luku_nro"] = int(osui_alaluku.group(1))
                luku["otsikko"] = f"{ctx['luku_nro']} {luku['otsikko']}"
                ctx["luku"] = luku["otsikko"]
            alaluku = {"otsikko": teksti, "sisalto": []}
            luku["alaluvut"].append(alaluku)
            viime_sana = None
            ctx["alaluku"] = teksti
            ctx["valiotsikko"] = None
            ctx["rektioluku"] = bool(re.match(r"^6\.[3-6]\b", teksti))
            continue

        if EROTIN in teksti or on_yhtasuuruusmerkinta(teksti):
            if EROTIN in teksti:
                ruotsi_raaka, suomi_raaka = teksti.split(EROTIN, 1)
            else:
                ruotsi_raaka, suomi_raaka = teksti.split(" = ", 1)
            ruotsi_raaka, luokka = erota_luokka(ruotsi_raaka)
            sanat = jasenna_merkinta(ruotsi_raaka, luokka, suomi_raaka, ctx, kaytetyt)
            sisalto().extend(sanat)
            viime_sana = sanat[0]
            continue

        # Jaljelle jaa otsikko, kappale tai muistilistan rivi.
        if on_sivun_otsikko(teksti, seuraava_rivi(numero)):
            luku = {"otsikko": teksti, "alaluvut": []}
            doc["luvut"].append(luku)
            alaluku = None
            viime_sana = None
            ctx.update(luku=teksti, luku_nro=0, alaluku=None, valiotsikko=None,
                       rektioluku=False, muistilista=teksti.startswith("Muistilista"))
        elif ctx["muistilista"]:
            viime_sana = None
            sisalto().append({"tyyppi": "muistilista", "teksti": teksti})
        elif len(teksti) > VALIOTSIKON_RAJA or teksti.endswith("."):
            viime_sana = None
            sisalto().append({"tyyppi": "teksti", "teksti": teksti})
        else:
            viime_sana = None
            ctx["valiotsikko"] = teksti
            sisalto().append({"tyyppi": "otsikko", "teksti": teksti})

    return doc


def numeroi_luvut(doc):
    """Numeroimattomat luvut (ei alalukujen numeroita) jatkavat edellisesta."""
    edellinen = 0
    for luku in doc["luvut"]:
        osui = re.match(r"^(\d+)\s", luku["otsikko"])
        if osui:
            edellinen = int(osui.group(1))
        elif edellinen:
            edellinen += 1
            luku["otsikko"] = f"{edellinen} {luku['otsikko']}"
            for alaluku in luku["alaluvut"]:
                for kohta in alaluku["sisalto"]:
                    if kohta["tyyppi"] == "sana":
                        kohta["kategoria"] = luku["otsikko"]


def merkitse_paallekkaiset(doc):
    """Sama sana useassa luvussa: teoriassa kaikki, kortteja vain ensimmaisesta."""
    nahdyt, maara = set(), 0
    for luku in doc["luvut"]:
        for alaluku in luku["alaluvut"]:
            for kohta in alaluku["sisalto"]:
                if kohta["tyyppi"] != "sana":
                    continue
                avain = kohta["ruotsi"].lower()
                if avain in nahdyt:
                    kohta["paallekkainen"] = True
                    maara += 1
                else:
                    nahdyt.add(avain)
    return maara


if __name__ == "__main__":
    doc = rakenna()
    numeroi_luvut(doc)
    paallekkaisia = merkitse_paallekkaiset(doc)
    KOHDE.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    sanat = [k for l in doc["luvut"] for a in l["alaluvut"]
             for k in a["sisalto"] if k["tyyppi"] == "sana"]
    laskuri = {}
    for s in sanat:
        laskuri[s["sanaluokka"]] = laskuri.get(s["sanaluokka"], 0) + 1
    print(f"Kirjoitettu {KOHDE.name}: {len(doc['luvut'])} lukua, {len(sanat)} sanaa")
    for k in sorted(laskuri, key=lambda x: -laskuri[x]):
        print(f"  {k:14} {laskuri[k]}")
    print(f"  rektioita     {sum(1 for s in sanat if s['rektio'])}")
    print(f"  vastakohtia   {sum(1 for s in sanat if s['vastakohta'])}")
    print(f"  esimerkkeja   {sum(len(s['esimerkit']) for s in sanat)}")
    print(f"  paallekkaisia {paallekkaisia} (ei kortteja)")
    print(f"  -> kortteja   {(len(sanat) - paallekkaisia) * 2}")
    print("\nLuvut:")
    for l in doc["luvut"]:
        n = sum(1 for a in l["alaluvut"] for k in a["sisalto"] if k["tyyppi"] == "sana")
        print(f"  {l['otsikko']:34} {len(l['alaluvut']):2} alalukua, {n:3} sanaa")
    if varoitukset:
        print(f"\nVaroitukset ({len(varoitukset)}):", file=sys.stderr)
        for v in varoitukset:
            print("  " + v, file=sys.stderr)
