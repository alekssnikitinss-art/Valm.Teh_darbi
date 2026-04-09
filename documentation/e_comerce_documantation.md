# E-komercijas produktu meklēšanas sistēma (Pilna Mermaid dokumentācija)

```mermaid
flowchart TD

%% =====================================================
%% TITLE
%% =====================================================
TITLE["E-komercijas produktu meklēšanas sistēma"]

%% =====================================================
%% FUNCTIONAL REQUIREMENTS + EXPLANATION
%% =====================================================
subgraph Funkcionalas_prasibas
    F1[Text search\nMeklē pēc nosaukuma/apraksta]
    F2[Kategoriju filtrs\nAtlasīt tikai noteiktu kategoriju]
    F3[Cenu diapazons\nMin/max cena]
    F4[Zīmolu filtrs\nAtlasīt konkrētu zīmolu]
    F5[Pieejamība\nTikai noliktavā esošie]
    F6[Sortēšana\nRelevance/cena/reitings]
    F7[Auto-complete\nIeteikumi rakstot]
    F8[Typo tolerance\nKļūdu tolerēšana]
end

%% =====================================================
%% NON-FUNCTIONAL REQUIREMENTS
%% =====================================================
subgraph Nefunkcionalas_prasibas
    N1[<200ms\nĀtra atbilde]
    N2[1000+ queries\nDaudz lietotāju]
    N3[1M+ produkti\nMērogojamība]
    N4[RAM limits\nEfektīva atmiņa]
    N5[Index <=150%\nIndeksa izmērs]
end

%% =====================================================
%% CORE ALGORITHMS + EXPLANATION
%% =====================================================
subgraph Algoritmi
    A1[Inverted Index\nVārds → produktu saraksts\nĀtra teksta meklēšana]
    A2[Trie\nPrefiksu koks\nAuto-complete]
    A3[HashMap\nKey → Value\nĀtri filtri]
    A4[Sorted List\nSakārtotas cenas\nDiapazona meklēšana]
end

%% =====================================================
%% PREFIX EXPLANATION (VERY IMPORTANT FOR SCHOOL)
%% =====================================================
subgraph Prefiksi_un_AutoComplete
    P1[Prefikss = vārda sākums\npiem: "app"]
    P2[Trie meklē visus vārdus\nkas sākas ar prefiksu]
    P3[Rezultāts:\napple, application]
end

P1 --> P2 --> P3

%% =====================================================
%% MAIN SEARCH FLOW
%% =====================================================
subgraph Meklesanas_process
    U[Lietotājs ievada tekstu]

    T1[Tokenizācija\nSadala vārdos]
    T2[Normalizācija\nLowercase + tīrīšana]

    IDX[Inverted Index\nAtrod kandidātus]

    TYPO[Typo tolerance\nAtrod līdzīgus vārdus]

    FILT[Filtri\nKategorija, zīmols, pieejamība]

    PRICE[Cenu filtrs\nMin/max]

    SCORE[Relevance score\nSvarīguma aprēķins]

    SORT[Kārtošana\nRelevance/cena/reitings]

    RES[Rezultāti]

    U --> T1 --> T2 --> IDX --> TYPO --> FILT --> PRICE --> SCORE --> SORT --> RES
end

%% =====================================================
%% DATA MODEL + EXPLANATION
%% =====================================================
subgraph Datu_modelis
    P[Product\nProdukts:\nID, nosaukums, cena,\nkategorija, zīmols, reitings]

    SR[SearchResult\nProdukts + score]

    P --> SR
end

%% =====================================================
%% COMPONENTS + EXPLANATION
%% =====================================================
subgraph Komponentes
    C1[SearchEngine\nGalvenā loģika]
    C2[Trie\nAuto-complete]
    C3[DataGenerator\nTesta dati]
    C4[Index\nInverted Index struktūra]
end

C1 --> C2
C1 --> C4
C1 --> P

%% =====================================================
%% RELEVANCE FORMULA + EXPLANATION
%% =====================================================
subgraph Relevance
    R1[Score formula]

    R2[3x title match\nNosaukums svarīgāks]
    R3[1x description\nApraksts mazāk svarīgs]
    R4[+ rating\nAugstāks reitings = labāk]
    R5[+ popularity\nPopulārāks = augstāk]
    R6[+ freshness\nJaunāks produkts]

    R1 --> R2
    R1 --> R3
    R1 --> R4
    R1 --> R5
    R1 --> R6
end

%% =====================================================
%% COMPLEXITY + EXPLANATION
%% =====================================================
subgraph Kompleksitate
    X1[Indeksēšana O(N*T)\nN=produkti, T=vārdi]
    X2[Meklēšana O(r log r)\nr=kandidāti]
    X3[Autocomplete O(p+s)\np=prefikss]
    X4[Price search O(log n)\nbinary search]
end

%% =====================================================
%% TESTING + EXPLANATION
%% =====================================================
subgraph Testesana
    TST1[10K produkti\nReāli dati]
    TST2[Performance tests\nLaika mērīšana]
    TST3[Precizitāte\nVai rezultāti pareizi]
    TST4[Filtru tests\nKategorija, cena utt]
end

%% =====================================================
%% CONNECTIONS
%% =====================================================
Algoritmi --> Meklesanas_process
Funkcionalas_prasibas --> Meklesanas_process
Nefunkcionalas_prasibas --> Kompleksitate
Komponentes --> Meklesanas_process
Testesana --> Meklesanas_process
Relevance --> Meklesanas_process
Prefiksi_un_AutoComplete --> Algoritmi