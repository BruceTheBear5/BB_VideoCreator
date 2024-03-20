var imageContainer = document.getElementById("imageContainer");
var sortBySelect = document.getElementById("sortBy");
var searchInput = document.getElementById("searchInput");

function loadImages(imageSet) {
    if (imageContainer) {
        while (imageContainer.firstChild) {
            imageContainer.removeChild(imageContainer.firstChild);
        }
        imageContainer.style.display = 'grid';
        imageSet.forEach(function (imageSet) {
            var img = document.createElement("img");
            img.src = "data:image/jpeg;base64," + imageSet.data;
            img.alt = imageSet.name;

            var div = document.createElement("div");
            div.classList.add("image-item");

            var selectButton = document.createElement("i");
            selectButton.classList.add("bi", "bi-check-circle", "close-button");

            img.addEventListener('click', function () {
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

function loadAudioOptions(audioSet) {
    var audioSelect = document.getElementById("backgroundMusic");

    audioSet.forEach(function (audio) {
        var option = document.createElement("option");
        option.value = audio.name;
        option.textContent = audio.name;
        audioSelect.appendChild(option);
    });
}

function setLoader(parentTag) {
    parentTag.innerHTML = "";
    parentTag.style.display = 'flex';
    parentTag.style.justifyContent = 'center';
    parentTag.style.alignItems = 'center';
    let loaderImg = document.createElement('img');
    loaderImg.src = '../static/Images/loader1.gif';
    parentTag.appendChild(loaderImg);
}

window.onload = function () {
    setLoader(imageContainer)
    fetch('/getUploadedImages')
        .then(response => response.json())
        .then(images => {
            loadImages(images);
        })
        .catch(error => console.error('Error fetching images:', error));

    fetch('/getPreloadedAudio')
        .then(response => response.json())
        .then(audios => {
            loadAudioOptions(audios);
        })
        .catch(error => console.error('Error fetching images:', error));

    fetch('/getUploadedAudio')
        .then(response => response.json())
        .then(audios => {
            loadAudioOptions(audios);
        })
        .catch(error => console.error('Error fetching images:', error));
}

searchInput.addEventListener("keypress", function (event) {
    if (event.key === 'Enter') {
        imageContainer.innerHTML = ""
        setLoader(imageContainer)
        event.preventDefault();
        var searchValue = searchInput.value;
        console.log("Search value:", searchValue);

        fetch('/searchBy', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ search: searchValue })
        })
            .then(response => response.json())
            .then(images => {
                loadImages(images);
            })
            .catch(error => console.error('Error fetching images:', error));
    }
});

sortBySelect.addEventListener("change", function () {
    console.log(sortBySelect.value);
    imageContainer.innerHTML = ""
    setLoader(imageContainer)
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
        fetch('/getSortedImageDate')
            .then(response => response.json())
            .then(images => {
                loadImages(images);
            })
            .catch(error => console.error('Error fetching sorted images:', error));
    }
    if (selectedValue == "file_size") {
        fetch('/getSortedImageFileSize')
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

function generateVideo() {
    var imgDuration = document.getElementById("imageDuration").value;
    var Transition = document.getElementById("transitionType").value;
    var vidResolution = document.getElementById("resolution").value;

    var requestData = {
        imgDuration: imgDuration,
        Transition: Transition,
        vidResolution: vidResolution
    };

    fetch('/videoCreate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
        .then(response => {
            if (response.ok) {
                document.getElementById('videoPlayer').querySelector('source').src = '../static/output_video.mp4';
                document.getElementById('videoPlayer').load();
            } else {
                console.error('Failed to generate video');
            }
        })
        .catch(error => {
            console.error('Error generating video:', error);
        });
}
