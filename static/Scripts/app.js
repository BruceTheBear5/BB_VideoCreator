function connectToDB() {
    const isConnected = localStorage.getItem('dbConnected');

    if (!isConnected) {
        fetch('/connect-db')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to connect to the database');
                }
                console.log('Database connected successfully.');
                localStorage.setItem('dbConnected', true);
            })
            .catch(error => {
                console.error('Error connecting to the database:', error);
            });
    }
}

document.addEventListener('DOMContentLoaded', connectToDB);

function disconnectFromDB() {
    fetch('/disconnect-db')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to disconnect from the database');
            }
            console.log('Database disconnected successfully.');
            localStorage.removeItem('dbConnected');
        })
        .catch(error => {
            console.error('Error disconnecting from the database:', error);
        });
}


window.addEventListener('beforeunload', disconnectFromDB);