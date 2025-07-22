const BACKEND_URL = 'http://localhost:5000';

document.addEventListener("DOMContentLoaded", function () {
  const openModalBtn = document.getElementById("create-folder");
  const closeModalBtn = document.getElementById("modal-close");
  const modal = document.getElementById("folderModal");
  const form = document.getElementById("noteForm");
  const foldersContainer = document.getElementById("foldersContainer");

  // Abrir modal
  openModalBtn.addEventListener("click", () => {
    modal.style.display = "flex";
  });

  // Cerrar modal con botón
  closeModalBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  // Cerrar modal haciendo click fuera
  window.addEventListener("click", (event) => {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
  //Hasta aca esta todo bien
  // Enviar formulario
// ...código de inicialización...

function renderFolder(folder) {
    const folderDiv = document.createElement("div");
    folderDiv.classList.add("folder");

    const folderTitle = document.createElement("span");
    folderTitle.classList.add("folder-title");
    folderTitle.textContent = folder.name;

    // --- Evento para abrir el folder ---
    folderDiv.addEventListener("click", (e) => {
        // Evita que el click en los botones de editar/eliminar también navegue
        if (e.target === folderButtonEdit || e.target === folderButtonDelete) return;
        window.location.href = `folders.html?id=${folder.id}`;
    });

    const folderButtonDelete = document.createElement("button");
    folderButtonDelete.classList.add("folder-button-delete");
    folderButtonDelete.innerHTML = "🗑️";
    folderButtonDelete.addEventListener("click", async (e) => {
        e.stopPropagation(); // Evita que el click borre y navegue
        const response = await fetch(`${BACKEND_URL}/notes/delete_folder/${folder.id}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem("token")}`,
            },
        });

        if (response.ok) {
            folderDiv.remove();
        } else {
            const errorData = await response.json();
            alert(errorData.error);
        }
    });

    const folderButtonEdit = document.createElement("button");
    folderButtonEdit.classList.add("folder-button-edit");
    folderButtonEdit.innerHTML = "✏️";
    folderButtonEdit.addEventListener("click", async (e) => {
        e.stopPropagation(); // Evita que el click edite y navegue
        const newName = prompt("Ingrese el nuevo nombre de la carpeta:", folder.name);
        if (newName) {
            const response = await fetch(`${BACKEND_URL}/notes/edit_folder/${folder.id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${localStorage.getItem("token")}`,
                },
                body: JSON.stringify({ name: newName }),
            });

            if (response.ok) {
                folderTitle.textContent = newName;
                folder.name = newName;
            } else {
                const errorData = await response.json();
                alert(errorData.error);
            }
        }
    });

    folderDiv.appendChild(folderTitle);
    folderDiv.appendChild(folderButtonEdit);
    folderDiv.appendChild(folderButtonDelete);
    foldersContainer.appendChild(folderDiv);
}

// --- Usar renderFolder en ambos lugares ---

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const folderName = form.elements["name"].value;

    const response = await fetch(`${BACKEND_URL}/notes/create_folder`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({ name: folderName }),
    });

    if (response.ok) {
        const folderData = await response.json();
        // Ajusta según lo que devuelve tu backend:
        renderFolder({
            id: folderData.folder_id || folderData.id,
            name: folderData.folder_name || folderData.name
        });
        modal.style.display = "none";
        form.reset();
    } else {
        const errorData = await response.json();
        alert(errorData.error);
    }
});

async function loadFolders() {
    foldersContainer.innerHTML = "";

    const response = await fetch(`${BACKEND_URL}/notes/folders`, {
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("token")}`,
        },
    });

    if (response.ok) {
        const folders = await response.json();
        folders.forEach(folder => renderFolder(folder));
    } else {
        const errorData = await response.json();
        alert(errorData.error);
    }
}

loadFolders();

});
