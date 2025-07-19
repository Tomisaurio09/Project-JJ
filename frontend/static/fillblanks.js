const token = localStorage.getItem('token');
const BACKEND_URL = 'http://localhost:5000';

const createSentenceForm = document.getElementById("create_sentences");
if(createSentenceForm) {
    createSentenceForm.addEventListener("submit", async e => {
        e.preventDefault();
        const sentence_data = {
            sentence: e.target.sentence.value,
            hidden_word: e.target.hidden_word.value
        };
        const res = await fetch(`${BACKEND_URL}/fillblank/create_fillblanks`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(sentence_data)
        });
        const json = await res.json();
        console.log(json);
    });
}

//SEPARACION
document.addEventListener('DOMContentLoaded', () => {
    const sentenceList = document.getElementById('sentence_list');

    async function fetchSentences() {
        try {
            //res es informacion que te devuelve el backend
            const res = await fetch(`${BACKEND_URL}/fillblank/show_fillblanks`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            //En el  caso de que no haya ninguna oración
            //negacion de res.ok es decir "si la respuesta no fue existosa"
            if (!res.ok) {
                const err = await res.json();
                sentenceList.innerHTML = `<li>${err.message}</li>`;
                return;
            }

            const data = await res.json();
            sentenceList.innerHTML = '';

            data.forEach(item => {
                const hiddenSentence = item.sentence.replace(item.hidden_word, '_____');
                const li = document.createElement('li');
                li.textContent = hiddenSentence;
                sentenceList.appendChild(li);
            });

        } catch (error) {
            console.error("Error fetching sentences:", error);
            sentenceList.innerHTML = `<li>Error loading sentences</li>`;
        }
    }

    fetchSentences(); // Ejecutar al cargar la página
});

//borrar
document.addEventListener('DOMContentLoaded', () => {
  const sentenceList = document.getElementById('sentence_list');

  async function fetchSentences() {
    try {
      const res = await fetch(`${BACKEND_URL}/fillblank/show_fillblanks`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!res.ok) {
        const err = await res.json();
        sentenceList.innerHTML = `<li>${err.message}</li>`;
        return;
      }

      const data = await res.json();
      sentenceList.innerHTML = '';

      data.forEach(item => {
        const li = document.createElement('li');
        const hiddenSentence = item.sentence.replace(item.hidden_word, '_____');
        li.textContent = hiddenSentence;
        //el codigo es igual al anterior

        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = '❌ Delete';
        deleteBtn.style.marginLeft = '10px';
        deleteBtn.addEventListener('click', async () => {
          const confirmed = confirm('Are you sure you want to delete this sentence?');
          if (!confirmed) return;

          const delRes = await fetch(`${BACKEND_URL}/delete_fillblanks/${item.id}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });

          const result = await delRes.json();
          if (delRes.ok) {
            alert(result.message);
            fetchSentences(); // Refrescar lista
          } else {
            alert(result.error || 'Error deleting sentence');
          }
        });

        li.appendChild(deleteBtn);
        sentenceList.appendChild(li);
      });
    } catch (error) {
      console.error('Error fetching sentences:', error);
      sentenceList.innerHTML = `<li>Error loading sentences</li>`;
    }
  }

  fetchSentences(); // Ejecutar al cargar la página
});
