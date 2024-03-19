document.addEventListener('DOMContentLoaded', function () {
    const audioForm = document.getElementById('audioForm');
    
    audioForm.addEventListener('submit', function (e) {
        e.preventDefault();
        
        const formData = new FormData(audioForm);
        
        fetch('/upload-audio', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.text();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                console.log('Audio upload successful:', data);
            })
            .catch(error => {
                console.error('Error uploading audio:', error);
            });
        });
    });