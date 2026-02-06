// Simple front-end library for the library app
// Book class and in-memory structures

class Book {
	constructor(id, title, author, isbn) {
		this.id = id;
		this.title = title;
		this.author = author;
		this.isbn = isbn;
	}
}

const API_BASE = 'http://127.0.0.1:5002';

const state = {
	books: [], // ordered list
	byIsbn: new Map(), // O(1) lookup by ISBN
};

function renderBooks(list) {
	const ul = document.getElementById('books');
	ul.innerHTML = '';
	for (const b of list) {
		const li = document.createElement('li');
		li.textContent = `${b.title} — ${b.author} (ISBN: ${b.isbn})`;
		const del = document.createElement('button');
		del.textContent = 'Dzēst';
		del.style.marginLeft = '8px';
		del.onclick = async () => {
			const ok = confirm('Dzēst grāmatu?');
			if (!ok) return;
			await deleteBook(b.isbn);
			await loadBooks();
		};
		li.appendChild(del);
		ul.appendChild(li);
	}
}

async function loadBooks() {
	try {
		const res = await fetch(API_BASE + '/books');
		const data = await res.json();
		state.books = data.books.map(b => new Book(b.id, b.title, b.author, b.isbn));
		state.byIsbn.clear();
		for (const b of state.books) state.byIsbn.set(b.isbn, b);
		renderBooks(state.books);
	} catch (e) {
		console.error('loadBooks error', e);
	}
}

async function addBook(title, author, isbn) {
	const payload = { title, author, isbn };
	const res = await fetch(API_BASE + '/add_book', {
		method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload)
	});
	if (!res.ok) {
		const err = await res.json().catch(()=>({error:'unknown'}));
		alert('Neizdevās pievienot: ' + (err.error || JSON.stringify(err)));
		return false;
	}
	return true;
}

async function deleteBook(isbn) {
	const res = await fetch(API_BASE + '/delete_book', {
		method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ isbn })
	});
	if (!res.ok) {
		const err = await res.json().catch(()=>({error:'unknown'}));
		alert('Neizdevās dzēst: ' + (err.error || JSON.stringify(err)));
		return false;
	}
	return true;
}

function searchLocal(q) {
	q = (q || '').trim().toLowerCase();
	if (!q) return state.books;
	return state.books.filter(b => b.title.toLowerCase().includes(q) || b.author.toLowerCase().includes(q));
}

document.addEventListener('DOMContentLoaded', () => {
	document.getElementById('addBtn').addEventListener('click', async () => {
		const title = document.getElementById('title').value.trim();
		const author = document.getElementById('author').value.trim();
		const isbn = document.getElementById('isbn').value.trim();
		if (!title || !author || !isbn) { alert('Lūdzu aizpildiet visu'); return; }
		const ok = await addBook(title, author, isbn);
		if (ok) {
			document.getElementById('title').value = '';
			document.getElementById('author').value = '';
			document.getElementById('isbn').value = '';
			await loadBooks();
		}
	});

	document.getElementById('searchBtn').addEventListener('click', () => {
		const q = document.getElementById('q').value;
		renderBooks(searchLocal(q));
	});

	document.getElementById('listBtn').addEventListener('click', () => {
		renderBooks(state.books);
	});

	loadBooks();
});

// Exported for debugging if needed
window._lib = { state, loadBooks, addBook, deleteBook, searchLocal };
