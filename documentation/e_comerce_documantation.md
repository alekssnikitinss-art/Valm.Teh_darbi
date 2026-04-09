# E-komercijas produktu meklēšanas sistēma

## 1. Ievads

Šī darba mērķis ir izstrādāt e-komercijas produktu meklēšanas sistēmu Python valodā, kas spēj ātri un precīzi atrast produktus pēc lietotāja meklēšanas vaicājuma.

Sistēma izstrādāta darbam terminālī un atbalsta:
- teksta meklēšanu pēc produkta nosaukuma un apraksta
- filtrēšanu pēc kategorijas
- filtrēšanu pēc zīmola
- meklēšanu noteiktā cenu diapazonā
- pieejamības statusa pārbaudi
- rezultātu kārtošanu pēc relevances, cenas, reitinga un datuma
- auto-complete funkcionalitāti
- typo tolerance

Šīs prasības atbilst uzdevuma aprakstam par e-komercijas produktu meklēšanas sistēmu. :contentReference[oaicite:0]{index=0}

---

## 2. Prasību analīze

### 2.1. Funkcionālās prasības

Sistēmai jānodrošina:
- teksta meklēšana produktu nosaukumos un aprakstos
- kategoriju filtrēšana
- cenu diapazona meklēšana
- zīmolu filtrēšana
- pieejamības pārbaude
- rezultātu kārtošana
- auto-complete un typo tolerance :contentReference[oaicite:1]{index=1}

### 2.2. Nefunkcionālās prasības

Sistēmai jānodrošina:
- atbildes laiks mazāks par 200 ms standarta meklēšanai
- spēja apstrādāt 1000+ vienlaicīgas meklēšanas
- efektīva darbība ar 1M+ produktiem
- RAM patēriņš ne lielāks par 4 GB uz 100K produktu
- indeksa izmērs ne lielāks par 150% no sākotnējo datu izmēra
- korekta kļūdu apstrāde :contentReference[oaicite:2]{index=2}

---

## 3. Algoritma izvēle un pamatojums

### 3.1. Izvēlētais risinājums

Sistēmā tiek izmantots kombinēts risinājums:

- **Inverted Index** — teksta meklēšanai
- **Trie** — auto-complete funkcionalitātei
- **HashMap / dict / set** — kategoriju, zīmolu un pieejamības filtriem
- **Sakārtots cenu saraksts ar `bisect`** — cenu diapazona meklēšanai

Šāda pieeja atbilst arī ieteiktajiem risinājumiem uzdevuma materiālā, kur minēti Inverted Index, koka struktūras, jaucējtabulas un B-tree/B+ tree. :contentReference[oaicite:3]{index=3}

### 3.2. Pamatojums

#### Inverted Index
Inverted Index ir galvenā datu struktūra teksta meklēšanai. Tā vietā, lai katru reizi pārmeklētu visus produktus, sistēma glabā vārdus un tiem atbilstošos produktu ID. Tas ievērojami paātrina meklēšanu.

#### Trie
Trie tiek izmantots prefiksu meklēšanai. Tas ļauj ātri atrast vārdus, kas sākas ar lietotāja ievadīto prefiksu, tāpēc tas ir piemērots auto-complete funkcijai.

#### HashMap / Set
Šīs struktūras nodrošina ļoti ātru filtrēšanu pēc kategorijas, zīmola un pieejamības. Tās ir vienkāršas, efektīvas un labi piemērotas šāda veida uzdevumiem.

#### Sakārtots cenu saraksts
Cenu diapazona meklēšanai tiek izmantots sakārtots saraksts un binārā meklēšana (`bisect`). Tas ļauj ātri atrast produktus noteiktā cenu intervālā.

---

## 4. Alternatīvu salīdzinājums

| Risinājums | Priekšrocības | Trūkumi |
|---|---|---|
| Lineārā meklēšana | Vienkārša implementācija | Lēna pie lieliem datu apjomiem |
| SQL `LIKE` meklēšana | Viegli uztaisīt datubāzē | Slikta mērogojamība un relevance |
| Tikai Trie | Ātrs prefix search | Nav piemērots pilnteksta meklēšanai |
| Tikai HashMap | Ātri filtri | Nespēj efektīvi veikt pilnteksta meklēšanu |
| Inverted Index + Trie + filtri | Ātrs, mērogojams, atbalsta visas prasības | Sarežģītāka implementācija |

### Secinājums
Optimālākais risinājums ir kombinēt vairākas datu struktūras, jo neviena atsevišķa struktūra nespēj efektīvi izpildīt visas prasības vienlaikus.

---

## 5. Sistēmas arhitektūra

```mermaid
flowchart TD
    A[Lietotājs ievada vaicājumu] --> B[Tokenizācija un normalizācija]
    B --> C[Inverted Index meklēšana]
    C --> D[Typo tolerance]
    D --> E[Filtrēšana pēc kategorijas / zīmola / pieejamības]
    E --> F[Cenu diapazona filtrs]
    F --> G[Relevance score aprēķins]
    G --> H[Kārtošana]
    H --> I[Rezultātu izvade]