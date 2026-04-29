// Elementos del DOM
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadBtn = document.getElementById('uploadBtn');
const lionImage = document.getElementById('lionImage');
const analyzeBtn = document.getElementById('analyzeBtn');

// Función para manejar la selección de archivo
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function(e) {
            lionImage.src = e.target.result;
        };
        reader.readAsDataURL(file);
    } else {
        alert('Por favor, selecciona un archivo de imagen válido.');
    }
}

// Event listeners
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

uploadBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    fileInput.click();
});

fileInput.addEventListener('change', handleFileSelect);

// Botón para analizar otra foto
analyzeBtn.addEventListener('click', () => {
    lionImage.src = 'https://via.placeholder.com/300x200?text=Le%C3%B3n+Africano';
    fileInput.value = '';
});