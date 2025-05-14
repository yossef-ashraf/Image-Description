// DOM Elements
const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('fileElem');
const previewContainer = document.getElementById('preview-container');
const preview = document.getElementById('preview');
const changeImageBtn = document.getElementById('change-image');
const analyzeBtn = document.getElementById('analyze-btn');
const resultContainer = document.getElementById('result-container');
const loading = document.getElementById('loading');
const basicCaption = document.getElementById('basic-caption');
const detailedDescription = document.getElementById('detailed-description');
const imageProperties = document.getElementById('image-properties');

// Prevent default drag behaviors
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

// Highlight drop area when item is dragged over it
['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, highlight, false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, unhighlight, false);
});

function highlight() {
    dropArea.classList.add('highlight');
}

function unhighlight() {
    dropArea.classList.remove('highlight');
}

// Handle dropped files
dropArea.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

// Handle selected files
function handleFiles(files) {
    if (files.length) {
        const file = files[0];
        if (file.type.startsWith('image/')) {
            displayPreview(file);
        } else {
            alert('Please select an image file (PNG, JPG, JPEG, GIF)');
        }
    }
}

// Display image preview
function displayPreview(file) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
        preview.src = e.target.result;
        document.querySelector('.upload-form').style.display = 'none';
        previewContainer.classList.remove('hidden');
        analyzeBtn.classList.remove('hidden');
        resultContainer.classList.add('hidden');
    }
    
    reader.readAsDataURL(file);
}

// Change image button
changeImageBtn.addEventListener('click', () => {
    document.querySelector('.upload-form').style.display = 'flex';
    previewContainer.classList.add('hidden');
    analyzeBtn.classList.add('hidden');
    resultContainer.classList.add('hidden');
    fileInput.value = '';
});

// Analyze image
analyzeBtn.addEventListener('click', () => {
    if (!fileInput.files.length && !preview.src) {
        alert('Please select an image first');
        return;
    }
    
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);
    
    resultContainer.classList.remove('hidden');
    loading.classList.remove('hidden');
    basicCaption.textContent = '';
    detailedDescription.textContent = '';
    imageProperties.innerHTML = '';
    
    fetch('/analyze', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loading.classList.add('hidden');
        
        if (data.success) {
            const desc = data.description;
            
            // Display basic caption
            basicCaption.textContent = desc.basic_caption || 'Not available';
            
            // Display detailed description
            detailedDescription.textContent = desc.detailed_description || 'Not available';
            
            // Display image properties
            if (desc.analysis) {
                const analysis = desc.analysis;
                
                // Clear previous properties
                imageProperties.innerHTML = '';
                
                // Add dimensions
                if (analysis.dimensions) {
                    const li = document.createElement('li');
                    li.textContent = `Dimensions: ${analysis.dimensions}`;
                    imageProperties.appendChild(li);
                }
                
                // Add brightness
                if (analysis.brightness) {
                    const li = document.createElement('li');
                    li.textContent = `Brightness: ${analysis.brightness}`;
                    imageProperties.appendChild(li);
                }
                
                // Add colorfulness
                if (analysis.colorfulness) {
                    const li = document.createElement('li');
                    li.textContent = `Color profile: ${analysis.colorfulness}`;
                    imageProperties.appendChild(li);
                }
                
                // Add dominant colors
                if (analysis.dominant_colors && analysis.dominant_colors.length) {
                    const li = document.createElement('li');
                    li.textContent = `Dominant colors: ${analysis.dominant_colors.join(', ')}`;
                    imageProperties.appendChild(li);
                }
            }
        } else {
            basicCaption.textContent = `Error: ${data.error}`;
        }
    })
    .catch(error => {
        loading.classList.add('hidden');
        basicCaption.textContent = `Error: ${error.message}`;
    });
});

// Handle drag and drop for the entire document
document.addEventListener('dragenter', function(e) {
    if (!dropArea.contains(e.target)) {
        e.preventDefault();
        e.dataTransfer.effectAllowed = 'none';
        e.dataTransfer.dropEffect = 'none';
    }
}, false);

document.addEventListener('dragover', function(e) {
    if (!dropArea.contains(e.target)) {
        e.preventDefault();
        e.dataTransfer.effectAllowed = 'none';
        e.dataTransfer.dropEffect = 'none';
    }
}, false);

document.addEventListener('drop', function(e) {
    if (!dropArea.contains(e.target)) {
        e.preventDefault();
    }
}, false);