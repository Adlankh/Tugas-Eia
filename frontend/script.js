const API_BASE = 'http://localhost:5001';
const loginForm = document.getElementById('loginForm');
const userForm = document.getElementById('userForm');
const userTable = document.getElementById('userTable').querySelector('tbody');
const cancelBtn = document.getElementById('cancelBtn');
const loginSection = document.getElementById('loginSection');
const managementSection = document.getElementById('managementSection');
const logoutBtn = document.getElementById('logoutBtn');

function checkAuth() {
    fetch(`${API_BASE}/check-auth`)
        .then(response => response.json())
        .then(data => {
            if (data.authenticated) {
                loginSection.style.display = 'none';
                managementSection.style.display = 'block';
                loadUsers();
            } else {
                loginSection.style.display = 'block';
                managementSection.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error checking auth:', error);
            loginSection.style.display = 'block';
            managementSection.style.display = 'none';
        });
}

function loadUsers() {
    fetch(`${API_BASE}/users`)
        .then(response => {
            if (response.status === 401) {
                alert('Sesi login telah berakhir. Silakan login kembali.');
                checkAuth();
                return;
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;
            userTable.innerHTML = '';
            data.data.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${user.id}</td>
                    <td>${user.nama}</td>
                    <td>${user.email}</td>
                    <td>${user.tipe_pengguna}</td>
                    <td>
                        <button class="action-btn edit-btn" onclick="editUser(${user.id})">Edit</button>
                        <button class="action-btn delete-btn" onclick="deleteUser(${user.id})">Hapus</button>
                    </td>
                `;
                userTable.appendChild(row);
            });
        })
        .catch(error => console.error('Error:', error));
}

function editUser(id) {
    fetch(`${API_BASE}/users/${id}`)
        .then(response => {
            if (response.status === 401) {
                alert('Sesi login telah berakhir. Silakan login kembali.');
                checkAuth();
                return;
            }
            return response.json();
        })
        .then(data => {
            if (!data) return;
            const user = data.data;
            document.getElementById('userId').value = user.id;
            document.getElementById('nama').value = user.nama;
            document.getElementById('email').value = user.email;
            document.getElementById('tipePengguna').value = user.tipe_pengguna;
            document.getElementById('password').value = ''; // Kosongkan password untuk keamanan
            cancelBtn.style.display = 'inline-block';
        })
        .catch(error => console.error('Error:', error));
}

function deleteUser(id) {
    if (confirm('Apakah Anda yakin ingin menghapus pengguna ini?')) {
        fetch(`${API_BASE}/users/${id}`, { method: 'DELETE' })
            .then(response => {
                if (response.status === 401) {
                    alert('Sesi login telah berakhir. Silakan login kembali.');
                    checkAuth();
                    return;
                }
                return response.json();
            })
            .then(data => {
                if (!data) return;
                alert(data.pesan);
                loadUsers();
            })
            .catch(error => console.error('Error:', error));
    }
}

loginForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const loginData = {
        email: document.getElementById('loginEmail').value,
        password: document.getElementById('loginPassword').value
    };

    fetch(`${API_BASE}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(loginData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.pesan);
        if (data.pesan === 'Login berhasil') {
            checkAuth();
        }
    })
    .catch(error => console.error('Error:', error));
});

logoutBtn.addEventListener('click', function() {
    fetch(`${API_BASE}/logout`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            alert(data.pesan);
            checkAuth();
        })
        .catch(error => console.error('Error:', error));
});

userForm.addEventListener('submit', function(e) {
    e.preventDefault();
    const userId = document.getElementById('userId').value;
    const userData = {
        nama: document.getElementById('nama').value,
        email: document.getElementById('email').value,
        tipe_pengguna: document.getElementById('tipePengguna').value,
        password: document.getElementById('password').value
    };

    const method = userId ? 'PUT' : 'POST';
    const url = userId ? `${API_BASE}/users/${userId}` : `${API_BASE}/users`;

    fetch(url, {
        method: method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    })
    .then(response => {
        if (response.status === 401) {
            alert('Sesi login telah berakhir. Silakan login kembali.');
            checkAuth();
            return;
        }
        return response.json();
    })
    .then(data => {
        if (!data) return;
        alert(data.pesan);
        userForm.reset();
        document.getElementById('userId').value = '';
        cancelBtn.style.display = 'none';
        loadUsers();
    })
    .catch(error => console.error('Error:', error));
});

cancelBtn.addEventListener('click', function() {
    userForm.reset();
    document.getElementById('userId').value = '';
    cancelBtn.style.display = 'none';
});

// Check auth on page load
checkAuth();
