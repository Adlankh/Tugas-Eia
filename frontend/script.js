// === KONFIGURASI BACKEND API ===
const API_URL = "http://127.0.0.1:5001"; // samakan port dengan Flask

let users = [];

// === AMBIL DATA USER DARI BACKEND ===
async function fetchUsers() {
  try {
    const res = await fetch(`${API_URL}/api/users`);
    users = await res.json();
    renderTable(users);
  } catch (err) {
    console.error("Gagal mengambil data pengguna:", err);
  }
}

// === RENDER TABEL PENGGUNA ===
function renderTable(data) {
  const tableBody = document.querySelector("#userTable tbody");
  tableBody.innerHTML = "";

  data.forEach((user) => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${user.id}</td>
      <td>${user.nama}</td>
      <td>${user.email}</td>
      <td>${user.tipe_pengguna}</td>
      <td>
        <button class="editBtn btn btn-primary btn-sm" data-id="${user.id}">Edit</button>
        <button class="deleteBtn btn btn-danger btn-sm" data-id="${user.id}">Hapus</button>
      </td>
    `;
    tableBody.appendChild(row);
  });
}

// === TAMBAH PENGGUNA ===
document.querySelector("#userForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const newUser = {
    nama: document.querySelector("#nama").value,
    email: document.querySelector("#email").value,
    password: document.querySelector("#password").value,
    tipe_pengguna: document.querySelector("#tipePengguna").value,
  };

  try {
    const res = await fetch(`${API_URL}/api/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newUser),
    });

    const result = await res.json();
    alert(result.pesan);
    fetchUsers();
    document.querySelector("#userForm").reset();
  } catch (err) {
    console.error("Gagal menyimpan pengguna:", err);
  }
});

// === FUNGSI EDIT DAN HAPUS ===
document.addEventListener("click", async (e) => {
  const id = e.target.dataset.id;

  // === HAPUS ===
  if (e.target.classList.contains("deleteBtn")) {
    if (confirm("Yakin ingin menghapus pengguna ini?")) {
      try {
        const res = await fetch(`${API_URL}/api/users/${id}`, { method: "DELETE" });
        const result = await res.json();
        alert(result.pesan);
        fetchUsers();
      } catch (err) {
        console.error("Gagal menghapus pengguna:", err);
      }
    }
  }

  // === EDIT ===
  if (e.target.classList.contains("editBtn")) {
    const user = users.find((u) => u.id == id);
    if (user) {
      document.querySelector("#nama").value = user.nama;
      document.querySelector("#email").value = user.email;
      document.querySelector("#tipePengguna").value = user.tipe_pengguna;
      document.querySelector("#password").value = "";

      document.querySelector("#userForm").onsubmit = async (event) => {
        event.preventDefault();
        const updatedUser = {
          nama: document.querySelector("#nama").value,
          email: document.querySelector("#email").value,
          tipe_pengguna: document.querySelector("#tipePengguna").value,
          password: document.querySelector("#password").value,
        };

        try {
          const res = await fetch(`${API_URL}/api/users/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatedUser),
          });
          const result = await res.json();
          alert(result.pesan);
          fetchUsers();
          document.querySelector("#userForm").reset();
          document.querySelector("#userForm").onsubmit = null;
        } catch (err) {
          console.error("Gagal memperbarui pengguna:", err);
        }
      };
    }
  }
});

// === PANGGIL SAAT AWAL ===
fetchUsers();
