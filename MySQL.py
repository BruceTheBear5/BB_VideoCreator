import mysql.connector

class User:
    def __init__(self,name, username, email, password, isAdmin=False):
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.isAdmin = isAdmin
        
class Image:
    def __init__(self, file_name, image_len, file_type, file_data):
        self.file_name = file_name
        self.image_len = image_len
        self.file_type = file_type
        self.file_data = file_data

def save_to_mysql(data):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saiyam20_",
            database="Project"
        )

        cursor = connection.cursor()

        for x in data:
            name = x.name
            username = x.username
            email = x.email
            password = x.password
            isAdmin = x.isAdmin
            cursor.execute("INSERT INTO Users (name, username, email, password, isAdmin) VALUES (%s, %s, %s, %s, %s)", (name, username, email, password, isAdmin))

        connection.commit()
        print("Data saved to MySQL database successfully.")

    except mysql.connector.Error as error:
        print("Failed to save data to MySQL database:", error)

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            
def save_image(user_id, imageName):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Saiyam20_",
        database="Project"
    )
    
    cursor = conn.cursor()
    with open(imageName, "rb") as file:
        image_data = file.read()

    insert_query = """INSERT INTO images (user_id, file_name, file_size, file_type, file_data) VALUES (%s, %s, %s, %s, %s)"""
    image_values = (user_id, "image.jpg", len(image_data), "image/jpeg", image_data)
    cursor.execute(insert_query, image_values)

    conn.commit()
    cursor.close()
    conn.close()