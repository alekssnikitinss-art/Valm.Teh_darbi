# E-komercijas produktu meklēšanas sistēma

## 1. Ievads

Šī darba mērķis ir izstrādāt e-komercijas produktu meklēšanas sistēmu Python valodā, kas spēj ātri un precīzi atrast produktus pēc lietotāja ievadītā meklēšanas vaicājuma.

Sistēma darbojas terminālī un nodrošina teksta meklēšanu, filtrēšanu, rezultātu kārtošanu, auto-complete funkcionalitāti un kļūdu toleranci.

---

## 2. Funkcionālās prasības

Sistēmai jānodrošina:
- teksta meklēšana produktu nosaukumos un aprakstos
- filtrēšana pēc kategorijas
- filtrēšana pēc zīmola
- cenu diapazona meklēšana
- pieejamības pārbaude
- rezultātu kārtošana
- auto-complete funkcionalitāte
- typo tolerance

---

## 3. Nefunkcionālās prasības

- atbildes laiks mazāks par 200 ms
- spēja apstrādāt 1000+ vienlaicīgas meklēšanas
- efektīva darbība ar lielu datu apjomu
- optimizēts atmiņas patēriņš
- korekta kļūdu apstrāde

---

## 4. Izmantotie algoritmi un datu struktūras

| Algoritms | Pielietojums |
|----------|------------|
| Inverted Index | Teksta meklēšana |
| Trie | Auto-complete |
| HashMap / Set | Filtri |
| Sorted List (bisect) | Cenu diapazons |

---

## 5. Algoritmu skaidrojumi

### Inverted Index

    vārds -> produktu ID saraksts

Piemērs:

    iphone -> [1, 5, 9]

Tas nozīmē, ka vārds "iphone" parādās vairākos produktos.

---

### Trie (prefiksu koks)

    app -> apple, application

Trie tiek izmantots auto-complete funkcijai.

---

### Prefikss

Prefikss ir vārda sākums.

Piemēri:
- app → apple, application
- sam → samsung

---

### HashMap

Izmanto filtrēšanai:
- kategorija
- zīmols
- pieejamība

---

### Cenu diapazons

Izmanto sakārtotu sarakstu un bināro meklēšanu.

---

## 6. Sistēmas darbības process

~~~mermaid
flowchart TD
    A[Lietotājs ievada vaicājumu]
    B[Tokenizācija]
    C[Normalizācija]
    D[Inverted Index]
    E[Typo tolerance]
    F[Filtri]
    G[Cenu filtrs]
    H[Score]
    I[Kārtošana]
    J[Rezultāti]

    A --> B --> C --> D --> E --> F --> G --> H --> I --> J
~~~

---

## 7. Sistēmas arhitektūra

~~~mermaid
flowchart LR
    User --> SearchEngine
    SearchEngine --> InvertedIndex
    SearchEngine --> Trie
    SearchEngine --> Filters
    Filters --> Data
~~~

---

## 8. Datu modelis

~~~mermaid
classDiagram
    class Product {
        id
        nosaukums
        apraksts
        cena
        kategorija
        zimols
        pieejamiba
        reitings
    }

    class SearchResult {
        score
    }

    Product --> SearchResult
~~~

---

## 9. Relevance aprēķins

    score =
        3 * title_matches +
        1 * description_matches +
        rating +
        popularity +
        freshness

Nosaukuma sakritības ir svarīgākas par aprakstu.

---

## 10. Kompleksitātes analīze

| Operācija | Sarežģītība |
|----------|------------|
| Indeksēšana | O(N * T) |
| Meklēšana | O(r log r) |
| Autocomplete | O(p + s) |
| Cenu filtrs | O(log n) |

---

## 11. Gadījumu analīze

Labākais gadījums:
- maz rezultātu
- ļoti ātri

Vidējais gadījums:
- normāla veiktspēja

Sliktākais gadījums:
- daudz kandidātu
- lēnāka kārtošana

---

## 12. Testēšana

~~~mermaid
flowchart TD
    T1[10K dati]
    T2[Performance]
    T3[Precizitāte]
    T4[Filtri]

    T1 --> T2 --> T3 --> T4
~~~

---

## 13. Veiktspējas rezultāti

| Tests | Laiks |
|------|------|
| Meklēšana | ~10 ms |
| Filtri | ~15 ms |
| Auto-complete | ~2 ms |

---

## 14. Programmas palaišana

    python main.py

    python main.py --search "apple"

    python main.py --autocomplete "app"

---

## 15. Secinājumi

Sistēma:
- ir ātra
- izmanto efektīvus algoritmus
- atbilst prasībām
- ir mērogojama

---

## 16. Iespējamie uzlabojumi

- uzlabota typo tolerance
- caching
- paralēlā apstrāde
- Elasticsearch integrācija