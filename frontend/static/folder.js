const BACKEND_URL = 'http://localhost:5000';

document.addEventListener("DOMContentLoaded", async function () {
    // 1. Obtener el id del folder desde la URL
    const params = new URLSearchParams(window.location.search);
    const folderId = params.get('id');
    if (!folderId) {
        alert("No folder selected.");
        window.location.href = "notes.html";
        return;
    }

    const folderTitleElem = document.getElementById("folder-title");
    const notesContainer = document.getElementById("notesContainer");
    const openModalBtn = document.getElementById("create-note");
    const closeModalBtn = document.getElementById("modal-close");
    const modal = document.getElementById("noteModal");
    const form = document.getElementById("noteForm");

    // 2. Obtener y mostrar el nombre del folder
    async function loadFolderName() {
        const response = await fetch(`${BACKEND_URL}/notes/folders`, {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
        });
        if (response.ok) {
            const folders = await response.json();
            const folder = folders.find(f => f.id == folderId);
            if (folder) {
                folderTitleElem.textContent = folder.name;
            } else {
                folderTitleElem.textContent = "Folder not found";
            }
        }
    }

    // 3. Obtener y mostrar las notas del folder
    async function loadNotes() {
        notesContainer.innerHTML = "";
        const response = await fetch(`${BACKEND_URL}/notes/folders/${folderId}/notes`, {
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
        });
        if (response.ok) {
            const notes = await response.json();
            notes.forEach(note => {
                const noteDiv = document.createElement("div");
                noteDiv.classList.add("folder");
                noteDiv.innerHTML = `
                    <span class="folder-title">${note.title}</span>
                    <p>${note.content}</p>
                    <small>${new Date(note.created_at).toLocaleString()}</small>
                `;
                notesContainer.appendChild(noteDiv);
            });
        }
    }

    // 4. Abrir y cerrar modal
    openModalBtn.addEventListener("click", () => {
        modal.style.display = "flex";
    });
    closeModalBtn.addEventListener("click", () => {
        modal.style.display = "none";
    });
    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    // 5. Crear nueva nota en el folder
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const title = form.elements["title"].value;
        const content = form.elements["content"].value;
        const response = await fetch(`${BACKEND_URL}/notes/create_note`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
            body: JSON.stringify({ title, content, folder_id: folderId }),
        });
        if (response.ok) {
            modal.style.display = "none";
            form.reset();
            loadNotes();
        } else {
            const errorData = await response.json();
            alert(errorData.error);
        }
    });

    // Inicializar
    await loadFolderName();
    await loadNotes();
});