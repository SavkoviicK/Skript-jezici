#   id,ime,prezime,specijalnost

lekari = []

def str2lekar(line):
    
    parts = [p.strip() for p in line.rstrip('\n').split(',')]

    return {
        'id': parts[0],
        'ime': parts[1],
        'prezime': parts[2],
        'specijalnost': parts[3]
    }

def lekar2str(lekar):
    
    return ','.join([
        lekar['id'],
        lekar['ime'],
        lekar['prezime'],
        lekar['specijalnost']
    ])

def load_lekari():
    
    lekari.clear()
    try:
        with open('lekari.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    lekari.append(str2lekar(line))
    except FileNotFoundError:
        with open('lekari.txt', 'w', encoding='utf-8') as file:
            pass

def find_lekar_by_id(lekar_id):
    """
    Pronalazi lekara po ID-u.
    Ako postoji – vraca recnik lekara.
    Ako ne – vraca None.
    """
    for lekar in lekari:
        if lekar['id'] == lekar_id:
            return lekar
    return None

def svi_lekari():
    """
    Vraca listu svih lekara iz memorije.
    """
    return lekari

load_lekari()
