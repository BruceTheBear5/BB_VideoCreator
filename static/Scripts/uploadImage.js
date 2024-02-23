document.addEventListener('DOMContentLoaded', function () {
    let dropArea = document.getElementById('drop-area');
    let fileInput = document.getElementById('fileInput');
    let imageList = document.getElementById('imageContainer');
    let browseButton = document.getElementById('browseButton');
<<<<<<< HEAD
    let uploadForm = document.getElementById('uploadForm');
=======
    let submitButton = document.getElementById('submit');
    let allFiles = [];
>>>>>>> 1c7d87f7f2913b79155c953b57a43f778372fa06

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
        e.preventDefault();
        dropArea.classList.remove('error');

        let files = e.dataTransfer.files;
        allFiles = allFiles.concat(Array.from(files).filter(file => file.type.startsWith('image/')));
        handleFiles(files);
    }

    browseButton.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', function (e) {
        e.preventDefault();
        dropArea.classList.remove('error');

        allFiles = allFiles.concat(Array.from(e.target.files).filter(file => file.type.startsWith('image/')));
        handleFiles(e.target.files);
    });

    //var ul = document.createElement('ul');
    function handleFiles(files) {
        files = Array.from(files);
        files.forEach(previewFile);
        //imageList.appendChild(ul);
    }

    function previewFile(file) {
        if (!file.type.startsWith('image/')){
            dropArea.classList.add('error');
            alert('Only image files are supported.');
            return;
        }
        //let li = document.createElement('li');
        let reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onloadend = function () {
            let container = document.createElement('div');
            container.classList.add('image-item');
            container.target = '_blank';

            let closeButton = document.createElement('button'); 
            closeButton.textContent = '×'; 
            closeButton.classList.add('close-button'); 
            
            closeButton.addEventListener('click', function() {
                container.remove();
                allFiles = allFiles.filter(f => f !== file);
                checkForImages();
            });

            let anchor = document.createElement('a');
            anchor.href = reader.result;

            let img = document.createElement('img');
            img.src = reader.result;
<<<<<<< HEAD
            img.alt = file.name;
            imageList.appendChild(img);
=======
            
            let label = document.createElement('label');
            label.textContent = file.name;
            
            anchor.appendChild(img);
            container.appendChild(closeButton);
            container.appendChild(anchor);
            container.appendChild(label);
            imageList.appendChild(container);
            //li.appendChild(img);
>>>>>>> 1c7d87f7f2913b79155c953b57a43f778372fa06
        }
    }
<<<<<<< HEAD
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
=======

    function checkForImages() {
        const images = imageList.querySelectorAll('div');
        if (images.length > 0) {
            document.getElementById('containerHeader').style.display = 'block';
        } else {
            document.getElementById('containerHeader').style.display = 'none';
        }
    }
    const observer = new MutationObserver(checkForImages);
    observer.observe(imageList, { childList: true });

    submitButton.addEventListener('click', function () {

    var formData = new FormData();
    allFiles.forEach(file => {
        formData.append('files[]', file);
    });

    fetch('/trigger-upload', {
      method: 'POST',
      body: formData
    })
      .then(response => response.json())
      .then(data => {
        console.log('Upload successful:', data);
      })
      .catch(error => {
        console.error('Error uploading files:', error);
      });
  });
});
>>>>>>> 1c7d87f7f2913b79155c953b57a43f778372fa06
