from flask import Flask, render_template, request, redirect, url_for, flash, session, Response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from MySQL import User, retrieve_users_from_mysql, save_data_to_mysql, retrieve_image_from_mysql, retrieve_profile_image, upload_profile_image, AdminRetrieve, AdminRetrieveProfilePic, retrieve_audio_from_mysql, save_image_to_mysql, save_audio_to_mysql, start_connection_pool, close_connection_pool, sort_mysql
import os
import base64
import jwt
import json
import atexit

app = Flask(__name__)
SECRET_KEY = os.urandom(24)
app.secret_key = SECRET_KEY

@app.before_request
def auto_authenticate():
    if 'jwt_token' in session:
        token = session.get('jwt_token')
        if token:
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                if "userId" in data:
                    session["userId"] = data["userId"]
                    session["username"] = data["username"]
                    session["userEmail"] = data["userEmail"]
                    session["userIsAdmin"] = data["userIsAdmin"]
            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                pass

start_connection_pool()

@app.route('/')
def home():
    token = session.get('jwt_token')
    if not token:
        return render_template('index.html', isAdmin = "False", user = "False")
    
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        if "userId" in session:
            if session["userIsAdmin"] == "True":
                return render_template('index.html', isAdmin = "True", user = "True", username = session["username"])
            else:
                return render_template('index.html', isAdmin = "False", user = "True", username = session["username"])
    
    except jwt.ExpiredSignatureError:
        return redirect(url_for('signin'))
    
    except jwt.InvalidTokenError:
        return redirect(url_for('signin'))

    return render_template('index.html', isAdmin = "False", user = "False")

@app.route('/signin')
def signin():
    return render_template('login.html', signin="True", signup="False", ForgetPassword="False")

@app.route('/signup')
def signup():
    return render_template('login.html', signin = "False", signup = "True", ForgetPassword = "False")

@app.route('/forgetpassword')
def forgetPassword():
    return render_template('login.html', signin = "False", signup = "False", ForgetPassword = "True")

@app.route('/SignIn', methods=['POST'])
def signinFunc():
    email = request.form['email']
    password = request.form['password']
    user = retrieve_users_from_mysql(email)
    if user == None:
        flash('No User Found')
        return redirect(url_for('signin'))
    elif check_password_hash(user.password, password):
        session["userId"] = user.id
        session["username"] = str(user.username)
        session["userEmail"] = user.email
        session["userIsAdmin"] = user.isAdmin
        if user.isAdmin:
            flash('Admin SignIn Successfull')
        else:
            flash('SignIn Successfull')
        
        token = jwt.encode({'username': user.username}, app.config['SECRET_KEY'], algorithm='HS256')
        session['jwt_token'] = token
        
        return redirect(url_for('home'))
        
    else:
        flash('Incorrect password')
        return redirect(url_for('signin'))

@app.route('/SignUp', methods=['POST'])
def signupFunc():
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    hashPassword = generate_password_hash(password, method='pbkdf2')

    if retrieve_users_from_mysql(email) == None:
        user = User(name, username, email, hashPassword, isAdmin="False")
        save_data_to_mysql(user)
        user = retrieve_users_from_mysql(email)
        upload_profile_image(user.id, "./static/Images/alt_image.jpg")
        session["userId"] = user.id
        session["username"] = user.username
        session["userEmail"] = user.email
        session["userIsAdmin"] = user.isAdmin
        flash('Registration Successful')
        
        token = jwt.encode({'username': user.username}, app.config['SECRET_KEY'], algorithm='HS256')
        session['jwt_token'] = token
        
        return redirect(url_for('home'))

    else:
        flash('Email already exists')
        return redirect(url_for('signup'))

@app.route('/profile/<username>', methods=['GET'])
def profileData(username):
    try:
        if "userId" in session:
            UserEmail = session["userEmail"]
            user = retrieve_users_from_mysql(UserEmail)
            profile_image = retrieve_profile_image(user.id)
            if profile_image == None:
                upload_profile_image(user.id, "./static/Images/alt_image.jpg")
                profile_image = retrieve_profile_image(user.id)
            profileImage = base64.b64encode(profile_image.file_data).decode('utf-8')

            return render_template('profile.html', user = user, profileImage = profileImage, username = user.username, isAdmin = user.isAdmin)
        else:
            return redirect(url_for('home'))
    except Exception as e:
        print("Error:", e)
        return Response(status=500)
    
@app.route('/getUploadedImages') #For JS
def getUploadedImages():
    try:
        userId = session["userId"]
        images = retrieve_image_from_mysql(userId)
        imageData = []
        for i in images:
            encoded_image = base64.b64encode(i.file_data).decode('utf-8')
            img = {'data' : encoded_image, 'name': i.file_name}
            imageData.append(img)
            
        return jsonify(imageData)
    except Exception as e:
        print("Error:", e)
        return Response(status=500)
    
@app.route('/getSortedImageName')
def getSortedImageName():
    try:
        userId = session.get("userId")
        images = sort_mysql(userId, "file_name")
        imageData = []
        for image in images:
            encoded_image = base64.b64encode(image.file_data).decode('utf-8')
            img = {'data': encoded_image, 'name': image.file_name}
            imageData.append(img)
            
        return jsonify(imageData)
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/getSortedImageFileSize')
def getSortedImageFileSize():
    try:
        userId = session.get("userId")
        images = sort_mysql(userId, "file_size")
        imageData = []
        for image in images:
            encoded_image = base64.b64encode(image.file_data).decode('utf-8')
            img = {'data': encoded_image, 'name': image.file_name}
            imageData.append(img)
            
        return jsonify(imageData)
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/getSortedImageDate')
def getSortedImageDate():
    try:
        userId = session.get("userId")
        images = sort_mysql(userId, "uploaded_at")
        imageData = []
        for image in images:
            encoded_image = base64.b64encode(image.file_data).decode('utf-8')
            img = {'data': encoded_image, 'name': image.file_name}
            imageData.append(img)
            
        return jsonify(imageData)
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': str(e)}), 500
    
@app.route('/getPreloadedAudio')
def getPreloadedAudio():
    try:
        userId = 1
        audio = retrieve_audio_from_mysql(userId)
        audioData = []
        for a in audio:
            encoded_audio = base64.b64encode(a.file_data).decode('utf-8')
            ad = {'data': encoded_audio, 'name': a.file_name}
            audioData.append(ad)
        return jsonify(audioData)
    except Exception as e:
        print("Error:", e)
        return Response(status=500)
    
@app.route('/getUploadedAudio') #For JS
def getUploadedAudio():
    try:
        audioData = []   
        userId = session.get("userId")
        audio = retrieve_audio_from_mysql(userId)
        for a in audio:
            encoded_audio = base64.b64encode(a.file_data).decode('utf-8')
            ad = {'data': encoded_audio, 'name': a.file_name}
            audioData.append(ad)            
        return jsonify(audioData)
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/Profile/<username>', methods=['POST'])
def uploadProfileImage(username):
    try:
        user_id = session["userId"]
        username = session["username"]
        image_file = request.files['image']

        TEMP_DIR = './temp/'

        if not os.path.exists(TEMP_DIR):
            os.makedirs(TEMP_DIR)

        image_path = f"./temp/{user_id}_profile_image.jpg"
        image_file.save(image_path)

        upload_profile_image(user_id, image_path)

        if os.path.exists(TEMP_DIR):
            for file_name in os.listdir(TEMP_DIR):
                file_path = os.path.join(TEMP_DIR, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            os.rmdir(TEMP_DIR)

        return redirect(url_for('profileData', username=username))
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/adminPage')
def Admin():
    try:
        if "userIsAdmin" in session:
            if session["userIsAdmin"] == 'True':
                users = AdminRetrieve()
                profilePictures = AdminRetrieveProfilePic()

                profilePic = []
                for pic in profilePictures:
                    encoded_image = base64.b64encode(pic.file_data).decode('utf-8')
                    profilePic.append(encoded_image)

                NumberOfAccounts = len(users)
                return render_template('adminPage.html', NumberOfAccounts = NumberOfAccounts, user = users, profilePic = profilePic, username = session["username"])
            else:
                return redirect(url_for('home'))
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/upload')
def upload():
    try:
        if "userId" in session:
                return render_template('uploadPage.html', username = session["username"], isAdmin = session["userIsAdmin"])
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/Upload-images', methods=['POST'])
def upload_images():
    if 'files[]' not in request.files:
        return "No files uploaded", 400

    files = request.files.getlist('files[]')

    TEMP_DIR = './temp/'

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    for file in files:
        if file.filename != '':
            filepath = os.path.join(TEMP_DIR, file.filename)
            file.save(filepath)
            save_image_to_mysql(session.get("userId"), filepath, file.filename)

    if os.path.exists(TEMP_DIR):
        for file_name in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(TEMP_DIR)

    return

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audioFile' not in request.files:
        return "No audio file uploaded", 400

    audio_files = request.files.getlist('audioFile')
    TEMP_DIR = './temp/'

    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    for audio_file in audio_files:
        if audio_file.filename != '':
            filename = os.path.join(TEMP_DIR, audio_file.filename)
            audio_file.save(filename)
            save_audio_to_mysql(session.get("userId"), filename)

    if os.path.exists(TEMP_DIR):
        for file_name in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(TEMP_DIR)

    return "Audio file uploaded successfully"

@app.route('/workspace')
def create():
    try:
        if "userId" in session:
            return render_template('workspace.html', username = session["username"], isAdmin = session["userIsAdmin"])

    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/toggle-image', methods=['POST'])
def toggle_selected():
    image_data = request.json.get('image')
    image_name = image_data['name']

    TEMP_DIR = './Selected/'
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    image_path = os.path.join(TEMP_DIR, image_name)
    image_selected = os.path.exists(image_path)

    if image_selected:
        os.remove(image_path)
        selected = False
    else:
        with open(image_path, 'wb') as f:
            image_bytes = base64.b64decode(image_data['data'])
            f.write(image_bytes)
        selected = True
    return jsonify({'selected': selected})

@app.route('/empty-selected', methods=['POST'])
def remove_all_selected_images():
    TEMP_DIR = './Selected/'
    if os.path.exists(TEMP_DIR):
        for filename in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    
    return jsonify({'message': 'All images removed from selection'})


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

atexit.register(close_connection_pool)

if __name__ == '__main__':
    app.run(debug=True)
