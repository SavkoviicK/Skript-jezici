# Format fajla pacijenti.txt:
#   ID,Ime,Prezime,Username,Telefon
# (telefon je opciono polje – ako nedostaje, ostaje prazan string).

pacijenti = []

def str2pacijent(line):
    
    parts = [p.strip() for p in line.rstrip('\n').split(',')]

    if len(parts) < 4:
        return None

    return {
        'id': parts[0],
        'ime': parts[1],
        'prezime': parts[2],
        'username': parts[3],
        'telefon': parts[4] if len(parts) >= 5 else ''  # (opciono)
    }

def pacijent2str(pacijent):
    """
    Obrnuto od str2pacijent:
    Recnik pacijenta pretvara u string spreman za upis u fajl pacijenti.txt.
    Uvek snima 5 kolona (ako telefon nedostaje, snima prazan string).
    """
    return ','.join([
        pacijent['id'],
        pacijent['ime'],
        pacijent['prezime'],
        pacijent['username'],
        pacijent.get('telefon', '')
    ])

def load_pacijenti():
    pacijenti.clear()
    try:
        with open('pacijenti.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    p = str2pacijent(line)
                    if p is not None:
                        pacijenti.append(p)
    except FileNotFoundError:
        with open('pacijenti.txt', 'w', encoding='utf-8') as file:
            pass

def find_pacijent_by_username(username):
    """
    Pronalazi pacijenta na osnovu korisnickog imena.
    Ako postoji – vraca recnik pacijenta.
    Ako ne – vraca None.
    """
    for pacijent in pacijenti:
        if pacijent['username'] == username:
            return pacijent
    return None

def find_pacijent_by_id(pacijent_id):
    """
    Pronalazi pacijenta na osnovu ID-a.
    Ako postoji – vraca rečnik pacijenta.
    Ako ne – vraca None
    """
    for pacijent in pacijenti:
        if pacijent['id'] == pacijent_id:
            return pacijent
    return None

def svi_pacijenti():
    """
    Vraca listu svih pacijenata iz memorije
    """
    return pacijenti

def save_pacijenti():
    with open('pacijenti.txt', 'w', encoding='utf-8') as file:
        for pacijent in pacijenti:
            file.write(pacijent2str(pacijent) + '\n')

def update_telefon_by_username(username: str, novi_telefon: str) -> bool:
    """
    Azurira broj telefona pacijenta po username-u.
    Ako je izmena uspesna vraca True, inace False
    """
    p = find_pacijent_by_username(username)
    if not p:
        return False
    p['telefon'] = (novi_telefon or '').strip()
    save_pacijenti()
    return True

load_pacijenti()
