#!/usr/bin/env python3
"""Muuntaa lahde/sanasto.txt -> sanasto.json (lukurakenne, ks. SPEC.md luku 1).

Lahdemuoto (rivialkuiset merkit):
  T / S   dokumentin otsikko ja alaotsikko
  p       kappale
  # ## ###  luku, alaluku, valiotsikko
  * ruotsi|luokka|suomi     sana taivutusmuotoineen
  = ruotsi|suomi            ilmaus (ei taivutusta)
  >       esimerkki, muotoa "sv = fi", useampi erotettuna " / "
  !       korjaus alkuperaisiin muistiinpanoihin
  ~       huomio
"""
import json
import re
import sys
from pathlib import Path

JUURI = Path(__file__).resolve().parent.parent
LAHDE = JUURI / "lahde" / "sanasto.txt"
KOHDE = JUURI / "sanasto.json"

VERBILUOKAT = {"I", "IIa", "IIb", "III", "IV", "dep."}
ADJLUOKAT = {"adj.", "part.", "taipumaton"}
PREPOSITIOT = {
    "på", "för", "till", "av", "med", "om", "efter", "från", "mot", "över",
    "åt", "i", "hos", "genom", "under", "vid", "inför", "utan", "trots",
}
# Luvun 3.1 vastakohtapareissa on mukana muutama verbi.
SANALUOKKA_POIKKEUS = {"förbättra": "verbi", "försämra": "verbi"}

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
    osui_suku = re.match(r"^(en|ett)\s+(.*)$", teksti)
    if osui_suku:
        suku = osui_suku.group(1)
        teksti = osui_suku.group(2)
    if " – " in teksti and "," not in teksti:
        osat = [o.strip() for o in teksti.split(" – ")]
    else:
        osat = jaa_pilkuilla(teksti)
    osat = [re.sub(r"^(att|har|\(har\))\s+", "", o).strip() for o in osat]
    return osat[0], osat[1:], suku


def poimi_rektio(perusmuoto):
    """Erottaa perusmuodosta sulkeissa olevan rektion: klaga (på/över)."""
    osui = re.search(r"\s*\(([^)]+)\)\s*$", perusmuoto)
    if not osui:
        return perusmuoto, None
    sisalto = osui.group(1)
    palat = [p.strip() for p in re.split(r"[/,]", sisalto)]
    if palat and all(p in PREPOSITIOT for p in palat):
        return perusmuoto[: osui.start()].strip(), "/".join(palat)
    return perusmuoto, None


def paattele_sanaluokka(luokka, suku, luku_nro, alaluku_otsikko):
    if suku:
        return "substantiivi"
    if luokka in VERBILUOKAT:
        return "verbi"
    if luokka == "adv.":
        return "adverbi"
    if luokka in ADJLUOKAT:
        return "adjektiivi"
    if luokka == "adj.subst.":
        return "substantiivi"
    if luokka in {"1", "2", "3", "4", "5", "epäsäänn."}:
        return "substantiivi"
    otsikko = (alaluku_otsikko or "").lower()
    for avain, arvo in (("verbi", "verbi"), ("substantiivi", "substantiivi"),
                        ("adjektiivi", "adjektiivi"), ("adverbi", "adverbi")):
        if avain in otsikko:
            return arvo
    return {1: "verbi", 2: "substantiivi", 3: "adjektiivi"}.get(luku_nro, "ilmaus")


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


def tee_sana(ruotsi_raaka, luokka, suomi_raaka, ctx, kaytetyt, jaa_taivutus=True):
    if jaa_taivutus:
        perusmuoto, taivutus, suku = jaa_muodot(ruotsi_raaka)
    else:
        perusmuoto, taivutus, suku = ruotsi_raaka.strip(), [], None
    perusmuoto, rektio = poimi_rektio(perusmuoto)
    if not rektio and ctx["rektioluku"]:
        loydot = [p for p in re.split(r"[\s/]+", perusmuoto) if p in PREPOSITIOT]
        if loydot:
            rektio = "/".join(dict.fromkeys(loydot))
    sanaluokka = SANALUOKKA_POIKKEUS.get(perusmuoto) or paattele_sanaluokka(
        luokka, suku, ctx["luku_nro"], ctx["alaluku"])
    if not perusmuoto or not suomi_raaka.strip():
        varoitukset.append(f"rivi {ctx['rivi']}: tyhja sana tai kaannos: {ruotsi_raaka!r}")
    return {
        "tyyppi": "sana",
        "id": tee_tunnus(perusmuoto, kaytetyt),
        "sanaluokka": sanaluokka,
        "ruotsi": perusmuoto,
        "suomi": jaa_pilkuilla(suomi_raaka),
        "taivutus": taivutus,
        "luokka": luokka if luokka and luokka not in {"–", ""} else None,
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


def jasenna_merkinta(ruotsi_raaka, luokka, suomi_raaka, ctx, kaytetyt, jaa_taivutus):
    """Palauttaa listan sanoja: 1 kpl, tai 2 kun rivilla on vastakohtapari."""
    if "↔" in ruotsi_raaka and "↔" in suomi_raaka:
        sv_osat = [o.strip() for o in ruotsi_raaka.split("↔")]
        fi_osat = [o.strip() for o in suomi_raaka.split("↔")]
        if len(sv_osat) == len(fi_osat) == 2:
            a = tee_sana(sv_osat[0], luokka, fi_osat[0], ctx, kaytetyt, jaa_taivutus)
            b = tee_sana(sv_osat[1], luokka, fi_osat[1], ctx, kaytetyt, jaa_taivutus)
            a["vastakohta"], b["vastakohta"] = b["id"], a["id"]
            return [a, b]
    if ctx["luku_nro"] == 3 and " / " in ruotsi_raaka and " / " in suomi_raaka:
        sv_osat = [o.strip() for o in ruotsi_raaka.split(" / ")]
        fi_osat = [o.strip() for o in suomi_raaka.split(" / ")]
        if len(sv_osat) == len(fi_osat):
            return [tee_sana(sv, luokka, fi, ctx, kaytetyt, jaa_taivutus)
                    for sv, fi in zip(sv_osat, fi_osat)]
    return [tee_sana(ruotsi_raaka, luokka, suomi_raaka, ctx, kaytetyt, jaa_taivutus)]


def rakenna():
    rivit = LAHDE.read_text(encoding="utf-8").split("\n")
    doc = {"otsikko": "", "alaotsikko": "", "johdanto": [], "luvut": []}
    kaytetyt = set()
    luku = alaluku = None
    ctx = {"luku": None, "luku_nro": 0, "alaluku": None, "valiotsikko": None,
           "rektioluku": False, "rivi": 0}
    viime_sana = None

    def sisalto():
        nonlocal alaluku
        if luku is None:
            return None
        if alaluku is None:
            alaluku = {"otsikko": None, "sisalto": []}
            luku["alaluvut"].append(alaluku)
            ctx["alaluku"] = None
        return alaluku["sisalto"]

    for numero, raaka in enumerate(rivit, start=1):
        rivi = raaka.rstrip()
        ctx["rivi"] = numero
        if not rivi.strip():
            continue
        merkki, _, loppu = rivi.partition(" ")
        loppu = loppu.strip()

        if merkki == "T":
            doc["otsikko"] = loppu
        elif merkki == "S":
            doc["alaotsikko"] = loppu
        elif merkki == "#":
            luku = {"otsikko": loppu, "alaluvut": []}
            doc["luvut"].append(luku)
            alaluku = None
            viime_sana = None
            osui = re.match(r"^(\d+)", loppu)
            ctx.update(luku=loppu, luku_nro=int(osui.group(1)) if osui else 0,
                       alaluku=None, valiotsikko=None, rektioluku=False)
        elif merkki == "##":
            alaluku = {"otsikko": loppu, "sisalto": []}
            luku["alaluvut"].append(alaluku)
            viime_sana = None
            ctx["alaluku"] = loppu
            ctx["valiotsikko"] = None
            ctx["rektioluku"] = bool(re.match(r"^6\.[3-6]\b", loppu))
        elif merkki == "###":
            ctx["valiotsikko"] = loppu
            viime_sana = None
            sisalto().append({"tyyppi": "otsikko", "teksti": loppu})
        elif merkki == "p":
            viime_sana = None
            (doc["johdanto"] if luku is None else sisalto()).append(
                {"tyyppi": "teksti", "teksti": loppu})
        elif merkki in {"*", "="}:
            osat = loppu.split("|")
            if merkki == "*":
                if len(osat) != 3:
                    varoitukset.append(f"rivi {numero}: * odotti 3 kenttaa, sai {len(osat)}")
                    continue
                ruotsi_raaka, luokka, suomi_raaka = osat
                jaa_taivutus = True
            else:
                if len(osat) < 2:
                    varoitukset.append(f"rivi {numero}: = odotti 2 kenttaa, sai {len(osat)}")
                    continue
                ruotsi_raaka, suomi_raaka = osat[0], "|".join(osat[1:])
                luokka = None
                # Luvun 3.1 vastakohtaparit on kirjattu =-riveille taivutuksineen.
                jaa_taivutus = ctx["alaluku"] is not None and ctx["alaluku"].startswith("3.1")
            if not suomi_raaka.strip():
                viime_sana = None
                sisalto().append({"tyyppi": "muistilista", "teksti": ruotsi_raaka.strip()})
                continue
            sanat = jasenna_merkinta(ruotsi_raaka, luokka, suomi_raaka, ctx,
                                     kaytetyt, jaa_taivutus)
            sisalto().extend(sanat)
            viime_sana = sanat[0]
        elif merkki == ">":
            esimerkit = jasenna_esimerkki(loppu)
            if viime_sana is not None:
                viime_sana["esimerkit"].extend(esimerkit)
            else:
                sisalto().append({"tyyppi": "esimerkki", "esimerkit": esimerkit})
        elif merkki in {"!", "~"}:
            sisalto().append({
                "tyyppi": "korjaus" if merkki == "!" else "huomio",
                "teksti": loppu,
                "liittyy": viime_sana["id"] if viime_sana else None,
            })
        else:
            varoitukset.append(f"rivi {numero}: tuntematon merkki {merkki!r}")

    return doc


def tilasto(doc):
    sanat = [k for l in doc["luvut"] for a in l["alaluvut"]
             for k in a["sisalto"] if k["tyyppi"] == "sana"]
    laskuri = {}
    nimet = {}
    for s in sanat:
        laskuri[s["sanaluokka"]] = laskuri.get(s["sanaluokka"], 0) + 1
        nimet.setdefault(s["ruotsi"], []).append(s["id"])
    kaksoiset = {k: v for k, v in nimet.items() if len(v) > 1}
    return sanat, laskuri, kaksoiset


def merkitse_paallekkaiset(doc):
    """Sama sana esiintyy lahteessa useassa luvussa (esim. lycka-pesue luvussa 8).
    Teoriassa kaikki esiintymat nakyvat; kortteja tehdaan vain ensimmaisesta."""
    nahdyt = set()
    maara = 0
    for l in doc["luvut"]:
        for a in l["alaluvut"]:
            for k in a["sisalto"]:
                if k["tyyppi"] != "sana":
                    continue
                avain = k["ruotsi"].lower()
                if avain in nahdyt:
                    k["paallekkainen"] = True
                    maara += 1
                else:
                    nahdyt.add(avain)
    return maara


if __name__ == "__main__":
    doc = rakenna()
    paallekkaisia = merkitse_paallekkaiset(doc)
    KOHDE.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    sanat, laskuri, kaksoiset = tilasto(doc)
    print(f"Kirjoitettu {KOHDE.name}: {len(doc['luvut'])} lukua, {len(sanat)} sanaa")
    for k in sorted(laskuri, key=lambda x: -laskuri[x]):
        print(f"  {k:14} {laskuri[k]}")
    print(f"  rektioita     {sum(1 for s in sanat if s['rektio'])}")
    print(f"  vastakohtia   {sum(1 for s in sanat if s['vastakohta'])}")
    print(f"  esimerkkeja   {sum(len(s['esimerkit']) for s in sanat)}")
    print(f"  paallekkaisia {paallekkaisia} (ei kortteja)")
    print(f"  -> kortteja   {(len(sanat) - paallekkaisia) * 2}")
    if kaksoiset:
        print(f"\nSama ruotsin sana useammassa kohdassa ({len(kaksoiset)}):")
        for k, v in sorted(kaksoiset.items()):
            print(f"  {k}: {', '.join(v)}")
    if varoitukset:
        print(f"\nVaroitukset ({len(varoitukset)}):", file=sys.stderr)
        for v in varoitukset:
            print("  " + v, file=sys.stderr)
