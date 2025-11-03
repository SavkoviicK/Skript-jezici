import korisnici
import lekari
import pacijenti
import pregledi
import dijagnoze
import datetime
import matplotlib.pyplot as plt

ulogovani_korisnik = None


def main():
    global ulogovani_korisnik

    print("Dobrodosli u Stomatolosku ordinaciju!")
    print("=======================================\n")

    # 1) Logovanje
    if not login():
        print("Logovanje nije uspelo. Pogresno korisnicko ime ili lozinka.")
        return

    print(f"\nDobrodosli, {ulogovani_korisnik['ime']} {ulogovani_korisnik['prezime']}!")

    # 2) Glavna petlja – odabir opcija po ulozi
    komanda = ''
    while komanda != 'X':
        if ulogovani_korisnik['uloga'] == 'lekar':
            komanda = meni_lekar()
            if komanda == '1':
                prikazi_preglede_lekara()
            elif komanda == '2':
                unesi_dijagnozu()
            elif komanda == '3':
                prikazi_statistiku_pregleda()
            elif komanda == '4':
                prikazi_prosek_po_lekaru()
        elif ulogovani_korisnik['uloga'] == 'pacijent':
            komanda = meni_pacijent()
            if komanda == '1':
                zakazi_pregled()
            elif komanda == '2':
                prikazi_moje_preglede()
            elif komanda == '3':
                otkazi_pregled_ui()
            elif komanda == '4':
                izmeni_moj_telefon()

    # 3) Na kraju rada – snimi izmene 
    pregledi.save_pregledi()
    korisnici.save_users()
    pacijenti.save_pacijenti()

    print("\nDovidjenja!")


def login():
    """
    Login korisnika preko korisnici.login(username, password).
    """
    global ulogovani_korisnik
    username = input("Unesite korisnicko ime: ")
    password = input("Unesite lozinku: ")
    ulogovani_korisnik = korisnici.login(username, password)
    return ulogovani_korisnik is not None


# ------------------ MENIJI ------------------

    """ LEKAR """

def meni_lekar():
    print("\n--- Meni za lekara ---")
    print("1 - Prikazi sve zakazane preglede")
    print("2 - Unesi dijagnozu za obavljeni pregled")
    print("3 - Prikazi statistiku pregleda (grafikon)")
    print("4 - Prosek pregleda po lekaru (tabela)")
    print("X - Izlaz iz programa")
    komanda = input("Unesite opciju: ").upper()
    return komanda

    """ PACIJENT """

def meni_pacijent():
    print("\n--- Meni za pacijenta ---")
    print("1 - Zakazi novi pregled")
    print("2 - Prikazi moje preglede")
    print("3 - Otkazi pregled")
    print("4 - Izmeni moj telefon")
    print("X - Izlaz iz programa")
    komanda = input("Unesite opciju: ").upper()
    return komanda


# --------------- FUNKCIONALNOSTI: LEKAR ---------------

def prikazi_preglede_lekara():
    """
    Ispisuje sve zakazane preglede za ulogovanog lekara.

    """
    lekar = lekari.find_lekar_by_id(ulogovani_korisnik['id'])
    if not lekar:
        print("Ulogovani korisnik nije povezan sa lekarom. Kontaktirajte administratora.")
        return

    pregledi_lekara = pregledi.get_pregledi_po_lekaru(lekar['id'])
    if not pregledi_lekara:
        print("Nemate zakazanih pregleda.")
        return

    # Sortiraj po datumu, vremenu (stringovi su YYYY-MM-DD i HH:MM )
    pregledi_lekara = sorted(pregledi_lekara, key=lambda p: (p['datum'], p['vreme']))

    print("\n--- Vasi zakazani pregledi ---")
    print("ID | Pacijent        | Datum      | Vreme | Opis       | Dijagnoza")
    print("---|-----------------|------------|-------|------------|----------")
    for p in pregledi_lekara:
        pacijent = pacijenti.find_pacijent_by_id(p['pacijent_id'])
        pacijent_ime = f"{pacijent['ime']} {pacijent['prezime']}" if pacijent else "Nepoznat"
        print(f"{p['id']:>2} | {pacijent_ime:<15} | {p['datum']:<10} | {p['vreme']:<5} | {p['opis']:<10} | {p['dijagnoza']:<10}")


def unesi_dijagnozu():
    
    prikazi_preglede_lekara()
    pregled_id = input("Unesite ID pregleda za koji unosite dijagnozu: ").strip()

    # Nadji pregled po ID-u u memoriji
    pregled = next((p for p in pregledi.pregledi if p['id'] == pregled_id), None)
    if not pregled:
        print("Pregled sa unetim ID-om ne postoji.")
        return

    # Autorizacija – ulogovani lekar mora biti nosilac pregleda
    lekar = lekari.find_lekar_by_id(ulogovani_korisnik['id'])
    if not lekar or pregled['lekar_id'] != lekar['id']:
        print("Nemate ovlascenje da unosite dijagnozu za ovaj pregled.")
        return

    # Ne dozvoli ponovni unos ako je vec obradjen
    if pregled_obradjen(pregled):
        print("Dijagnoza za ovaj pregled je vec uneta.")
        return

    # Prikazi dostupne dijagnoze i omoguci izbor
    print("\n--- Dijagnoze na raspolaganju ---")
    for i, d in enumerate(dijagnoze.dijagnoze):
        print(f"{i+1} - {d['naziv']} ({d['opis']})")

    try:
        izbor = int(input("Unesite redni broj dijagnoze: "))
        if 1 <= izbor <= len(dijagnoze.dijagnoze):
            dijagnoza_naziv = dijagnoze.dijagnoze[izbor-1]['naziv']
            opis = input("Unesite opis pregleda: ").strip() or 'N/A'
            pregled['opis'] = opis
            pregled['dijagnoza'] = dijagnoza_naziv
            pregledi.save_pregledi()
            print("Dijagnoza uspesno uneta!")
        else:
            print("Pogresan izbor dijagnoze.")
    except ValueError:
        print("Uneli ste pogresan format (ocekuje se broj).")


def pregled_obradjen(p):
    """Vraca True ako pregled ima unet opis koji NIJE 'N/A'."""
    val = (p.get('opis') or '').strip()
    return bool(val) and val.upper() != 'N/A'


def prikazi_statistiku_pregleda():
   
    # 1)  lekar_id -> broj obavljenih pregleda
    pregledi_po_lekaru = {}
    for p in pregledi.svi_pregledi():
        if pregled_obradjen(p):
            lekar_id = p['lekar_id']
            pregledi_po_lekaru[lekar_id] = pregledi_po_lekaru.get(lekar_id, 0) + 1

    # 2) Priprema za plot
    lekari_imena, broj_pregleda = [], []
    for lekar_id, broj in pregledi_po_lekaru.items():
        l = lekari.find_lekar_by_id(lekar_id)
        if l:
            lekari_imena.append(f"{l['ime']} {l['prezime']}")
            broj_pregleda.append(broj)

    if not lekari_imena:
        print("Nema dovoljno podataka za prikaz grafikona (nema obavljenih pregleda).")
        return

    # 3) Plot
    plt.figure(figsize=(10, 6))
    plt.bar(lekari_imena, broj_pregleda)
    plt.xlabel('Lekari')
    plt.ylabel('Broj obavljenih pregleda')
    plt.title('Broj obavljenih pregleda po lekaru')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('statistika_pregleda.png')
    print("Grafikon je sacuvan u fajlu statistika_pregleda.png")
    plt.show()

def prikazi_prosek_po_lekaru():
    """
    Tekstualni izvestaj: prosek pregleda po lekaru po danu.
    (1) svi pregledi
    (2) samo obradjeni (opis != 'N/A')
    """
    pro_svi = pregledi.prosek_po_lekaru_po_danu(samo_obradjeni=False)
    pro_obr = pregledi.prosek_po_lekaru_po_danu(samo_obradjeni=True)

    if not pro_svi and not pro_obr:
        print("Nema podataka za izracunavanje proseka.")
        return

    def _ime(lid):
        l = lekari.find_lekar_by_id(lid)
        return f"{l['ime']} {l['prezime']}" if l else f"ID {lid}"

    print("\n--- Prosek pregleda po lekaru (svi pregledi) ---")
    print("Lekar                  | Prosek/dan")
    print("-----------------------|-----------")
    for lid, val in sorted(pro_svi.items(), key=lambda x: _ime(x[0])):
        print(f"{_ime(lid):<23} | {val:>9.2f}")

    print("\n--- Prosek pregleda po lekaru (samo obradjeni) ---")
    print("Lekar                  | Prosek/dan")
    print("-----------------------|-----------")
    for lid, val in sorted(pro_obr.items(), key=lambda x: _ime(x[0])):
        print(f"{_ime(lid):<23} | {val:>9.2f}")


# --------------- FUNKCIONALNOSTI: PACIJENT ---------------

def zakazi_pregled():
    
    pacijent = pacijenti.find_pacijent_by_username(ulogovani_korisnik['username'])
    if not pacijent:
        print("Nalog nije povezan sa pacijentom. Kontaktirajte administratora.")
        return

    print("\n--- Zakazivanje pregleda ---")
    print("Dostupni lekari:")
    for l in lekari.svi_lekari():
        print(f"ID: {l['id']}, Ime: {l['ime']} {l['prezime']}, Specijalnost: {l['specijalnost']}")

    lekar_id = input("Unesite ID lekara kod koga zelite da zakazete: ").strip()
    lekar = lekari.find_lekar_by_id(lekar_id)
    if not lekar:
        print("Izabrani lekar ne postoji.")
        return

    datum = input("Unesite datum pregleda (YYYY-MM-DD): ").strip()
    vreme = input("Unesite vreme pregleda (HH:MM): ").strip()

    # 1) Validacija formata datuma/vremena
    try:
        datetime.datetime.strptime(datum, '%Y-%m-%d')
        datetime.datetime.strptime(vreme, '%H:%M')
    except ValueError:
        print("Pogresan format datuma ili vremena.")
        return

    # 2) Zabrana termina u proslosti
    ts = datetime.datetime.strptime(f"{datum} {vreme}", "%Y-%m-%d %H:%M")
    if ts < datetime.datetime.now():
        print("Ne mosete zakazati termin u proslosti.")
        return

    # 3) Provera zauzeca
    if not pregledi.proveri_slobodan_termin(lekar_id, datum, vreme):
        print("Termin je zauzet. Pokusajte sa drugim datumom ili vremenom.")
        return

    # 4) Kreiranje i snimanje pregleda
    novi_pregled = {
        'id': str(pregledi.get_sledeci_id()),  
        'pacijent_id': pacijent['id'],
        'lekar_id': lekar_id,
        'datum': datum,
        'vreme': vreme,
        'opis': 'N/A',        # dok se ne obavi, opis je N/A
        'dijagnoza': 'N/A'
    }

    pregledi.add_pregled(novi_pregled)
    pregledi.save_pregledi()
    print("Pregled uspesno zakazan!")


def prikazi_moje_preglede():
    """Ispisuje sve preglede ulogovanog pacijenta (povezuje sa imenom lekara)."""
    pacijent = pacijenti.find_pacijent_by_username(ulogovani_korisnik['username'])
    if not pacijent:
        print("Nalog nije povezan sa pacijentom.")
        return

    pregledi_pacijenta = pregledi.get_pregledi_po_pacijentu(pacijent['id'])
    if not pregledi_pacijenta:
        print("Nemate zakazanih ili obavljenih pregleda.")
        return

    print("\n--- Vasi pregledi ---")
    print("ID | Lekar           | Datum      | Vreme | Opis       | Dijagnoza")
    print("---|------------------|------------|-------|------------|----------")
    for p in pregledi_pacijenta:
        l = lekari.find_lekar_by_id(p['lekar_id'])
        lekar_ime = f"{l['ime']} {l['prezime']}" if l else "Nepoznat"
        print(f"{p['id']:>2} | {lekar_ime:<16} | {p['datum']:<10} | {p['vreme']:<5} | {p['opis']:<10} | {p['dijagnoza']:<10}")


def otkazi_pregled_ui():
    pacijent = pacijenti.find_pacijent_by_username(ulogovani_korisnik['username'])
    if not pacijent:
        print("Nalog nije povezan sa pacijentom.")
        return

    prikazi_moje_preglede()
    pid = input("Unesite ID pregleda koji zelite da otkazete: ").strip()

    # dozvoli otkazivanje samo svojih termina
    target = None
    for p in pregledi.get_pregledi_po_pacijentu(pacijent['id']):
        if p['id'] == pid:
            target = p
            break

    if not target:
        print("Ne postoji takav pregled medju vasim terminima.")
        return

    if pregledi.otkazi_pregled(pid):
        print("Pregled je uspesno otkazan.")
    else:
        print("Otkazivanje nije uspelo.")


def izmeni_moj_telefon():
    """Pacijent menja svoj kontakt telefon (snima u pacijenti.txt)."""
    p = pacijenti.find_pacijent_by_username(ulogovani_korisnik['username'])
    if not p:
        print("Nalog nije povezan sa pacijentom.")
        return
    print(f"Trenutni telefon: {p.get('telefon', '')}")
    novi = input("Unesite novi telefon: ").strip()
    if not novi:
        print("Telefon nije promenjen (prazan unos).")
        return
    if pacijenti.update_telefon_by_username(ulogovani_korisnik['username'], novi):
        print("Telefon je uspešno izmenjen.")
    else:
        print("Izmena nije uspela.")


# Standardni Python ulaz u program
if __name__ == '__main__':
    main()
