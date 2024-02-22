
document.addEventListener('DOMContentLoaded', function () {
    let dropArea = document.getElementById('drop-area');
    let fileInput = document.getElementById('fileInput');
    let imageList = document.getElementById('imageContainer');
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
            imageList.appendChild(img);
            //li.appendChild(img);
        }
        //ul.appendChild(li);
    }

    let submitButton = document.getElementById('submit');
    submitButton.addEventListener('click', function () {
    var files = fileInput.files;

    var formData = new FormData();
    for (var i = 0; i < files.length; i++) {
      formData.append('files[]', files[i]);
    }

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