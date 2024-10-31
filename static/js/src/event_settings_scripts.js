document.addEventListener("DOMContentLoaded", () => {
   // ====== Gestion des onglets ======
   const initTabs = () => {
      const generalTabBtn = document.getElementById("generalTabBtn");
      const statsTabBtn = document.getElementById("statsTabBtn");
      const galleryTabBtn = document.getElementById("galleryTabBtn");

      const generalTab = document.getElementById("generalTab");
      const statsTab = document.getElementById("statsTab");
      const galleryTab = document.getElementById("galleryTab");

      const slider = document.getElementById("slider");

      function showTab(tabToShow, otherTabs, activeBtn, otherButtons) {
         tabToShow.style.display = "block";
         otherTabs.forEach(tab => tab.style.display = "none");

         activeBtn.classList.add("active");
         otherButtons.forEach(button => button.classList.remove("active"));

         updateSlider(activeBtn);
      }

      function updateSlider(button) {
         slider.style.width = `${button.offsetWidth}px`;
         slider.style.left = `${button.offsetLeft}px`;
      }

      // Initialisation de l'onglet par défaut
      showTab(generalTab, [statsTab, galleryTab], generalTabBtn, [statsTabBtn, galleryTabBtn]);

      // Event listeners pour les onglets
      generalTabBtn.addEventListener("click", () => {
         showTab(generalTab, [statsTab, galleryTab], generalTabBtn, [statsTabBtn, galleryTabBtn]);
      });

      statsTabBtn.addEventListener("click", () => {
         showTab(statsTab, [generalTab, galleryTab], statsTabBtn, [generalTabBtn, galleryTabBtn]);
      });

      galleryTabBtn.addEventListener("click", () => {
         showTab(galleryTab, [generalTab, statsTab], galleryTabBtn, [generalTabBtn, statsTabBtn]);
      });
   };

   // ====== Gestion du formulaire d'événement ======
   const initEventForm = () => {
      const form = document.getElementById("event-form");
      const submitBtn = document.getElementById("submit-btn");
      const initialFormState = new FormData(form);
      const fileInput = document.getElementById("pick-poster");
      const previewImage = document.getElementById("poster-preview");
      let isFormDirty = false;

      const isFormModified = () => {
         const currentFormState = new FormData(form);
         for (let [key, value] of currentFormState.entries()) {
            // Ignorer la comparaison pour le fichier poster si aucun nouveau fichier n'est sélectionné
            if (key === 'poster' && !value.name) continue;
            if (initialFormState.get(key)?.toString() !== value?.toString()) return true;
         }
         return false;
      };

      // Mettre à jour l'état du formulaire et le bouton
      const updateFormState = () => {
         isFormDirty = isFormModified();
         submitBtn.disabled = !isFormDirty;
      };

      // Gestionnaire pour les changements dans le formulaire
      form.addEventListener("input", updateFormState);

      // Gestionnaire spécifique pour le changement d'image
      fileInput.addEventListener("change", (event) => {
         const file = event.target.files[0];
         if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
               previewImage.src = e.target.result;
            }
            reader.readAsDataURL(file);
         }
         isFormDirty = true;
         submitBtn.disabled = false;
      });

      // Gestionnaire de soumission du formulaire
      form.addEventListener("submit", () => {
         isFormDirty = false;
      });

      // Avertissement avant de quitter la page
      window.addEventListener("beforeunload", (event) => {
         if (isFormDirty) {
            // Message standard qui sera affiché par le navigateur
            event.preventDefault();
            event.returnValue = "";
            return "";
         }
      });

      // Ajoutez ceci dans la fonction initEventForm
      document.querySelectorAll('a').forEach(link => {
         link.addEventListener('click', (event) => {
            if (isFormDirty && !event.target.closest('form')) {
               const confirmation = confirm('Vous avez des modifications non enregistrées. Voulez-vous vraiment quitter la page ?');
               if (!confirmation) {
                  event.preventDefault();
               }
            }
         });
      });
   };

   // ====== Gestion de la galerie ======
   const initGallery = () => {
      const form = document.getElementById('gallery-form');
      const input = document.getElementById('gallery-images');
      const container = document.getElementById('gallery-container');
      const dropZone = form.querySelector('.border-dashed');
      const uploadUrl = form.dataset.uploadUrl;

      // Prévention des comportements par défaut pour le drag & drop
      ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
         dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
         }, false);
      });

      // Gestion des effets visuels du drag & drop
      ['dragenter', 'dragover'].forEach(eventName => {
         dropZone.addEventListener(eventName, () => {
            dropZone.style.borderColor = '#a1c617';
         }, false);
      });

      ['dragleave', 'drop'].forEach(eventName => {
         dropZone.addEventListener(eventName, () => {
            dropZone.style.borderColor = '';
         }, false);
      });

      // Gestion du dépôt des fichiers
      dropZone.addEventListener('drop', (e) => {
         handleFiles(e.dataTransfer.files);
      }, false);

      input.addEventListener('change', function (e) {
         handleFiles(this.files);
      });

      function handleFiles(files) {
         const formData = new FormData();
         Array.from(files).forEach(file => {
            formData.append('images', file);
         });

         const loadingIndicator = document.getElementById('loading-indicator');
         loadingIndicator.classList.remove('hidden');
         loadingIndicator.classList.add('flex');

         fetch(uploadUrl, {
            method: 'POST',
            body: formData,
            headers: {
               'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
         })
            .then(response => response.json())
            .then(data => {
               if (data.status === 'success') {
                  data.images.forEach(image => {
                     const newImageElement = createImageElement(image);
                     container.insertAdjacentHTML('afterbegin', newImageElement);
                  });
               } else {
                  alert('Erreur lors du téléchargement des images');
               }
            })
            .catch(error => {
               console.error('Error:', error);
               alert('Erreur lors du téléchargement des images');
            })
            .finally(() => {
               loadingIndicator.classList.remove('flex');
               loadingIndicator.classList.add('hidden');
               form.reset();
            });
      }

      function createImageElement(image) {
         return `
                <div id="image-${image.id}" class="gallery-image relative group rounded-lg overflow-hidden shadow">
                    <div class="aspect-w-16 aspect-h-9">
                        <img src="${image.url}"
                             alt=""
                             class="w-full h-full object-cover">
                    </div>
                    <button class="delete-image absolute top-2 right-2 p-2 rounded-full bg-red-600 hover:bg-red-700 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                            data-image-id="${image.id}"
                            aria-label="Supprimer l'image">
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"
                             fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                             stroke-linejoin="round" class="lucide lucide-trash-2">
                            <path d="M3 6h18"/>
                            <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>
                            <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>
                            <line x1="10" x2="10" y1="11" y2="17"/>
                            <line x1="14" x2="14" y1="11" y2="17"/>
                        </svg>
                    </button>
                </div>
            `;
      }

      // Gestion de la suppression des images
      document.addEventListener('click', function (e) {
         if (e.target.closest('.delete-image')) {
            const button = e.target.closest('.delete-image');
            const imageId = button.dataset.imageId;
            if (confirm('Voulez-vous vraiment supprimer cette image ?')) {
               deleteImage(imageId);
            }
         }
      });

      function deleteImage(imageId) {
         fetch(`/dashboard/gallery/image/${imageId}/delete/`, {
            method: 'POST',
            headers: {
               'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
         })
            .then(response => response.json())
            .then(data => {
               if (data.status === 'success') {
                  document.getElementById(`image-${imageId}`).remove();
               }
            })
            .catch(error => {
               console.error('Error:', error);
               alert('Erreur lors de la suppression de l\'image');
            });
      }

      // Gestion du compteur de la galerie
      function updateGalleryCounter(imageCount) {
         const counterElement = document.getElementById('gallery-counter');
         const text = imageCount === 0 ? 'Aucune image dans la galerie' :
            imageCount === 1 ? '1 image dans la galerie' :
               `${imageCount} images dans la galerie`;
         counterElement.textContent = text;
      }

      // Observer pour mettre à jour le compteur
      const galleryObserver = new MutationObserver(() => {
         const imageCount = document.querySelectorAll('.gallery-image').length;
         updateGalleryCounter(imageCount);
      });

      galleryObserver.observe(container, {
         childList: true,
         subtree: true
      });
   };

   // Initialisation de toutes les fonctionnalités
   initTabs();
   initEventForm();
   initGallery();
});
