// function listUploadedImages() {
//     const fileInput = document.getElementById('fileInput');
//     const imageList = document.getElementById('imageList');

//     const files = fileInput.files;
//     for (let i = 0; i < files.length; i++) {
//         const file = files[i];
//         if (file.type.startsWith('image/')) {
//             const listItem = document.createElement('li');
//             const image = document.createElement('img');
//             image.src = URL.createObjectURL(file);
//             image.alt = file.name;
//             listItem.appendChild(image);
//             imageList.appendChild(listItem);
//         }
//     }
// }

// function uploadImages() {
//     const files = document.getElementById('fileInput').files;

//     if (files.length === 0) {
//         alert('No files selected for upload.');
//         return;
//     }
    
//     console.log('Uploading files:', files);
//     const imageList = document.getElementById('imageList');
//     imageList.innerHTML = '';
// }

// document.getElementById('fileInput').addEventListener('change', listUploadedImages);
// document.getElementById('uploadButton').addEventListener('click', uploadImages);
document.addEventListener('DOMContentLoaded', function () {
    let dropArea = document.getElementById('drop-area');
    let fileInput = document.getElementById('fileInput');
    let imageList = document.getElementById('imageList');
    let browseButton = document.getElementById('browseButton');

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
        document.body.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });

    dropArea.addEventListener('drop', handleDrop, false);

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    function highlight() {
        dropArea.classList.add('highlight');
    }

    function unhighlight() {
        dropArea.classList.remove('highlight');
    }

    function handleDrop(e) {
        let files = e.dataTransfer.files;
        handleFiles(files);
    }

    browseButton.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', function (e) {
        handleFiles(this.files);
    });

    var ul = document.createElement('ul');
    function handleFiles(files) {
        files = [...files];
        files.forEach(previewFile);
        imageList.appendChild(ul);
    }

    function previewFile(file) {
        let li = document.createElement('li');
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function () {
            let img = document.createElement('img');
            img.src = reader.result;
            li.appendChild(img);
        }
        ul.appendChild(li);
    }
});