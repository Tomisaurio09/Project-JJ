    document.getElementById('loginForm').addEventListener('submit', async e => {
        e.preventDefault();
        const data = {
        username: e.target.username.value,
        password: e.target.password.value
        };
        const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
        });
        const json = await res.json();
        console.log(json);
    });