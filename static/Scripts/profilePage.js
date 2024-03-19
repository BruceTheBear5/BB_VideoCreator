var imageContainer = document.getElementById("imageContainer");
var sortBySelect = document.getElementById("sortBy");

function loadImages(imageSet) {
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
            var label = document.createElement('label');
            label.textContent = imageSet.name;

            div.appendChild(img);
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

window.onload = function () {
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