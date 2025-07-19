//si, es necesario el backend url
const BACKEND_URL = 'http://localhost:5000';

const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async e => {
        e.preventDefault();
        const data = {
            username: e.target.username.value,
            password: e.target.password.value
        };
        const res = await fetch(`${BACKEND_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const json = await res.json();
        console.log(json);
    });
}

const loginForm = document.getElementById('loginForm');

if (loginForm) {
    loginForm.addEventListener('submit', async e => {
        e.preventDefault();
        
        const data = {
            username: e.target.username.value,
            password: e.target.password.value
        };

        const res = await fetch(`${BACKEND_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const json = await res.json();
        console.log(json); // Aquí te llega { "access_token": "..." }

        if (json.access_token) {
            localStorage.setItem('token', json.access_token);
            console.log('Token guardado en localStorage');
        } else {
            console.error('No se recibió token');
        }
    });
}
