const API_BASE = 'http://localhost:5001';
const userForm = document.getElementById('userForm');
const userTable = document.getElementById('userTable').querySelector('tbody');
const cancelBtn = document.getElementById('cancelBtn');

function loadUsers() {
    fetch(`${API_BASE}/users`)
        .then(response => response.json())
        .then(data => {
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
        .then(response => response.json())
        .then(data => {
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
            .then(response => response.json())
            .then(data => {
                alert(data.pesan);
                loadUsers();
            })
            .catch(error => console.error('Error:', error));
    }
}

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
    .then(response => response.json())
    .then(data => {
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

// Load users on page load
loadUsers();
