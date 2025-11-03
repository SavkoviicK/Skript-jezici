# Format fajla korisnici.txt:
#   id,ime,prezime,username,password,uloga

# Globalna lista u kojoj se cuvaju svi korisnici kao recnici
korisnici = []

def str2user(line):
    
    # Ukloni novi red ako postoji i podeli po zarezu
    parts = [p.strip() for p in line.rstrip('\n').split(',')]

    # Pretvori u recnik
    return {
        'id': parts[0],
        'ime': parts[1],
        'prezime': parts[2],
        'username': parts[3],
        'password': parts[4],
        'uloga': parts[5]   # npr. 'lekar' ili 'pacijent'
    }

def user2str(user):
    """
    Obrnuto od str2user: recnik korisnika pretvara u string
    spreman za upis u fajl korisnici.txt.
    """
    return ','.join([
        user['id'],
        user['ime'],
        user['prezime'],
        user['username'],
        user['password'],
        user['uloga']
    ])

def load_users():
    """
    Ucitava sve korisnike iz fajla 'korisnici.txt' u globalnu listu korisnici.
    """
    korisnici.clear()
    try:
        with open('korisnici.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():
                    korisnici.append(str2user(line))
    except FileNotFoundError:
        # Ako fajl ne postoji, kreira se prazan fajl
        with open('korisnici.txt', 'w', encoding='utf-8') as file:
            pass

def save_users():
    """
    Snima sve korisnike iz memorije nazad u fajl 'korisnici.txt'.
    """
    with open('korisnici.txt', 'w', encoding='utf-8') as file:
        for user in korisnici:
            file.write(user2str(user) + '\n')

def login(username, password):
    """
    Proverava da li postoje korisnik sa datim username i password.
    Ako postoji – vraca recnik korisnika.
    Ako ne – vraca None.
    """
    for user in korisnici:
        if user['username'] == username and user['password'] == password:
            return user
    return None

def get_user_by_username(username):
    """
    Pronalazi korisnika po korisnickom imenu.
    Ako postoji – vraca recnik korisnika.
    Ako ne – vraca None.
    """
    for user in korisnici:
        if user['username'] == username:
            return user
    return None

load_users()
