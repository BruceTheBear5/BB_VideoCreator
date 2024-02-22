document.addEventListener('DOMContentLoaded', function () {
    let dropArea = document.getElementById('drop-area');
    let fileInput = document.getElementById('fileInput');
    let imageList = document.getElementById('imageContainer');
    let browseButton = document.getElementById('browseButton');
    let uploadForm = document.getElementById('uploadForm');

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

    //var ul = document.createElement('ul');
    function handleFiles(files) {
        files = [...files];
        files.forEach(previewFile);
        //imageList.appendChild(ul);
    }

    function previewFile(file) {
        //let li = document.createElement('li');
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function () {
            let img = document.createElement('img');
            img.src = reader.result;
            img.alt = file.name;
            imageList.appendChild(img);
        }
    }
    document.addEventListener('DOMContentLoaded', function () {
        let uploadForm = document.getElementById('uploadForm');
    
        uploadForm.addEventListener('submit', function (e) {
            e.preventDefault(); // Prevent default form submission
    
            let formData = new FormData(uploadForm); // Create a new FormData object from the form
            let images = document.querySelectorAll('#imageList img');
    
            images.forEach(function (image, index) {
                let src = image.getAttribute('src');
                let alt = image.getAttribute('alt');
    
                // Append the image src and alt attributes as additional form fields
                formData.append(`imageListData[${index}][src]`, src);
                formData.append(`imageListData[${index}][alt]`, alt);
            });
    
            // Log FormData for debugging
            for (let pair of formData.entries()) {
                console.log(pair[0], pair[1]); 
            }
    
            // Send FormData to the backend using fetch
            fetch('/Upload', {
                method: 'POST',
                body: formData
            })
            .then(response => {
                if (response.ok) {
                    console.log('Images uploaded successfully!');
                } else {
                    console.error('Error uploading images:', response.statusText);
                }
            })
            .catch(error => {
                console.error('Error uploading images:', error);
            });
        });
    });
});    
