# Biblotēkas īstenošana (kopsavilkums)

Šeit ir īsi aprakstīts, kas tika izveidots un kā to izmantot.

1) Datu struktūru izvēle
- Mēs izmantojam divu līmeņu atmiņas struktūru klienta pusē (JavaScript):
  - Array (sakārtots saraksts) `books` — saglabā kārtību un atvieglo rādīšanu (iterēšana).
  - Map `byIsbn` — indeksē pēc ISBN, nodrošina O(1) meklēšanu pēc ISBN.

Pamatojums: Array ir viegli uzturēt un parasti pietiek mazām bibliotēkām; Map nodrošina ātru piekļuvi pēc atslēgas (ISBN). Meklēšana pēc nosaukuma/autora izmanto filtru (O(n)), kas ir vienkāršs risinājums mazām datu kopām. Ja datu apjoms pieaugs, serverī izmantojama SQL indekss.

Edge cases: dublikātu aizsardzība balstīta uz ISBN. Tiek aizsargāts pret tukšām vērtībām.

2) Datu objekts
- `Book` ar atribūtiem: `id` (int), `title` (string), `author` (string), `isbn` (string).
- Atmiņā uz klienta tā ir JS objekts; serverī — ieraksts SQLite datubāzē `database/bibloteka.db`.

3) Datubāzes risinājums
- Izvēlēts: lokāla SQLite datubāze (`database/bibloteka.db`) ar API, kas veic CRUD operācijas.
  - Iemesls: SQLite nodrošina transakciju atbalstu, vienkāršu konfigurāciju (viena lokāla .db datne) un labu datu konsekvenci bez atsevišķa DB servera. Tas ir drošāks un uzticamāks nekā tikai teksts vai append-to-.sql pieeja.
  - Salīdzinājums: JSON faila risinājums ir vienkāršs, bet var radīt sacensības rakstīšanas laikā un nav ideāls mērogošanai. PostgreSQL/SQLite serveris ir labāks, ja nepieciešama mērogojamība vai vairākas konkursa piekļuves; SQLite ir labs kompromiss lokālai lietošanai.

4) Kods un API
- Front-end: `WEB/index.html` + `WEB/func/functional.js`. Interfeiss ļauj pievienot, meklēt un dzēst grāmatas.
- API: `WEB/api.py` (Flask). Endpoints:
  - GET /books — atgriež visas grāmatas JSON formātā
  - POST /add_book — pievieno grāmatu (ieraksta ierakstu SQLite DB)
  - POST /delete_book — izdzēš grāmatu (no DB)
  - GET /search?q=... — meklē nosaukumā/autorā
  - GET /export_sql — ģenerē vienkāršu SQL dump (INSERTs) no DB

5) Kā palaist (PowerShell)
```powershell
cd .\Biblotekas_sistema\WEB
python -m pip install -r requirements.txt
# palaist API (izveidosies bibloteka.db automātiski)
python api.py
```

Pēc tam atveriet `index.html` pārlūkā. Front-end veiks pieprasījumus uz `http://127.0.0.1:5002`.

6) Failu atrašanās
- `WEB/index.html` — UI
- `WEB/func/functional.js` — klienta loģika
- `WEB/api.py` — lokālais API (Flask + SQLite)
- `WEB/requirements.txt` — nepieciešamās bibliotēkas
- `WEB/database/bibloteka.db` — SQLite datubāze (izveidojas palaistot API)

Ja vēlaties, varu pārbīdīt API uz citu portu vai pielāgot DB struktūru (piem., pievienot loans tabulu saskaņā ar ER diagrammu). 
# Biblotēkas īstenošana (kopsavilkums)

Šeit ir īsi aprakstīts, kas tika izveidots un kā to izmantot.

1) Datu struktūru izvēle
- Mēs izmantojam divu līmeņu atmiņas struktūru klienta pusē (JavaScript):
  - Array (sakārtots saraksts) `books` — saglabā kārtību un atvieglo rādīšanu (iterēšana).
  - Map `byIsbn` — indeksē pēc ISBN, nodrošina O(1) meklēšanu pēc ISBN.

Pamatojums: Array ir viegli uzturēt un parasti pietiek mazām bibliotēkām; Map nodrošina ātru piekļuvi pēc atslēgas (ISBN). Meklēšana pēc nosaukuma/autora izmanto filtru (O(n)), kas ir vienkāršs risinājums mazām datu kopām. Ja datu apjoms pieaugs, serverī izmantojama SQL indekss.

Edge cases: dublikātu aizsardzība balstīta uz ISBN. Tiek aizsargāts pret tukšām vērtībām.

2) Datu objekts
- `Book` ar atribūtiem: `id` (int), `title` (string), `author` (string), `isbn` (string).
- Atmiņā uz klienta tā ir JS objekts; serverī — JSON ieraksts datu failā `database/data.json`.

3) Datubāzes risinājums
- Izvēlēts: vienkārša JSON datne (`database/data.json`) + papildus pildījums uz `database/bibloteka.sql` ar INSERT teikumiem.
  - Iemesls: vienkāršība, viegla pārvietošana, nav nepieciešama ārēja datubāze. SQL dumps nodrošina, ka var atjaunot relāciju DB viegli, ja nepieciešams.
  - Salīdzinājums: pilna SQL/DB (SQLite/Postgres) nodrošinātu labāku veiktspēju/konkurenci, bet prasītu papildu konfigurāciju. NoSQL nodrošinātu elastību, bet nav nepieciešams šim mazajam projektam.

4) Kods un API
- Front-end: `WEB/index.html` + `WEB/func/functional.js`. Interfeiss ļauj pievienot, meklēt un dzēst grāmatas.
- API: `WEB/api.py` (Flask). Endpoints:
  - GET /books — atgriež visas grāmatas JSON formātā
  - POST /add_book — pievieno grāmatu (pievieno JSON failam un ieraksta SQL INSERT rindā `bibloteka.sql`)
  - POST /delete_book — izdzēš grāmatu (no JSON) un pievieno komentāru SQL failā
  - GET /search?q=... — meklē nosaukumā/autorā

5) Kā palaist (PowerShell)
```
cd .\Biblotekas_sistema\WEB
python -m pip install -r requirements.txt
python api.py
```

Pēc tam atveriet `index.html` pārlūkā. Front-end veiks pieprasījumus uz `http://127.0.0.1:5002`.

6) Failu atrašanās
- `WEB/index.html` — UI
- `WEB/func/functional.js` — klienta loģika
- `WEB/api.py` — lokālais API (Flask)
- `WEB/requirements.txt` — nepieciešamās bibliotēkas
- `WEB/database/data.json` — JSON glabātne
- `WEB/database/bibloteka.sql` — SQL dump, automātiski papildināts

Ja vēlaties, varu pārbīdīt API uz citu portu vai pāriet uz SQLite, lai panāktu striktāku konsistenci un transakcijas. 
