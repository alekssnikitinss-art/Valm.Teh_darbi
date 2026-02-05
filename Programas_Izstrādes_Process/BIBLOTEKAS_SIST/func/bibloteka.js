// Simple frontend that talks to a local backend API
const API_HOST = 'http://127.0.0.1:5001'; // local Flask API host

const qs = s => document.querySelector(s);
const qsa = s => document.querySelectorAll(s);

let currentUser = null;

async function api(path, opts={}){
    try{
        const res = await fetch(path, opts);
        return await res.json();
    }catch(e){
        console.error('API error', e);
        return {error: 'no-connection'};
    }
}

async function loadBooks(){
    const booksList = qs('#books-list');
    booksList.textContent = 'Ielādē...';
    const res = await api(API_HOST + '/data.json');
    if(res && Array.isArray(res.books)){
        renderBooks(res.books);
    }else{
        booksList.innerHTML = '<i>Nevar ielādēt grāmatas (palaižiet API vai atveriet datu failu)</i>';
    }
}

function renderBooks(books){
    const root = qs('#books-list');
    if(books.length === 0){ root.innerHTML = '<i>Nav grāmatu</i>'; return }
    root.innerHTML = '';
    books.forEach(b => {
        const div = document.createElement('div');
        div.className = 'book';
        div.innerHTML = `<strong>${escapeHtml(b.title)}</strong> — ${escapeHtml(b.author)} <br> <small>ISBN: ${escapeHtml(b.isbn)}</small>`;
        const btn = document.createElement('button');
        if(b.reserved){
            btn.textContent = 'Rezervēta'; btn.disabled = true;
            const span = document.createElement('div'); span.className='reserved-by'; span.textContent = 'Rezervēja: '+(b.reserved_by||'—'); div.appendChild(span);
        }else{
            btn.textContent = 'Rezervēt';
            btn.onclick = () => reserveBook(b.isbn);
        }
        div.appendChild(btn);
        root.appendChild(div);
    })
}

function escapeHtml(s){ if(!s) return ''; return s.replace(/[&<>"]/g, c=> ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])) }

async function reserveBook(isbn){
    if(!currentUser){
        alert('Lūdzu piesakieties, lai rezervētu grāmatu.');
        return;
    }
    const res = await api(API_HOST + '/api/reserve', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({isbn, user: currentUser})});
    if(res && res.ok){
        await loadBooks();
        alert('Grāmata rezervēta');
    }else{
        alert('Neizdevās rezervēt: '+(res && res.error || 'unknown'));
    }
}

async function doLogin(){
    const u = qs('#username').value.trim();
    const p = qs('#password').value.trim();
    if(!u || !p){ qs('#login-status').textContent = 'ievadiet lietotāju un paroli'; return }
    const res = await api(API_HOST + '/api/login', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username:u,password:p})});
    if(res && res.ok){
        currentUser = u;
        qs('#login-status').textContent = 'Ielogots kā '+u;
        if(res.admin) showAdmin();
        // save to cache via backend
    await api(API_HOST + '/api/cache_user', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username:u,password:p})});
    }else{
        qs('#login-status').textContent = 'Nepareiza parole';
    }
}

function showAdmin(){
    qs('#admin-section').classList.remove('hidden');
}

async function addBook(){
    const title = qs('#new-title').value.trim();
    const author = qs('#new-author').value.trim();
    const isbn = qs('#new-isbn').value.trim();
    if(!title||!author||!isbn){ alert('Aizpildiet visus laukus'); return }
    const res = await api(API_HOST + '/api/admin/add_book', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({title,author,isbn})});
    if(res && res.ok){
        qs('#new-title').value=''; qs('#new-author').value=''; qs('#new-isbn').value='';
        await loadBooks();
        alert('Grāmata pievienota');
    }else{
        alert('Neizdevās pievienot: '+(res && res.error || 'unknown'));
    }
}

document.addEventListener('DOMContentLoaded', ()=>{
    qs('#btn-login').addEventListener('click', doLogin);
    qs('#btn-add-book').addEventListener('click', addBook);
    loadBooks();
});

// small helper endpoints fallback when API is run at ../database/api
// the API will implement the endpoints used above
