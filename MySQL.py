import mysql.connector

class User:
    def __init__(self, name, username, email, password, id=-1, isAdmin=False):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.isAdmin = isAdmin
        
    def printUser(self):
        if (self != None):
            print("User ID:", self.id)
            print("Name:", self.name)
            print("Username:", self.username)
            print("Email:", self.email)
            print("Password:", self.password)
            print("Is Admin:", self.isAdmin)
        else:
            print("User not found.")
        
class Image:
    def __init__(self, file_name, image_len, file_type, file_data):
        self.file_name = file_name
        self.image_len = image_len
        self.file_type = file_type
        self.file_data = file_data

def save_data_mysql(data):
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
            
def save_image_to_mysql(user_id, image_name):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saiyam20_",
            database="Project"
        )

        cursor = connection.cursor()

        with open(image_name, "rb") as file:
            image_data = file.read()

        insert_query = """INSERT INTO images (user_id, file_name, file_size, file_type, file_data) VALUES (%s, %s, %s, %s, %s)"""
        image_values = (user_id, image_name, len(image_data), "image/jpeg", image_data)
        cursor.execute(insert_query, image_values)

        connection.commit()
        print("Image saved to MySQL database successfully.")

    except mysql.connector.Error as error:
        print("Failed to save image to MySQL database:", error)

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            
def retrieve_users_from_mysql(email):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saiyam20_",
            database="Project"
        )

        cursor = connection.cursor()

        query = "SELECT * FROM Users WHERE Users.email = %s"
        cursor.execute(query, (email, ))

        for (id, name, username, email, password, isAdmin) in cursor:
            users = User(name, username, email, password, id, isAdmin)

        if(users):
            print("Data retrieved from MySQL database successfully.")    
            return users
        else:
            print("Failed to retrieve data from MySQL database:")
            return None

    except mysql.connector.Error as error:
        print("Failed to retrieve data from MySQL database:", error)

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

users = [
    User("John Doe", "johndoe", "john@example.com", "password123"),
    User("Jane Smith", "janesmith", "jane@example.com", "password456", isAdmin=True)
]

# save_data_mysql(users)
user = retrieve_users_from_mysql("jane@example.com")
if(user):
    user.printUser()