function listUploadedImages() {
    const fileInput = document.getElementById('fileInput');
    const imageList = document.getElementById('imageList');

    const files = fileInput.files;
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (file.type.startsWith('image/')) {
            const listItem = document.createElement('li');
            const image = document.createElement('img');
            image.src = URL.createObjectURL(file);
            image.alt = file.name;
            listItem.appendChild(image);
            imageList.appendChild(listItem);
        }
    }
}

function uploadImages() {
    const files = document.getElementById('fileInput').files;

    if (files.length === 0) {
        alert('No files selected for upload.');
        return;
    }
    
    console.log('Uploading files:', files);
    const imageList = document.getElementById('imageList');
    imageList.innerHTML = '';
}

document.getElementById('fileInput').addEventListener('change', listUploadedImages);
document.getElementById('uploadButton').addEventListener('click', uploadImages);
