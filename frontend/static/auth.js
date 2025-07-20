//si, es necesario el backend url
const BACKEND_URL = 'http://localhost:5000';

const registerForm = document.getElementById('registerForm');
if (registerForm) {
    registerForm.addEventListener('submit', async e => {
        e.preventDefault();
        const data = {
            username: e.target.username.value,
            password: e.target.password.value,
            confirm_password: e.target.confirm_password.value
        };
        const res = await fetch(`${BACKEND_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        const errorBox = document.getElementById("error-message");
        // fragmento dentro del submit del registerForm
        if (!res.ok) {
            errorBox.textContent = result.error || "Error al registrarse";
            errorBox.style.display = "block";
        } else {
            if (result.access_token) {
                localStorage.setItem('token', result.access_token);
                console.log('Token guardado en localStorage');
                window.location.href = `http://localhost:5500/frontend/templates/notes.html`;
            } else {
                window.location.href = `http://localhost:5500/frontend/templates/login.html`;
            }
        }
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

        const result = await res.json();
        const errorBox = document.getElementById("error-message");

        if (!res.ok) {
            errorBox.textContent = result.error || "Error al iniciar sesión";
            errorBox.style.display = "block";
        } else {
            if (result.access_token) {
                localStorage.setItem('token', result.access_token);
                console.log('Token guardado en localStorage');
                window.location.href = `http://localhost:5500/frontend/templates/notes.html`;
            } else {
                errorBox.textContent = "Token no recibido";
                errorBox.style.display = "block";
                console.error('No se recibió token');
            }
        }
    });
}

