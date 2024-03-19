var imageContainer = document.getElementById("imageContainer");
var musicContainer = document.getElementById("musicContainer");
// var sortBySelect = document.getElementById("sortBy");

function loadImages(imageSet) {
    imageContainer.innerHTML = '';
    imageSet.forEach(function (image) {
        var anchor = document.createElement("a");
        anchor.href = "data:image/jpeg;base64," + image.data;
        anchor.target = "_blank";

        var img = document.createElement("img");
        img.src = "data:image/jpeg;base64," + image.data;
        img.alt = image.name;

        var div = document.createElement("div");
        div.classList.add("image-item");

        var label = document.createElement('label');
        label.textContent = image.name;

        anchor.appendChild(img);
        div.appendChild(anchor);
        div.appendChild(label);
        imageContainer.appendChild(div);
    });
}

function loadAudio(audioSet) {
    musicContainer.innerHTML = '';

    audioSet.forEach(function (audio) {
        console.log("" + audio.name);

        var cell = document.createElement("div");
        cell.classList.add('audioCell');

        var name = document.createElement("span");
        name.classList.add('audioName');
        name.textContent = "" + audio.name;
        
        var controls = document.createElement("audio");
        controls.setAttribute('controls', '');

        var clip = document.createElement("source");
        clip.setAttribute('src', "data:audio/mpeg;base64," + audio.data);

        controls.appendChild(clip);
        cell.appendChild(name);
        cell.appendChild(controls);
        musicContainer.appendChild(cell);
    });
}

window.onload = function () {
    fetch('/getUploadedImages')
        .then(response => response.json())
        .then(images => {
            loadImages(images);
        })
        .catch(error => console.error('Error fetching images:', error));

    fetch('/getUploadedAudio')
        .then(response => response.json())
        .then(audios => {
            loadAudio(audios);
        })
        .catch(error => console.error('Error fetching images:', error));
}

// sortBySelect.addEventListener("change", function () {
//     console.log(sortBySelect.value);
//     imageContainer.innerHTML = ""
//     var selectedValue = sortBySelect.value;
//     if (selectedValue == "file_name") {
//         fetch('/getSortedImageName')
//             .then(response => response.json())
//             .then(images => {
//                 loadImages(images);
//             })
//             .catch(error => console.error('Error fetching sorted images:', error));
//     }
//     if (selectedValue == "uploaded_at") {
//         fetch('/getSortedImageDate')
//             .then(response => response.json())
//             .then(images => {
//                 loadImages(images);
//             })
//             .catch(error => console.error('Error fetching sorted images:', error));
//     }
//     if (selectedValue == "file_size") {
//         fetch('/getSortedImageFileSize')
//             .then(response => response.json())
//             .then(images => {
//                 loadImages(images);
//             })
//             .catch(error => console.error('Error fetching sorted images:', error));
//     }
// });