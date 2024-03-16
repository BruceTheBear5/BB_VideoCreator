function connectToDB() {
    const isNOTConnected = localStorage.getItem('dbConnected');

    if (isNOTConnected) {
        fetch('/connect-db')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to connect to the database');
                }
                localStorage.setItem('dbConnected', false); 
                return response.text();
            })
            .then(message => {
                console.log(message);
            })
            .catch(error => {
                console.error('Error connecting to the database:', error);
            });
    } else{
        console.log('Already connected to database');
    }
    
}

window.addEventListener('beforeunload', disconnectFromDB);
document.addEventListener('DOMContentLoaded', connectToDB);

function disconnectFromDB() {
    fetch('/disconnect-db')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to disconnect from the database');
            }
            return response.text(); 
        })
        .then(message => {
            console.log(message); 
        })
        .catch(error => {
            console.error('Error disconnecting from the database:', error);
        });
}
