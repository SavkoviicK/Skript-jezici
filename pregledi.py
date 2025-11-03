# Format fajla pregledi.txt:
#   id,pacijent_id,lekar_id,datum,vreme,opis,dijagnoza
# -----------------------------------------------------

pregledi = []

def str2pregled(line):
    
    parts = [p.strip() for p in line.rstrip('\n').split(',')]
    return {
        'id':         parts[0] if len(parts) > 0 else '',
        'pacijent_id':parts[1] if len(parts) > 1 else '',
        'lekar_id':   parts[2] if len(parts) > 2 else '',
        'datum':      parts[3] if len(parts) > 3 else '',
        'vreme':      parts[4] if len(parts) > 4 else '',
        'opis':       parts[5] if len(parts) > 5 else '',
        'dijagnoza':  parts[6] if len(parts) > 6 else ''
    }

def pregled2str(pregled):
   
    opis = str(pregled.get('opis', '')).replace(',', ' ')
    dijagnoza = str(pregled.get('dijagnoza', '')).replace(',', ' ')
    return ','.join([
        str(pregled['id']),
        str(pregled['pacijent_id']),
        str(pregled['lekar_id']),
        str(pregled['datum']),
        str(pregled['vreme']),
        opis,
        dijagnoza
    ])

def load_pregledi():
    pregledi.clear()
    try:
        with open('pregledi.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    pregledi.append(str2pregled(line))
    except FileNotFoundError:
        with open('pregledi.txt', 'w', encoding='utf-8') as file:
            pass

def save_pregledi():
    with open('pregledi.txt', 'w', encoding='utf-8') as file:
        for p in pregledi:
            file.write(pregled2str(p) + '\n')

def add_pregled(pregled):
    """
    Dodaje novi pregled u listu u memoriji.
    (Kasnije se snima u fajl preko save_pregledi().)
    """
    pregledi.append(pregled)

def get_sledeci_id():
    """
    Pronalazi sledeci slobodan ID za novi pregled.
    """
    if not pregledi:
        return 1
    try:
        return max(int(p['id']) for p in pregledi) + 1
    except Exception:
        return int(pregledi[-1]['id']) + 1

def svi_pregledi():
    """
    Vraca listu svih pregleda iz memorije.
    """
    return pregledi

def get_pregledi_po_lekaru(lekar_id):
    """
    Filtrira i vraca sve preglede za odredjenog lekara.
    """
    return [p for p in pregledi if p['lekar_id'] == lekar_id]

def get_pregledi_po_pacijentu(pacijent_id):
    """
    Filtrira i vraca sve preglede za određenog pacijenta.
    """
    return [p for p in pregledi if p['pacijent_id'] == pacijent_id]

def proveri_slobodan_termin(lekar_id, datum, vreme):
    """
    Proverava da li je termin slobodan kod lekara.
    Termin je zauzet ako vec postoji zapis sa istim lekar_id, datum i vreme.
    """
    for p in pregledi:
        if p['lekar_id'] == lekar_id and p['datum'] == datum and p['vreme'] == vreme:
            return False
    return True

def otkazi_pregled(pregled_id):
    """
    Otkazuje pregled – brise ga iz liste po ID-u.
    Ako uspe, snima promene u fajl i vrasa True.
    Ako ne nađe ID, vraca False.
    """
    for i, p in enumerate(pregledi):
        if p['id'] == pregled_id:
            del pregledi[i]
            save_pregledi()
            return True
    return False

# ---------  Prosek pregleda po lekaru ----------
def broj_pregleda_po_lekaru(samo_obradjeni: bool = False) -> dict[str, int]:
    """
    Vraca: {lekar_id: broj_pregleda}
    Ako je samo_obradjeni=True, broje se samo pregledi sa opisom != 'N/A'.
    """
    cnt = {}
    for p in pregledi:
        if samo_obradjeni:
            val = (p.get('opis') or '').strip()
            if not val or val.upper() == 'N/A':
                continue
        lid = p['lekar_id']
        cnt[lid] = cnt.get(lid, 0) + 1
    return cnt

def broj_radnih_dana_po_lekaru() -> dict[str, int]:
    """
    Koliko RAZLICITIH datuma svaki lekar ima u fajlu (tretira se kao broj radnih dana).
    """
    days = {}
    for p in pregledi:
        lid = p['lekar_id']
        d   = p['datum']
        if lid not in days:
            days[lid] = set()
        days[lid].add(d)
    return {lid: len(s) for lid, s in days.items()}

def prosek_po_lekaru_po_danu(samo_obradjeni: bool = False) -> dict[str, float]:
    """
    Prosek = broj_pregleda / broj_radnih_dana (po lekaru), zaokruzen na 2 decimale.
    """
    cnt = broj_pregleda_po_lekaru(samo_obradjeni=samo_obradjeni)
    days = broj_radnih_dana_po_lekaru()
    out = {}
    for lid, n in cnt.items():
        d = days.get(lid, 0)
        if d > 0:
            out[lid] = round(n / d, 2)
    return out


load_pregledi()
