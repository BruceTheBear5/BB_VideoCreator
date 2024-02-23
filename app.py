from flask import Flask, render_template, request, redirect, url_for, flash, session, Response
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from MySQL import User, retrieve_users_from_mysql, save_data_to_mysql, retrieve_image_from_mysql, retrieve_profile_image, upload_profile_image, AdminRetrieve, AdminRetrieveProfilePic, retrieve_audio_from_mysql, save_image_to_mysql, save_audio_to_mysql
import os
import base64

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["JWT_TOKEN_LOCATION"] = ["headers","cookies","json","query_string"]
app.config["JWT_SECRET_KEY"] = os.urandom(24)
jwt = JWTManager(app)

@app.route('/')
def home():
    if 'jwt_token' in session:
        user_info = session['jwt_token']
        if user_info.get("isAdmin"):
            return render_template('index.html', isAdmin="True", user="True", username=user_info.get("username"))
        else:
            return render_template('index.html', isAdmin="False", user="True", username=user_info.get("username"))
    return render_template('index.html', isAdmin="False", user="False")

@app.route('/signin')
def signin():
    return render_template('login.html', signin="True", signup="False", ForgetPassword="False")

@app.route('/signup')
def signup():
    return render_template('login.html', signin="False", signup="True", ForgetPassword="False")

@app.route('/forgetpassword')
def forgetPassword():
    return render_template('login.html', signin="False", signup="False", ForgetPassword="True")

@app.route('/SignIn', methods=['POST'])
def signinFunc():
    email = request.form['email']
    password = request.form['password']
    user = retrieve_users_from_mysql(email)
    if user == None:
        flash('No User Found')
        return redirect(url_for('signin'))
    elif check_password_hash(user.password, password):
        access_token = create_access_token(identity={"userId": user.id, "username": user.username, "isAdmin": user.isAdmin})
        user_info = {"userId": user.id, "username": user.username,"email": user.email , "isAdmin": user.isAdmin}
        session['jwt_token'] = user_info
        if user.isAdmin:
            flash('Admin SignIn Successful')
        else:
            flash('SignIn Successful')
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
        access_token = create_access_token(identity={"userId": user.id, "username": user.username, "isAdmin": user.isAdmin})
        user_info = {"userId": user.id, "username": user.username,"email": user.email ,"isAdmin": user.isAdmin}
        session['jwt_token'] = user_info
        flash('Registration Successful')
        return redirect(url_for('home'))   
    else:
        flash('Email already exists')
        return redirect(url_for('signup'))

@app.route('/profile/<username>', methods=['GET'])
def profileData(username):
    try:
        if "jwt_token" in session:
            user_info = session["jwt_token"]
            user = retrieve_users_from_mysql(user_info["email"])
            profile_image = retrieve_profile_image(user.id)
            profileImage = base64.b64encode(profile_image.file_data).decode('utf-8')
            images = retrieve_image_from_mysql(user.id)
            imageData = []
            for i in images:
                encoded_image = base64.b64encode(i.file_data).decode('utf-8')
                img = {'data': encoded_image, 'name': i.file_name}
                imageData.append(img)

            audio = retrieve_audio_from_mysql(user.id)
            audioData = []
            for a in audio:
                encoded_audio = base64.b64encode(a.file_data).decode('utf-8')
                ad = {'data': encoded_audio, 'name': a.file_name}
                audioData.append(ad)

            return render_template('profile.html', user=user, profileImage=profileImage, images=imageData, audio=audioData, username=user.username, isAdmin=user.isAdmin)
        else:
            return redirect(url_for('home'))
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/Profile/<username>', methods=['POST'])
def uploadProfileImage(username):
    try:
        if "jwt_token" in session:
            user_info = session["jwt_token"]
            user_id = user_info["userId"]
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
        if "jwt_token" in session:
            user_info = session["jwt_token"]
            if user_info["isAdmin"] == 'True':
                users = AdminRetrieve()
                profilePictures = AdminRetrieveProfilePic()

                profilePic = []
                for pic in profilePictures:
                    encoded_image = base64.b64encode(pic.file_data).decode('utf-8')
                    profilePic.append(encoded_image)

                NumberOfAccounts = len(users)
                return render_template('adminPage.html', NumberOfAccounts=NumberOfAccounts, user=users, profilePic=profilePic, username=user_info["username"])
            else:
                return redirect(url_for('home'))
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/upload-images')
def upload():
    try:
        if "jwt_token" in session:
            user_info = session["jwt_token"]
            return render_template('uploadPage.html', username=user_info["username"], isAdmin=user_info["isAdmin"])
        else:
            return redirect(url_for('signin'))  # Redirect to signin if user not logged in
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/Upload', methods=['POST'])
def upload_images():
    try:
        if "jwt_token" in session:
            user_info = session["jwt_token"]
            if 'files[]' not in request.files:
                return "No files uploaded", 400

            files = request.files.getlist('files[]')

            TEMP_DIR = './temp/'

            if not os.path.exists(TEMP_DIR):
                os.makedirs(TEMP_DIR)

            for file in files:
                if file.filename != '':
                    filename = os.path.join(TEMP_DIR, file.filename)
                    file.save(filename)
                    save_image_to_mysql(user_info["userId"], filename)

            if os.path.exists(TEMP_DIR):
                for file_name in os.listdir(TEMP_DIR):
                    file_path = os.path.join(TEMP_DIR, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(TEMP_DIR)

            return redirect(url_for('create'))
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/create-video')
def create():
    try:
        if "jwt_token" in session:
            user_info = session["jwt_token"]
            images = retrieve_image_from_mysql(user_info["userId"])
            imageData = []
            for i in images:
                encoded_image = base64.b64encode(i.file_data).decode('utf-8')
                img = {'data': encoded_image, 'name': i.file_name}
                imageData.append(img)

            audio = retrieve_audio_from_mysql(1)
            audioData = []
            for a in audio:
                encoded_audio = base64.b64encode(a.file_data).decode('utf-8')
                ad = {'data': encoded_audio, 'name': a.file_name}
                audioData.append(ad)
            audio = retrieve_audio_from_mysql(user_info["userId"])
            for a in audio:
                encoded_audio = base64.b64encode(a.file_data).decode('utf-8')
                ad = {'data': encoded_audio, 'name': a.file_name}
                audioData.append(ad)

            return render_template('workspace.html', images=imageData, audio=audioData, username=user_info["username"], isAdmin=user_info["isAdmin"])

    except Exception as e:
        print("Error:", e)
        return Response(status=500)

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    try:
        if "jwt_token" in session:
            user_info = session["jwt_token"]
            if 'audioFile' not in request.files:
                return "No audio file uploaded", 400

            audio_file = request.files['audioFile']
            TEMP_DIR = './temp/'

            if not os.path.exists(TEMP_DIR):
                os.makedirs(TEMP_DIR)

            if audio_file.filename != '':
                filename = os.path.join(TEMP_DIR, audio_file.filename)
                audio_file.save(filename)
                save_audio_to_mysql(user_info["userId"], filename)

            if os.path.exists(TEMP_DIR):
                for file_name in os.listdir(TEMP_DIR):
                    file_path = os.path.join(TEMP_DIR, file_name)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                os.rmdir(TEMP_DIR)

            return "Audio file uploaded successfully"
    except Exception as e:
        print("Error:", e)
        return Response(status=500)

if __name__ == '__main__':
    app.run(debug=True)
