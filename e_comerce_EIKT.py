import argparse
import bisect
import json
import random
import re
import time
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from difflib import get_close_matches
from typing import Dict, List, Set, Optional, Tuple


# MODEĻI


@dataclass
class Product:
    """
    Produkta datu modelis.
    """
    id: int
    nosaukums: str
    apraksts: str
    cena: float
    kategorija: str
    zimols: str
    pieejamiba: bool
    reitings: float
    pievienosanas_datums: str
    popularitate: int


@dataclass
class SearchResult:
    
    """Meklēšanas rezultāta modelis ar score relevances kārtošanai."""
    
    product: Product
    score: float


# PALĪGFUNKCIJAS

def normalize_text(text: str) -> str:
    """
    Normalizē tekstu:
    - lowercase
    - atstāj tikai burtus, ciparus un atstarpes
    """
    text = text.lower().strip()
    text = re.sub(r"[^a-zA-Z0-9āčēģīķļņōŗšūž\s\-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize(text: str) -> List[str]:
    
    """Sadala tekstu tokenos."""
    
    normalized = normalize_text(text)
    return [token for token in normalized.split() if token]


def safe_float(value: Optional[str], default: Optional[float] = None) -> Optional[float]:
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")

# TRIE AUTO-COMPLETE

class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.is_end: bool = False
        self.frequency: int = 0


class Trie:
    
    """Trie struktūra auto-complete funkcijai."""
    
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, frequency: int = 1) -> None:
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True
        node.frequency += frequency

    def _collect(self, node: TrieNode, prefix: str, output: List[Tuple[str, int]]) -> None:
        if node.is_end:
            output.append((prefix, node.frequency))

        for ch, child in node.children.items():
            self._collect(child, prefix + ch, output)

    def autocomplete(self, prefix: str, limit: int = 10) -> List[str]:
        prefix = normalize_text(prefix)
        node = self.root

        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]

        words: List[Tuple[str, int]] = []
        self._collect(node, prefix, words)
        words.sort(key=lambda x: (-x[1], x[0]))
        return [word for word, _ in words[:limit]]


# MEKLĒŠANAS SISTĒMA

class SearchEngine:
    """
    E-komercijas produktu meklēšanas sistēma.

    Izmantotās struktūras:
    - Inverted index teksta meklēšanai
    - Trie auto-complete
    - Dict / Set filtrēšanai
    - Sakārtots cenu saraksts diapazona vaicājumiem
    """
    def __init__(self):
        self.products_by_id: Dict[int, Product] = {}

        # Inverted index
        self.title_index: Dict[str, Set[int]] = defaultdict(set)
        self.description_index: Dict[str, Set[int]] = defaultdict(set)

        # Filtri
        self.category_index: Dict[str, Set[int]] = defaultdict(set)
        self.brand_index: Dict[str, Set[int]] = defaultdict(set)
        self.availability_index: Dict[bool, Set[int]] = defaultdict(set)

        # Cenu diapazonam
        self.price_list: List[Tuple[float, int]] = []
        self.price_values_only: List[float] = []

        # Trie auto-complete
        self.trie = Trie()
        self.term_frequency: Counter = Counter()

        # Terminu saraksts typo tolerance vajadzībām
        self.all_terms: Set[str] = set()

    def index_products(self, products: List[Product]) -> None:
        
        """Izveido indeksus no produktu saraksta."""
        
        self.products_by_id.clear()
        self.title_index.clear()
        self.description_index.clear()
        self.category_index.clear()
        self.brand_index.clear()
        self.availability_index.clear()
        self.price_list.clear()
        self.price_values_only.clear()
        self.trie = Trie()
        self.term_frequency.clear()
        self.all_terms.clear()

        for product in products:
            self.products_by_id[product.id] = product

            title_tokens = tokenize(product.nosaukums)
            desc_tokens = tokenize(product.apraksts)

            for token in title_tokens:
                self.title_index[token].add(product.id)
                self.term_frequency[token] += 3
                self.all_terms.add(token)

            for token in desc_tokens:
                self.description_index[token].add(product.id)
                self.term_frequency[token] += 1
                self.all_terms.add(token)

            self.category_index[normalize_text(product.kategorija)].add(product.id)
            self.brand_index[normalize_text(product.zimols)].add(product.id)
            self.availability_index[product.pieejamiba].add(product.id)

            self.price_list.append((product.cena, product.id))

        self.price_list.sort(key=lambda x: x[0])
        self.price_values_only = [price for price, _ in self.price_list]

        for term, freq in self.term_frequency.items():
            self.trie.insert(term, freq)

    def _get_candidate_ids_for_price_range(self, min_price: Optional[float], max_price: Optional[float]) -> Set[int]:
        if min_price is None and max_price is None:
            return set(self.products_by_id.keys())

        low = min_price if min_price is not None else float("-inf")
        high = max_price if max_price is not None else float("inf")

        left = bisect.bisect_left(self.price_values_only, low)
        right = bisect.bisect_right(self.price_values_only, high)

        return {product_id for _, product_id in self.price_list[left:right]}

    def _get_typo_suggestions(self, token: str, max_suggestions: int = 3) -> List[str]:
        
        """Atrod līdzīgus terminus typo tolerance nodrošināšanai."""
        
        if token in self.all_terms:
            return [token]

        matches = get_close_matches(token, list(self.all_terms), n=max_suggestions, cutoff=0.75)
        return matches

    def autocomplete(self, prefix: str, limit: int = 10) -> List[str]:
        return self.trie.autocomplete(prefix, limit)

    def search(
        self,
        query: str,
        category: Optional[str] = None,
        brand: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        available_only: bool = False,
        sort_by: str = "relevance",
        limit: int = 20
    ) -> List[SearchResult]:
        
        """Galvenā meklēšanas funkcija."""
        
        if limit <= 0:
            raise ValueError("limit jābūt lielākam par 0")

        query_tokens = tokenize(query)
        if not query_tokens:
            raise ValueError("Meklēšanas vaicājums nedrīkst būt tukšs")

        candidate_ids: Set[int] = set()
        score_map: Dict[int, float] = defaultdict(float)

        # Meklēšana ar typo tolerance
        for token in query_tokens:
            expanded_terms = self._get_typo_suggestions(token)

            for term in expanded_terms:
                title_matches = self.title_index.get(term, set())
                desc_matches = self.description_index.get(term, set())

                for product_id in title_matches:
                    candidate_ids.add(product_id)
                    score_map[product_id] += 3.0

                for product_id in desc_matches:
                    candidate_ids.add(product_id)
                    score_map[product_id] += 1.0

        # Ja neko neatrod, atgriež tukšu
        if not candidate_ids:
            return []

        # Kategorijas filtrs
        if category:
            category_ids = self.category_index.get(normalize_text(category), set())
            candidate_ids &= category_ids

        # Zīmola filtrs
        if brand:
            brand_ids = self.brand_index.get(normalize_text(brand), set())
            candidate_ids &= brand_ids

        # Pieejamība
        if available_only:
            candidate_ids &= self.availability_index.get(True, set())

        # Cenu diapazons
        price_ids = self._get_candidate_ids_for_price_range(min_price, max_price)
        candidate_ids &= price_ids

        results: List[SearchResult] = []

        now = datetime.now()

        for product_id in candidate_ids:
            product = self.products_by_id[product_id]
            score = score_map[product_id]

            # Papildu relevance faktori
            score += product.reitings * 0.35
            score += min(product.popularitate / 1000.0, 2.0)

            age_days = (now - parse_date(product.pievienosanas_datums)).days
            freshness_bonus = max(0.0, 1.0 - age_days / 3650.0)
            score += freshness_bonus

            results.append(SearchResult(product=product, score=score))

        # Kārtošana
        if sort_by == "relevance":
            results.sort(key=lambda r: (-r.score, -r.product.reitings, r.product.cena))
        elif sort_by == "price_asc":
            results.sort(key=lambda r: (r.product.cena, -r.score))
        elif sort_by == "price_desc":
            results.sort(key=lambda r: (-r.product.cena, -r.score))
        elif sort_by == "rating":
            results.sort(key=lambda r: (-r.product.reitings, -r.score))
        elif sort_by == "date":
            results.sort(key=lambda r: (r.product.pievienosanas_datums,), reverse=True)
        else:
            raise ValueError("Nepareizs sort_by. Izmanto: relevance, price_asc, price_desc, rating, date")

        return results[:limit]



# TESTA DATU ĢENERATORS


class DataGenerator:
    """
    Ģenerē reprezentatīvus testa datus.
    """
    CATEGORIES = [
        "Elektronika", "Apģērbs", "Mājas preces", "Sports",
        "Skaistumkopšana", "Datori", "Aksesuāri", "Bērniem"
    ]

    BRANDS = [
        "Apple", "Samsung", "Nike", "Adidas", "Sony", "Lenovo",
        "Xiaomi", "Bosch", "Philips", "LG", "Puma", "Asus"
    ]

    ADJECTIVES = [
        "Premium", "Moderns", "Jaudīgs", "Kompakts", "Bezvadu",
        "Ergonomisks", "Profesionāls", "Universāls", "Stilīgs", "Ērts"
    ]

    PRODUCT_TYPES = [
        "telefons", "dators", "austiņas", "ledusskapis", "apavi",
        "jaka", "pulkstenis", "kamera", "putekļsūcējs", "monitoris",
        "krēsls", "mugursoma", "blenderis", "pele", "klaviatūra"
    ]

    DESCRIPTION_WORDS = [
        "augsta", "kvalitāte", "izturīgs", "ātrs", "ērts", "piemērots",
        "ikdienai", "darbam", "spēlēm", "mājai", "ceļošanai", "kompakts",
        "labs", "veiktspēja", "moderns", "dizains", "energoefektīvs",
        "uzticams", "praktisks", "profesionāls"
    ]

    @staticmethod
    def generate_products(count: int = 10000) -> List[Product]:
        products: List[Product] = []

        for i in range(1, count + 1):
            brand = random.choice(DataGenerator.BRANDS)
            adjective = random.choice(DataGenerator.ADJECTIVES)
            product_type = random.choice(DataGenerator.PRODUCT_TYPES)
            category = random.choice(DataGenerator.CATEGORIES)

            nosaukums = f"{brand} {adjective} {product_type} {random.randint(100, 999)}"

            description_length = random.randint(10, 22)
            description_words = random.choices(DataGenerator.DESCRIPTION_WORDS, k=description_length)
            apraksts = " ".join(description_words)

            cena = round(random.uniform(5.0, 3000.0), 2)
            pieejamiba = random.choice([True, False])
            reitings = round(random.uniform(1.0, 5.0), 1)
            popularitate = random.randint(1, 5000)

            random_days_ago = random.randint(0, 365 * 3)
            date_value = (datetime.now() - timedelta(days=random_days_ago)).strftime("%Y-%m-%d")

            products.append(
                Product(
                    id=i,
                    nosaukums=nosaukums,
                    apraksts=apraksts,
                    cena=cena,
                    kategorija=category,
                    zimols=brand,
                    pieejamiba=pieejamiba,
                    reitings=reitings,
                    pievienosanas_datums=date_value,
                    popularitate=popularitate
                )
            )

        return products



# FAILU DARBS


def save_products_to_json(products: List[Product], filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump([asdict(product) for product in products], f, ensure_ascii=False, indent=2)


def load_products_from_json(filepath: str) -> List[Product]:
    with open(filepath, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    products = []
    for item in raw_data:
        products.append(Product(**item))
    return products



# VEIKTSPĒJAS TESTI


def benchmark_engine(engine: SearchEngine) -> None:
    """
    Veiktspējas testu funkcija.
    """
    test_queries = [
        ("apple", None, None, None, None, False, "relevance"),
        ("nike shoes", "Apģērbs", "Nike", 20, 300, True, "relevance"),
        ("wireless", None, None, None, None, False, "rating"),
        ("samsung phone", "Elektronika", "Samsung", 50, 1500, True, "price_asc"),
        ("premium monitor", "Datori", None, 100, 2000, False, "price_desc"),
        ("sony", None, "Sony", None, None, False, "rating"),
        ("jaudīgs dators", "Datori", "Lenovo", 300, 2500, True, "relevance"),
        ("bezvadu austiņas", "Elektronika", None, 10, 600, True, "relevance"),
        ("ergonomisks krēsls", "Mājas preces", None, 40, 800, False, "price_asc"),
        ("adidas jaka", "Apģērbs", "Adidas", 15, 400, True, "date"),
    ]

    times = []

    print("\n--- VEIKTSPĒJAS TESTS ---")
    for i, (query, category, brand, min_p, max_p, available, sort_by) in enumerate(test_queries, start=1):
        start = time.perf_counter()
        results = engine.search(
            query=query,
            category=category,
            brand=brand,
            min_price=min_p,
            max_price=max_p,
            available_only=available,
            sort_by=sort_by,
            limit=10
        )
        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000
        times.append(elapsed_ms)

        print(f"Tests {i}: '{query}' -> {len(results)} rezultāti, {elapsed_ms:.3f} ms")

    avg_time = sum(times) / len(times)
    print(f"\nVidējais meklēšanas laiks: {avg_time:.3f} ms")
    print(f"Ātrākais meklējums: {min(times):.3f} ms")
    print(f"Lēnākais meklējums: {max(times):.3f} ms")

    if avg_time < 200:
        print("Secinājums: prasība < 200ms ir izpildīta.")
    else:
        print("Secinājums: prasība < 200ms nav izpildīta.")



# REZULTĀTU IZVADE


def print_results(results: List[SearchResult]) -> None:
    if not results:
        print("Nav atrasti rezultāti.")
        return

    print(f"\nAtrasti {len(results)} rezultāti:\n")
    for i, result in enumerate(results, start=1):
        p = result.product
        print(f"{i}. [{p.id}] {p.nosaukums}")
        print(f"   Kategorija: {p.kategorija}")
        print(f"   Zīmols: {p.zimols}")
        print(f"   Cena: {p.cena:.2f} EUR")
        print(f"   Pieejams: {'Jā' if p.pieejamiba else 'Nē'}")
        print(f"   Reitings: {p.reitings}")
        print(f"   Datums: {p.pievienosanas_datums}")
        print(f"   Score: {result.score:.2f}")
        print(f"   Apraksts: {p.apraksts[:100]}...")
        print()



# INTERAKTĪVA IZVĒLNE


def run_interactive_menu(engine: SearchEngine) -> None:
    while True:
        print("\n=== E-komercijas produktu meklēšanas sistēma ===")
        print("1. Meklēt produktus")
        print("2. Auto-complete")
        print("3. Palaist benchmark")
        print("4. Iziet")

        choice = input("Izvēlies darbību: ").strip()

        if choice == "1":
            try:
                query = input("Meklēšanas teksts: ").strip()
                category = input("Kategorija (Enter ja nav): ").strip() or None
                brand = input("Zīmols (Enter ja nav): ").strip() or None

                min_price_input = input("Min cena (Enter ja nav): ").strip()
                max_price_input = input("Max cena (Enter ja nav): ").strip()

                min_price = safe_float(min_price_input, None) if min_price_input else None
                max_price = safe_float(max_price_input, None) if max_price_input else None

                available_only = input("Tikai pieejamie? (y/n): ").strip().lower() == "y"
                sort_by = input("Kārtošana (relevance/price_asc/price_desc/rating/date): ").strip() or "relevance"

                start = time.perf_counter()
                results = engine.search(
                    query=query,
                    category=category,
                    brand=brand,
                    min_price=min_price,
                    max_price=max_price,
                    available_only=available_only,
                    sort_by=sort_by,
                    limit=10
                )
                elapsed_ms = (time.perf_counter() - start) * 1000

                print_results(results)
                print(f"Meklēšanas laiks: {elapsed_ms:.3f} ms")

            except Exception as e:
                print(f"Kļūda: {e}")

        elif choice == "2":
            prefix = input("Ievadi prefiksu: ").strip()
            suggestions = engine.autocomplete(prefix, limit=10)

            if suggestions:
                print("\nIeteikumi:")
                for item in suggestions:
                    print(f"- {item}")
            else:
                print("Nav ieteikumu.")

        elif choice == "3":
            benchmark_engine(engine)

        elif choice == "4":
            print("Programma beidzas.")
            break

        else:
            print("Nepareiza izvēle.")



# GALVENĀ FUNKCIJA


def main():
    parser = argparse.ArgumentParser(description="E-komercijas produktu meklēšanas sistēma")
    parser.add_argument("--generate", type=int, help="Ģenerē N produktus")
    parser.add_argument("--save", type=str, help="Saglabā produktus JSON failā")
    parser.add_argument("--load", type=str, help="Ielādē produktus no JSON faila")
    parser.add_argument("--search", type=str, help="Meklēšanas teksts")
    parser.add_argument("--category", type=str, help="Kategorijas filtrs")
    parser.add_argument("--brand", type=str, help="Zīmola filtrs")
    parser.add_argument("--min_price", type=float, help="Minimālā cena")
    parser.add_argument("--max_price", type=float, help="Maksimālā cena")
    parser.add_argument("--available", action="store_true", help="Rādīt tikai pieejamos produktus")
    parser.add_argument("--sort", type=str, default="relevance", help="relevance/price_asc/price_desc/rating/date")
    parser.add_argument("--autocomplete", type=str, help="Auto-complete prefikss")
    parser.add_argument("--benchmark", action="store_true", help="Palaist veiktspējas testu")
    parser.add_argument("--interactive", action="store_true", help="Palaist interaktīvo režīmu")

    args = parser.parse_args()

    products: List[Product] = []

    try:
        if args.load:
            products = load_products_from_json(args.load)
            print(f"Ielādēti {len(products)} produkti no faila '{args.load}'")
        elif args.generate:
            products = DataGenerator.generate_products(args.generate)
            print(f"Ģenerēti {len(products)} produkti")
        else:
            # Noklusējuma variants, lai programma strādātu uzreiz
            products = DataGenerator.generate_products(10000)
            print("Ģenerēti 10000 noklusējuma produkti")

        if args.save:
            save_products_to_json(products, args.save)
            print(f"Produkti saglabāti failā '{args.save}'")

        engine = SearchEngine()

        start_index = time.perf_counter()
        engine.index_products(products)
        end_index = time.perf_counter()

        print(f"Indekss izveidots {(end_index - start_index) * 1000:.3f} ms")

        if args.autocomplete:
            suggestions = engine.autocomplete(args.autocomplete, limit=10)
            print("\nAuto-complete rezultāti:")
            for s in suggestions:
                print("-", s)

        if args.search:
            start_search = time.perf_counter()
            results = engine.search(
                query=args.search,
                category=args.category,
                brand=args.brand,
                min_price=args.min_price,
                max_price=args.max_price,
                available_only=args.available,
                sort_by=args.sort,
                limit=10
            )
            end_search = time.perf_counter()

            print_results(results)
            print(f"Meklēšanas laiks: {(end_search - start_search) * 1000:.3f} ms")

        if args.benchmark:
            benchmark_engine(engine)

        if args.interactive:
            run_interactive_menu(engine)

        # Ja nav dots neviens darbības parametrs, ieslēdz interaktīvo
        if not any([
            args.autocomplete,
            args.search,
            args.benchmark,
            args.interactive
        ]):
            run_interactive_menu(engine)

    except FileNotFoundError as e:
        print(f"Fails nav atrasts: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON nolasīšanas kļūda: {e}")
    except ValueError as e:
        print(f"Validācijas kļūda: {e}")
    except Exception as e:
        print(f"Nezināma kļūda: {e}")


if __name__ == "__main__":
    main()