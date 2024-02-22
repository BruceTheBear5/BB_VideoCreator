import os
import mysql.connector
from mutagen.mp3 import MP3
import wave
import cv2
import numpy as np
from datetime import datetime

class User:
    def __init__(self, name, username, email, password, id=-1, isAdmin="False"):
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
        
    def UploadData(self, cursor):
        cursor.execute("INSERT INTO Users (name, username, email, password, isAdmin) VALUES (%s, %s, %s, %s, %s)", (self.name, self.username, self.email, self.password, self.isAdmin))
        
    
class Image:
    def __init__(self, file_name, image_len, file_type, file_data, upload_date = datetime.now()):
        self.file_name = file_name
        self.file_size = image_len
        self.file_type = file_type
        self.file_data = file_data
        self.upload_date = upload_date
        
    def display(self):
        nparr = np.frombuffer(self.file_data, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        cv2.imshow(self.file_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
class Audio:
    def __init__(self, file_name, file_size, file_type, file_data, duration, upload_date = datetime.now()):
        self.file_name = file_name
        self.file_size = file_size
        self.file_type = file_type
        self.file_data = file_data
        self.duration = duration
        self.upload_date = upload_date

def save_data_to_mysql(data):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saiyam20_",
            database="Project"
        )

        cursor = connection.cursor()

        data.UploadData(cursor)

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

        for (id, name, email, password, isAdmin, username) in cursor:
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

def retrieve_image_from_mysql(userId):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saiyam20_",
            database="Project"
        )

        cursor = connection.cursor()
        query = "SELECT file_data, file_name FROM images WHERE user_id = %s"
        
        cursor.execute(query, (userId, ))
        rows = cursor.fetchall()
        
        Images = []
        if rows:
            for i, row in enumerate(rows):
                file_name = row[1]
                image_len = len(row[0])
                file_type = "image/jpg"
                file_data = row[0]
                upload_date = datetime.now()
                image = Image(file_name, image_len, file_type, file_data, upload_date)
                Images.append(image)
                
        return Images

    except mysql.connector.Error as error:
        print("Failed to retrieve image from MySQL database:", error)

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def upload_profile_image(user_id, image_name):
    """When user is created, use upload_profile_image(user_id, "./Images/alt_image.jpg")"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saiyam20_",
            database="Project"
        )

        cursor = connection.cursor()
        
        if(retrieve_profile_image(user_id) != None):
            delete_query = "DELETE FROM profile_pictures WHERE user_id = %s"
            cursor.execute(delete_query, (user_id,))
            connection.commit()
        
        with open(image_name, "rb") as file:
            image_data = file.read()

        query = "INSERT INTO profile_pictures (user_id, filename, filesize, file_type, file_data) VALUES (%s, %s, %s, %s, %s)"
        profileData = (user_id, image_name, len(image_data), "image/jpeg", image_data)
        
        cursor.execute(query, profileData)
        connection.commit()

        print("Profile image uploaded successfully.")

    except mysql.connector.Error as error:
        print("Failed to upload profile image:", error)

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def retrieve_profile_image(userId):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saiyam20_",
            database="Project"
        )
        
        cursor = connection.cursor()
        query = "SELECT file_data FROM profile_pictures WHERE user_id = %s"
        
        cursor.execute(query, (userId, ))
        row = cursor.fetchone()
        
        if row:
            file_name = "Image {}"
            image_len = len(row[0])
            file_type = "image/jpg"
            file_data = row[0]
            upload_date = datetime.now()
            image = Image(file_name, image_len, file_type, file_data, upload_date)
            return image
        else:
            print("Image not found in the database.")
            return None
     
    except mysql.connector.Error as error:
        print("Failed to upload profile image:", error)

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()   
  
def get_duration(file_path, file_format):
    if file_format.lower() == "mp3":
        audio = MP3(file_path)
        duration_seconds = int(audio.info.length)
    elif file_format.lower() == "wav":
        with wave.open(file_path, 'rb') as audio:
            frames = audio.getnframes()
            rate = audio.getframerate()
            duration_seconds = frames / float(rate)
    else:
        raise ValueError("Unsupported audio format")

    return duration_seconds

def save_audio_to_mysql(user_id, relative_file_path):
    try:
        absolute_file_path = os.path.abspath(relative_file_path)
        filename = os.path.basename(absolute_file_path)

        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saiyam20_",
            database="Project"
        )

        cursor = connection.cursor()

        with open(absolute_file_path, "rb") as file:
            audio_data = file.read()

        file_size_bytes = os.path.getsize(absolute_file_path)
        
        _, file_extension = os.path.splitext(filename)
        file_format = file_extension[1:]

        duration_seconds = get_duration(absolute_file_path, file_format)
        audio= Audio(filename, file_size_bytes, file_format, audio_data, duration_seconds)

        insert_query = """INSERT INTO audio_files (userId, filename, file_data, duration_seconds, file_size_bytes, file_format) VALUES (%s, %s, %s, %s, %s, %s)"""
        audio_values = (user_id, audio.file_name, audio.file_data, audio.duration, audio.file_size, audio.file_type)
        cursor.execute(insert_query, audio_values)

        connection.commit()
        print("Audio file saved to MySQL database successfully.")

    except FileNotFoundError:
        print("Error: Audio file '{}' not found.".format(absolute_file_path))
    except mysql.connector.Error as error:
        print("Failed to save audio file to MySQL database:", error)
    except ValueError as error:
        print("Failed to extract duration:", error)

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            
def retrieve_audio_from_mysql(user_id):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saiyam20_",
            database="Project"
        )

        cursor = connection.cursor()

        select_query = "SELECT filename, file_data, duration_seconds, file_size_bytes, file_format FROM audio_files WHERE userId = %s"
        cursor.execute(select_query, (user_id,))
        audio_files = cursor.fetchall()

        audio = []
        for audio_data in audio_files:
            file_name = audio_data[0]
            file_data = audio_data[1]
            duration = audio_data[2]
            file_size = audio_data[3]
            file_format = audio_data[4]
            AudioData = Audio(file_name, file_size, file_format, file_data, duration)
            audio.append(AudioData)

            
        print("Audio files retrieved from MySQL database successfully.")
        return audio

    except mysql.connector.Error as error:
        print("Failed to retrieve audio files from MySQL database:", error)

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            
def AdminRetrieve():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saiyam20_",
            database="Project"
        )

        cursor = connection.cursor()

        query = "SELECT * FROM Users"
        cursor.execute(query)
        rows = cursor.fetchall()

        Users = []
        for row in rows:
            id, name, email, password, isAdmin, username = row
            user = User(name, username, email, password, id, isAdmin)
            Users.append(user)

        return Users
    
    except mysql.connector.Error as error:
        print("Failed to retrieve users:", error)
        return []
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def AdminRetrieveProfilePic():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Saiyam20_",
            database="Project"
        )

        cursor = connection.cursor()

        query = "SELECT file_data, filename, filesize, file_type FROM profile_pictures"
        cursor.execute(query)
        rows = cursor.fetchall()

        profile_picture = []
        if rows:
            for row in rows:
                file_data = row[0]
                file_name = row[1]
                image_len = row[2]
                file_type = row[3]
                image = Image(file_name, image_len, file_type, file_data)
                profile_picture.append(image)
                
        return profile_picture
    
    except mysql.connector.Error as error:
        print("Failed to retrieve users:", error)
        return []
        
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# users = [
#     User("John Doe", "johndoe", "john@example.com", "password123", isAdmin="False"),
#     User("Jane Smith", "janesmith", "jane@example.com", "password456", isAdmin="True"),
#     User("Saiyam", "saiyam", "saiyam3420@gmail.com", "Saiyam20", isAdmin="True")
# ]

# save_data_to_mysql(users[2])
# save_data_to_mysql(users[1])
# user = retrieve_users_from_mysql("sa@ja.com")
# if(user):
#     user.printUser()
#     print(type(user.isAdmin))

# save_image_to_mysql(2, "./static/Images/Logo.png")
# retrieve_image_from_mysql(3)
# upload_profile_image(2, "./static/Images/alt_image.jpg")
# retrieve_profile_image(1)

# AdminRetrieve()
# AdminRetrieveProfilePic()

# save_audio_to_mysql(1, '/home/saiyamjain/Downloads/try.mp3')
# retrieve_audio_from_mysql(3)