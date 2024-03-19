var imageContainer = document.getElementById("imageContainer");
var sortBySelect = document.getElementById("sortBy");

function loadImages(imageSet) {
    // Ensure imageContainer exists before trying to modify it
    if (imageContainer) {
        while (imageContainer.firstChild) {
            imageContainer.removeChild(imageContainer.firstChild);
        }
        imageSet.forEach(function (imageSet) {
            var img = document.createElement("img");
            img.src = "data:image/jpeg;base64," + imageSet.data;
            img.alt = imageSet.name;

            var div = document.createElement("div");
            div.classList.add("image-item");

            var selectButton = document.createElement("i");
            selectButton.classList.add("bi", "bi-check-circle", "close-button");

            selectButton.addEventListener('click', function () {
                toggleImage(imageSet, selectButton);
            });

            var label = document.createElement('label');
            label.textContent = imageSet.name;

            div.appendChild(img);
            div.appendChild(selectButton);
            div.appendChild(label);
            imageContainer.appendChild(div);
        });
    } else {
        console.error("Image container not found.");
    }
}


window.onload = function () {
    fetch('/getUploadedImages')
        .then(response => response.json())
        .then(images => {
            print("F");
            loadImages(images);
        })
        .catch(error => console.error('Error fetching images:', error));
}

sortBySelect.addEventListener("change", function () {
    console.log(sortBySelect.value);
    imageContainer.innerHTML = ""
    var selectedValue = sortBySelect.value;
    if (selectedValue == "file_name") {
        fetch('/getSortedImageName')
            .then(response => response.json())
            .then(images => {
                loadImages(images);
            })
            .catch(error => console.error('Error fetching sorted images:', error));
    }
    if (selectedValue == "uploaded_at") {
        fetch('/getSortedImageFileSize')
            .then(response => response.json())
            .then(images => {
                loadImages(images);
            })
            .catch(error => console.error('Error fetching sorted images:', error));
    }
    if (selectedValue == "file_size") {
        fetch('/getSortedImageDate')
            .then(response => response.json())
            .then(images => {
                loadImages(images);
            })
            .catch(error => console.error('Error fetching sorted images:', error));
    }
});

function toggleImage(image, selectButton) {
    fetch('/toggle-image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: image })
    })
        .then(response => {
            if (response.ok) {
                response.json().then(data => {
                    if (data.selected) {
                        selectButton.classList.remove('bi-check-circle');
                        selectButton.classList.add('bi-check-circle-fill');
                    } else {
                        selectButton.classList.remove('bi-check-circle-fill');
                        selectButton.classList.add('bi-check-circle');
                    }
                });
            } else {
                console.error('Failed to toggle selected status for image.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function emptyImages() {
    fetch('/empty-selected', {
        method: 'POST'
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to remove all images from selection.');
            }
        })
        .then(data => {
            console.log(data.message);
        })
        .catch(error => {
            console.error('Error:', error.message);
        });
}

var clear = document.getElementById("imageClear");
clear.addEventListener('click', function () {
    emptyImages();
    var checks = imageContainer.querySelectorAll('.bi.close-button.bi-check-circle-fill');
    checks.forEach(function (element) {
        element.classList.add('bi-check-circle');
        element.classList.remove('bi-check-circle-fill');
    });
});