# Globalna lista koja u memoriji cuva sve dijagnoze kao recnike
dijagnoze = []

def str2dijagnoza(line):
   
    # Ukloni znak novog reda i podeli po zarezima
    parts = [p.strip() for p in line.rstrip('\n').split(',')]

    # Minimalno 3 kolone: id, naziv, opis
    if len(parts) < 3:
        return None

    # Prva kolona mora biti numericki ID
    if not parts[0].isdigit():
        return None

    return {
        'id': parts[0],
        'naziv': parts[1],
        'opis': parts[2]
    }

def dijagnoza2str(d):
    """
    Obrnuto od str2dijagnoza: iz recnika pravi liniju spremnu za upis u fajl.
    Upisujemo TACNO tri kolone: id,naziv,opis
    """
    return ','.join([d.get('id', ''), d.get('naziv', ''), d.get('opis', '')])

def load_dijagnoze():
    """
    Ucita sve dijagnoze iz fajla 'dijagnoze.txt'
    Ako fajl ne postoji, lista ostaje prazna
    """
    dijagnoze.clear()
    try:
        with open('dijagnoze.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                d = str2dijagnoza(line)
                if d is not None:
                    dijagnoze.append(d)
    except FileNotFoundError:
        pass

def svi_dijagnoze():
    """
    Vraca referencu na listu svih dijagnoza u memoriji.
    """
    return dijagnoze

# Automatsko ucitavanje pri importu modula
load_dijagnoze()
