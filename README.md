# Stomatološka ordinacija

**Projekat iz predmeta Skript jezici – Python**  

Ovo je aplikacija koja simulira rad stomatološke ordinacije i omogućava upravljanje pacijentima, lekarima i terminima. Projekat je razvijen u **Pythonu** koristeći **Visual Studio Code**, a za prikaz statistike koristi se biblioteka **matplotlib**.

---

## Funkcionalnosti

### Upravljanje korisnicima
- Prijavljivanje korisnika sa različitim ulogama: **lekar** i **pacijent**  
- Funkcionalnosti se razlikuju u zavisnosti od uloge korisnika

### Zakazivanje pregleda
- Pacijent bira lekara, datum i vreme pregleda  
- Provera dostupnosti termina  
- Evidencija zakazanih pregleda

### Vođenje evidencije
- Lekar može unositi dijagnoze i beleške o pregledima  
- Mogućnost dodavanja, izmene i brisanja podataka u bazi (pregledi, dijagnoze, korisnici)

### Statistika i analiza
- Provera slobodnih termina  
- Računanje prosečnog broja pregleda po lekaru  
- Vizuelni prikaz statistike pomoću grafikona (**matplotlib**) – npr. broj pregleda po danima ili po lekarima

---

## Tehnologije
- Python 3.12.3
- Biblioteka matplotlib (za grafik)  
- Visual Studio Code  

---

## Pokretanje aplikacije

1. Klonirajte repozitorijum:
   ```bash
   git clone https://github.com/username/stomatoloska-ordinacija.git
