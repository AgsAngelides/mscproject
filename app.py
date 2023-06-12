from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import datetime
import MySQLdb.cursors
import re
import secrets
from Crypto.Cipher import AES
import base64
from environs import Env


app = Flask(__name__)

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'project'
mysql = MySQL(app)

# Secret key for the session
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

env = Env()
env.read_env()
key = env.str("SECRET_KEY")
key_bytes = key.encode('utf-8')

# Encryption function
def encrypt_password(password):
    # Set the secret key and the mode
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    # Encode the password to bytes and pad it
    password_bytes = password.encode('utf-8')
    length = 16 - (len(password_bytes) % 16)
    password_bytes += bytes([length]) * length
    # Encrypt the password and encode it to base64
    encrypted_password_bytes = cipher.encrypt(password_bytes)
    encrypted_password = base64.b64encode(encrypted_password_bytes).decode('utf-8')
    return encrypted_password

# Decryption function
def decrypt_password(encrypted_password):
    # Set the secret key and the mode
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    # Decode the encrypted password from base64
    encrypted_password_bytes = base64.b64decode(encrypted_password)
    # Decrypt the password and remove the padding
    password_bytes = cipher.decrypt(encrypted_password_bytes)
    length = password_bytes[-1]
    password = password_bytes[:-length].decode('utf-8')
    return password


"""Home page with informed consent form. If the participant consents, take them to the optional prize draw opt in, otherwise advise them they cannot participate."""
@app.route('/', methods=['GET','POST'])
def consent():
    if request.method == 'POST':
        consent_value = request.form.get('consent', None)
        uk_based = request.form.get('uk_based', None)
        if consent_value:
            session['consent_value'] = 1 # stores consent value in the session to be used by prize draw page in determining whether the page can load
            if uk_based: # checks whether the person is UK based and if not, does not allow them to proceed
                return redirect(url_for('prize_draw'))
            else:
                return render_template('consent_required.html')
        else:
            session['consent_value'] = 0 # stores user not consented value in the session
            return render_template('consent_required.html') # renders template advising the user they must consent to be able to participate in the study
    return render_template('consent.html')


"""Renders prize draw optional opt in template"""
@app.route('/prize-draw', methods=['GET','POST'])
def prize_draw():
    consent_value = session.get('consent_value') # requests informed consent value from the session
    """If the user consented in the previous page, it loads the prize draw opt in page, otherwise takes them to the access denied page"""
    if consent_value == 1: # checks the informed consent value
        if request.method == 'POST':
            prize_draw_value = request.form.get('prize-draw', None)
            session['prize_draw_visited'] = True # stores the prize draw visited value in the session to be used when loading the next page
            if prize_draw_value:
                session['prize_draw_value'] = 1 # stores the prize draw opt in in the session to be saved in the database upon user registration
            else:
                session['prize_draw_value'] = 0 # stores prize opt out in the session to be saved in the database upon user registration
            return redirect(url_for('pre_registration_survey'))
        else:
            return render_template('prize-draw.html')
    else:
        return render_template('accessdenied.html') # renders access denied page if the user tries accessing the url extension without first consenting

"""This is the page for rendering the demographic survey and computer literacy questionnaire"""
@app.route('/pre-registration-survey', methods=['GET', 'POST'])
def pre_registration_survey():
    if 'prize_draw_visited' not in session or not session['prize_draw_visited']: # Checks if the user visited the prize draw opt in page first before allowing to access this page
        return render_template('accessdenied.html')
    else:
        if request.method == 'POST':
            """Gets the responses selected by the participant in the survey and stores them in session to be saved in the database later"""
            gender_response = request.form.get('gender', None)
            age_response = request.form.get('age', None)
            education_response = request.form.get('education', None)
            if education_response == "other":
                other_specified = request.form["other_specified"]
            else:
                other_specified = ""
            employment_response = request.form.get('employment', None)
            comp_lit_1 = request.form.get('lit_1', None)
            comp_lit_2 = request.form.get('lit_2', None)
            comp_lit_3 = request.form.get('lit_3', None)
            comp_lit_4 = request.form.get('lit_4', None)
            comp_lit_5 = request.form.get('lit_5', None)
            comp_lit_6 = request.form.get('lit_6', None)
            comp_lit_7 = request.form.get('lit_7', None)
            comp_lit_8 = request.form.get('lit_8', None)
            comp_lit_9 = request.form.get('lit_9', None)
            comp_lit_10 = request.form.get('lit_10', None)
            comp_lit_11 = request.form.get('lit_11', None)
            comp_lit_12 = request.form.get('lit_12', None)
            comp_lit_13 = request.form.get('lit_13', None)
            comp_lit_14 = request.form.get('lit_14', None)
            comp_lit_15 = request.form.get('lit_15', None)
            comp_lit_16 = request.form.get('lit_16', None)
            comp_lit_17 = request.form.get('lit_17', None)
            comp_lit_18 = request.form.get('lit_18', None)
            comp_lit_19 = request.form.get('lit_19', None)
            comp_lit_20 = request.form.get('lit_20', None)
            comp_lit_21 = request.form.get('lit_21', None)
            comp_lit_22 = request.form.get('lit_22', None)
            comp_lit_23 = request.form.get('lit_23', None)
            comp_lit_24 = request.form.get('lit_24', None)
            comp_lit_25 = request.form.get('lit_25', None)
            comp_lit_26 = request.form.get('lit_26', None)
            comp_lit_27 = request.form.get('lit_27', None)
            comp_lit_28 = request.form.get('lit_28', None)
            comp_lit_29 = request.form.get('lit_29', None)
            comp_lit_30 = request.form.get('lit_30', None)
            comp_lit_31 = request.form.get('lit_31', None)
            comp_lit_32 = request.form.get('lit_32', None)
            comp_lit_33 = request.form.get('lit_33', None)
            comp_lit_34 = request.form.get('lit_34', None)
            comp_lit_35 = request.form.get('lit_35', None)
            session['visited_pre_reg_survey'] = True # sets page visited session value to True
            # calls back all the survey responses from the session
            session['gender_response'] = gender_response
            session['age_response'] = age_response
            session['education_response'] = education_response
            session ['other_specified'] = other_specified
            session['employment_response'] = employment_response
            session['comp_lit_1'] = comp_lit_1
            session['comp_lit_2'] = comp_lit_2
            session['comp_lit_3'] = comp_lit_3
            session['comp_lit_4'] = comp_lit_4
            session['comp_lit_5'] = comp_lit_5
            session['comp_lit_6'] = comp_lit_6
            session['comp_lit_7'] = comp_lit_7
            session['comp_lit_8'] = comp_lit_8
            session['comp_lit_9'] = comp_lit_9
            session['comp_lit_10'] = comp_lit_10
            session['comp_lit_11'] = comp_lit_11
            session['comp_lit_12'] = comp_lit_12
            session['comp_lit_13'] = comp_lit_13
            session['comp_lit_14'] = comp_lit_14
            session['comp_lit_15'] = comp_lit_15
            session['comp_lit_16'] = comp_lit_16
            session['comp_lit_17'] = comp_lit_17
            session['comp_lit_18'] = comp_lit_18
            session['comp_lit_19'] = comp_lit_19
            session['comp_lit_20'] = comp_lit_20
            session['comp_lit_21'] = comp_lit_21
            session['comp_lit_22'] = comp_lit_22
            session['comp_lit_23'] = comp_lit_23
            session['comp_lit_24'] = comp_lit_24
            session['comp_lit_25'] = comp_lit_25
            session['comp_lit_26'] = comp_lit_26
            session['comp_lit_27'] = comp_lit_27
            session['comp_lit_28'] = comp_lit_28
            session['comp_lit_29'] = comp_lit_29
            session['comp_lit_30'] = comp_lit_30
            session['comp_lit_31'] = comp_lit_31
            session['comp_lit_32'] = comp_lit_32
            session['comp_lit_33'] = comp_lit_33
            session['comp_lit_34'] = comp_lit_34
            session['comp_lit_35'] = comp_lit_35
            # get the most recently added user's variant for the same gender_response
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT reg_variant as variant FROM users u INNER JOIN pre_registration_survey prs ON u.userId = prs.user_id WHERE prs.gender = %s ORDER BY u.userId DESC LIMIT 1;", [gender_response])
            results = cursor.fetchone()
            if results is None: # if there is no user for the same gender, then we set the variant value to 1 (traditional registration page)
                most_recent_variant = 1
            else:
                most_recent_variant = results['variant'] # we query the variant from the database from the latest entry and assign it to the variable
            if most_recent_variant == 1: # if the variant is 1, we take the user to registration page variant 2
                return redirect(url_for('register_2'))
            elif most_recent_variant == 2: # if the variant is 2, we take the user to the registration page variant 1
                return redirect(url_for('register_1'))
        else:
            return render_template('pre_registration_survey.html')

"""Renders the view of the registration one page and logs the time it was first opened"""   
@app.route('/register-1', methods=['GET'])
def register_1_view():
    """Displays the registration page and logs the time it was opened"""
    session['reg_page_opened'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('register_1.html')

"""Defines a route for the registration page, variant 1 - traditional registration page."""
@app.route('/register-1', methods=['GET', 'POST'])
def register_1():
    """Checks if the user visited the pre registration survey page first before loading the registration page"""
    if 'visited_pre_reg_survey' not in session or not session['visited_pre_reg_survey']:
        return render_template('accessdenied.html')
    else:
        message = '' # assigns an empty message variable to be used in the html template for rendering the messages passed by the code on the page
        if request.method == 'POST':
            session['visited_reg_page'] = True # sets page visited session value to True
            # requests the email and password from the registration form
            email = request.form['email']
            password = request.form['password']
            encrypted_password = encrypt_password(password) # encrypts password using the encryption function
            prize_draw_value = session.get('prize_draw_value') # calls back the prize draw value previously stored in session
            reg_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # assigns the current date and time to the registration date variable for when the user submits the new account form
            # calls back all demographic questionnaire and computer literacy assessment values from the session so it can be stored in the database upon the user registration
            gender_response = session.get('gender_response', None)
            age_response = session.get('age_response', None)
            education_response = session.get('education_response', None)
            other_specified = session.get('other_specified', None)
            employment_response = session.get('employment_response', None)
            comp_lit_1 = session.get('comp_lit_1', None)
            comp_lit_2 = session.get('comp_lit_2', None)
            comp_lit_3 = session.get('comp_lit_3', None)
            comp_lit_4 = session.get('comp_lit_4', None)
            comp_lit_5 = session.get('comp_lit_5', None)
            comp_lit_6 = session.get('comp_lit_6', None)
            comp_lit_7 = session.get('comp_lit_7', None)
            comp_lit_8 = session.get('comp_lit_8', None)
            comp_lit_9 = session.get('comp_lit_9', None)
            comp_lit_10 = session.get('comp_lit_10', None)
            comp_lit_11 = session.get('comp_lit_11', None)
            comp_lit_12 = session.get('comp_lit_12', None)
            comp_lit_13 = session.get('comp_lit_13', None)
            comp_lit_14 = session.get('comp_lit_14', None)
            comp_lit_15 = session.get('comp_lit_15', None)
            comp_lit_16 = session.get('comp_lit_16', None)
            comp_lit_17 = session.get('comp_lit_17', None)
            comp_lit_18 = session.get('comp_lit_18', None)
            comp_lit_19 = session.get('comp_lit_19', None)
            comp_lit_20 = session.get('comp_lit_20', None)
            comp_lit_21 = session.get('comp_lit_21', None)
            comp_lit_22 = session.get('comp_lit_22', None)
            comp_lit_23 = session.get('comp_lit_23', None)
            comp_lit_24 = session.get('comp_lit_24', None)
            comp_lit_25 = session.get('comp_lit_25', None)
            comp_lit_26 = session.get('comp_lit_26', None)
            comp_lit_27 = session.get('comp_lit_27', None)
            comp_lit_28 = session.get('comp_lit_28', None)
            comp_lit_29 = session.get('comp_lit_29', None)
            comp_lit_30 = session.get('comp_lit_30', None)
            comp_lit_31 = session.get('comp_lit_31', None)
            comp_lit_32 = session.get('comp_lit_32', None)
            comp_lit_33 = session.get('comp_lit_33', None)
            comp_lit_34 = session.get('comp_lit_34', None)
            comp_lit_35 = session.get('comp_lit_35', None)
            # calls back the email value from the session, looks it up in the database to see if the user already exists
            session['email'] = email
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE email = %s', [email])
            account = cursor.fetchone()
            if account:
                message = 'There is already an account for this email address'
            elif not password or not email:
                message = 'Please fill in email and password fields'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                message = 'Please provide a valid email address'
            else:
                reg_page_opened = session.get('reg_page_opened', None) # calls the registration page opened value from the session
                # inserts the new user into the users table, the demographic responses to the pre_registration_survey database, and the computer literacy responses to the user_literacy_responses database
                cursor.execute("INSERT INTO users (email, password, prize_draw, date_registered, reg_variant, reg_page_opened) VALUES (%s, %s, %s, %s, %s, %s)", (email, encrypted_password, prize_draw_value, reg_date, '1', reg_page_opened))
                mysql.connection.commit()
                user_id = cursor.lastrowid
                cursor.execute("INSERT INTO pre_registration_survey (user_id, gender, age, education, education_other, employment) VALUES (%s, %s, %s, %s, %s, %s)", (user_id, gender_response, age_response, education_response, other_specified, employment_response))
                cursor.execute("INSERT INTO user_literacy_responses (user_id, computer_literacy_id, response) VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s)", (user_id, '1', comp_lit_1, user_id, '2', comp_lit_2, user_id, '3', comp_lit_3, user_id, '4', comp_lit_4, user_id, '5', comp_lit_5, user_id, '6', comp_lit_6, user_id, '7', comp_lit_7,user_id, '8', comp_lit_8, user_id, '9', comp_lit_9, user_id, '10', comp_lit_10, user_id, '11', comp_lit_11, user_id, '12', comp_lit_12, user_id, '13', comp_lit_13, user_id, '14', comp_lit_14, user_id, '15', comp_lit_15, user_id, '16', comp_lit_16, user_id, '17', comp_lit_17, user_id, '18', comp_lit_18, user_id, '19', comp_lit_19, user_id, '20', comp_lit_20, user_id, '21', comp_lit_21, user_id, '22', comp_lit_22, user_id, '23', comp_lit_23, user_id, '24', comp_lit_24, user_id, '25', comp_lit_25, user_id, '26', comp_lit_26, user_id, '27', comp_lit_27, user_id, '28', comp_lit_28, user_id, '29', comp_lit_29, user_id, '30', comp_lit_30, user_id, '31', comp_lit_31, user_id, '32', comp_lit_32, user_id, '33', comp_lit_33, user_id, '34', comp_lit_34, user_id, '35', comp_lit_35))
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for('post_registration_survey_1')) # redirects the user to a follow up open ended questionnaire
        return render_template('register_1.html', message=message)

"""Renders the view of the registration two page and logs the time it was first opened"""   
@app.route('/register-2', methods=['GET'])
def register_2_view():
    """Displays the registration page and logs the time it was opened"""
    session['reg_page_opened'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    max_words = 3
    return render_template('register_2.html', max_words=max_words)

"""Defines the route for the variant 2 of the registration page"""
@app.route('/register-2', methods=['GET', 'POST'])
def register_2():
    """Checks if the user visited the pre registration survey page first before loading the registration page"""
    if 'visited_pre_reg_survey' not in session or not session['visited_pre_reg_survey']:
        return render_template('accessdenied.html')
    else:
        message = '' # assigns an empty message variable to be used in the html template for rendering the messages passed by the code on the page
        if request.method == 'POST':
            session['visited_reg_page'] = True # sets page visited session value to True
             # requests the email and password from the registration form
            email = request.form['email']
            passphrase = request.form['passphrase']
            encrypted_password = encrypt_password(passphrase) # encrypts the password
            prize_draw_value = session.get('prize_draw_value') # calls back the previously provided prize opt in value from the session
            reg_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # assigns the time the registration form is submitted to a variable
            # calls back all demographic questionnaire and computer literacy assessment responses from the session to be inserted into the database later
            gender_response = session.get('gender_response', None)
            age_response = session.get('age_response', None)
            education_response = session.get('education_response', None)
            other_specified = session.get('other_specified', None)
            employment_response = session.get('employment_response', None)
            comp_lit_1 = session.get('comp_lit_1', None)
            comp_lit_2 = session.get('comp_lit_2', None)
            comp_lit_3 = session.get('comp_lit_3', None)
            comp_lit_4 = session.get('comp_lit_4', None)
            comp_lit_5 = session.get('comp_lit_5', None)
            comp_lit_6 = session.get('comp_lit_6', None)
            comp_lit_7 = session.get('comp_lit_7', None)
            comp_lit_8 = session.get('comp_lit_8', None)
            comp_lit_9 = session.get('comp_lit_9', None)
            comp_lit_10 = session.get('comp_lit_10', None)
            comp_lit_11 = session.get('comp_lit_11', None)
            comp_lit_12 = session.get('comp_lit_12', None)
            comp_lit_13 = session.get('comp_lit_13', None)
            comp_lit_14 = session.get('comp_lit_14', None)
            comp_lit_15 = session.get('comp_lit_15', None)
            comp_lit_16 = session.get('comp_lit_16', None)
            comp_lit_17 = session.get('comp_lit_17', None)
            comp_lit_18 = session.get('comp_lit_18', None)
            comp_lit_19 = session.get('comp_lit_19', None)
            comp_lit_20 = session.get('comp_lit_20', None)
            comp_lit_21 = session.get('comp_lit_21', None)
            comp_lit_22 = session.get('comp_lit_22', None)
            comp_lit_23 = session.get('comp_lit_23', None)
            comp_lit_24 = session.get('comp_lit_24', None)
            comp_lit_25 = session.get('comp_lit_25', None)
            comp_lit_26 = session.get('comp_lit_26', None)
            comp_lit_27 = session.get('comp_lit_27', None)
            comp_lit_28 = session.get('comp_lit_28', None)
            comp_lit_29 = session.get('comp_lit_29', None)
            comp_lit_30 = session.get('comp_lit_30', None)
            comp_lit_31 = session.get('comp_lit_31', None)
            comp_lit_32 = session.get('comp_lit_32', None)
            comp_lit_33 = session.get('comp_lit_33', None)
            comp_lit_34 = session.get('comp_lit_34', None)
            comp_lit_35 = session.get('comp_lit_35', None)
            # calls back the email address from the session and then looks up the user against this email address in the database
            session['email'] = email
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE email = %s', [email])
            account = cursor.fetchone()
            if account:
                message = 'The account for this email address already exists.'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                message = 'Please provide a valid email address.'
            elif not passphrase or not email:
                message = 'Please fill out email and password fields.'
            else:
                # if the user does not exist, the user is inserted into the database, including the demographic questionnaire and computer literacy assessment responses
                reg_page_opened = session.get('reg_page_opened', None)
                cursor.execute("INSERT INTO users (email, password, prize_draw, date_registered, reg_variant, reg_page_opened) VALUES (%s, %s, %s, %s, %s, %s)", (email, encrypted_password, prize_draw_value, reg_date, '2', reg_page_opened))
                mysql.connection.commit()
                user_id = cursor.lastrowid
                cursor.execute("INSERT INTO pre_registration_survey (user_id, gender, age, education, education_other, employment) VALUES (%s, %s, %s, %s, %s, %s)", (user_id, gender_response, age_response, education_response, other_specified, employment_response))
                cursor.execute("INSERT INTO user_literacy_responses (user_id, computer_literacy_id, response) VALUES (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s), (%s, %s, %s)", (user_id, '1', comp_lit_1, user_id, '2', comp_lit_2, user_id, '3', comp_lit_3, user_id, '4', comp_lit_4, user_id, '5', comp_lit_5, user_id, '6', comp_lit_6, user_id, '7', comp_lit_7,user_id, '8', comp_lit_8, user_id, '9', comp_lit_9, user_id, '10', comp_lit_10, user_id, '11', comp_lit_11, user_id, '12', comp_lit_12, user_id, '13', comp_lit_13, user_id, '14', comp_lit_14, user_id, '15', comp_lit_15, user_id, '16', comp_lit_16, user_id, '17', comp_lit_17, user_id, '18', comp_lit_18, user_id, '19', comp_lit_19, user_id, '20', comp_lit_20, user_id, '21', comp_lit_21, user_id, '22', comp_lit_22, user_id, '23', comp_lit_23, user_id, '24', comp_lit_24, user_id, '25', comp_lit_25, user_id, '26', comp_lit_26, user_id, '27', comp_lit_27, user_id, '28', comp_lit_28, user_id, '29', comp_lit_29, user_id, '30', comp_lit_30, user_id, '31', comp_lit_31, user_id, '32', comp_lit_32, user_id, '33', comp_lit_33, user_id, '34', comp_lit_34, user_id, '35', comp_lit_35))
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for('post_registration_survey_2'))
        max_words = 3  # Define the maximum number of words displayed on the page
        return render_template('register_2.html', message=message, max_words=max_words) # renders the registration two template using the message passed by the code and the number of words

"""Defines the route for the post-registration survey presented for the registration page variant 1"""
@app.route('/post-registration-survey-1', methods=['GET', 'POST'])
def post_registration_survey_1():
    # checks if the user visited the registration page first, if not, access denied is presented
    if 'visited_reg_page' not in session or not session['visited_reg_page']:
        return render_template('accessdenied.html')
    else:
        if request.method == 'POST':
            session['visited_post_reg_survey'] = True # sets page visited session value to True
            # calls back the user email from the session and assigns the user responses provided in the form to the variables
            email = session.get('email')
            overall_experience = request.form['overall_experience']
            reg_frustration = request.form['reg_frustration']
            # connects to the database to find the user for the email address passed in session
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT userId as user_id FROM users WHERE email = %s', [email])
            account = cursor.fetchone()
            user_id = account['user_id'] # fecthes the user id for the email address from the session
            # inserts the user pos registration follow up survey responses in the database and presents a thank you page
            cursor.execute("INSERT INTO post_registration_survey (user_id, overall_experience, page_layout, reg_frustration) VALUES (%s, %s, %s, %s)", (user_id, overall_experience, "", reg_frustration))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('phase_one_thank_you'))
        return render_template('post_registration_survey_1.html')

"""Defines the route for the post-registration survey presented for the registration page variant 2, which asks one additional question when compared to page 1 post registration follow up survey"""
@app.route('/post-registration-survey-2', methods=['GET', 'POST'])
def post_registration_survey_2():
    # checks if the user visited the registration page first, if not, access denied is presented
    if 'visited_reg_page' not in session or not session['visited_reg_page']:
        return render_template('accessdenied.html')
    else:
        if request.method == 'POST':
            session['visited_post_reg_survey'] = True # sets page visited session value to True
            # calls back the user email from the session and assigns the user responses provided in the form to the variables
            email = session.get('email')
            overall_experience = request.form['overall_experience']
            page_layout = request.form['page_layout']
            reg_frustration = request.form['reg_frustration']
            # connects to the database to find the user for the email address passed in session
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT userId as user_id FROM users WHERE email = %s', [email])
            account = cursor.fetchone()
            user_id = account['user_id'] # fecthes the user id for the email address from the session
             # inserts the user pos registration follow up survey responses in the database and presents a thank you page
            cursor.execute("INSERT INTO post_registration_survey (user_id, overall_experience, page_layout, reg_frustration) VALUES (%s, %s, %s, %s)", (user_id, overall_experience, page_layout, reg_frustration))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('phase_one_thank_you'))
        return render_template('post_registration_survey_2.html')

"""Renders phase 1 thank you message presented upon the post-registration survey completion"""
@app.route('/phase-one-thank-you')
def phase_one_thank_you():
    if 'visited_post_reg_survey' not in session or not session['visited_post_reg_survey']:
        return render_template('accessdenied.html')
    else:
        return render_template('phase_one_thank_you.html')

"""Renders the login page and logs the time the page was first opened"""
@app.route('/login', methods=['GET'])
def login_view():
    """Displays the registration page"""
    attempts = 0
    session['login_page_opened'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template('login.html', attempts = attempts)

"""Defines the logic of the registration page"""
@app.route('/login', methods =['GET', 'POST'])
def login():
    message = '' # assigns an empty message variable to be used in the html template for rendering the messages passed by the code on the page
    user_id = None  # sets the variable to None initially
    attempts = 0 # sets the initial login attempts to 0 for any user who previously didn't attempt to login
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form: 
        session['visited_login_page'] = True # sets page visited session value to True
        # requests the email and password from the login form
        email = request.form['email']
        password = request.form['password']
        login_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # sets the login submission date
        # looks up the user in the database using the email provided
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()
        if user:
            # finds the number of previous unsucsessful login attempts from the database for the user the email belongs to
            user_id = user['userId']
            session['user_id'] = user_id
            cursor.execute ("SELECT count(user_id) as login_attempts FROM user_login WHERE user_id = %s and failed_login = 'yes'", (user_id,))
            results = cursor.fetchone()
            attempts = results['login_attempts'] # stores the number of attempts from the database in the variable; this is used for the html template which allows to bypass the login process after 3 unsuccessful attempts
            login_page_opened = session.get('login_page_opened', None)
            if decrypt_password(user['password']) == password: # decrypts the password and checks if it matches the user provided password, if it does, we store the login attempt in the database and redirect the participant to a follow up questionnaire
                session['loggedin'] = True
                session['email'] = user['email']
                cursor.execute("INSERT INTO user_login (user_id, login_attempted_on, failed_login, login_page_opened) VALUES (%s, %s, %s, %s)", (user_id, login_date, 'no', login_page_opened))
                mysql.connection.commit()
                cursor.close()
                return redirect(url_for('post_login_survey'))
            else:
                # if the password is incorrect, we also store this attempt in the database and ask the user to provide the correct one
                cursor.execute("INSERT INTO user_login (user_id, login_attempted_on, failed_login, login_page_opened) VALUES (%s, %s, %s, %s)", (user_id, login_date, 'yes', login_page_opened))
                mysql.connection.commit()
                cursor.close()
                message = 'Please provide correct password'
        else:
            message= 'Please provide correct email address and password'
    return render_template('login.html', message = message, attempts = attempts)

"""Renders the page for the post login survey to be displayed when the user has logged in or after the user bypassed the login process after 3 unsuccessful attempts"""
@app.route('/post-login-survey', methods=['GET', 'POST'])
def post_login_survey():
    # checks if the user visited a login page first before allowing to access this page
    if 'visited_login_page' not in session or not session['visited_login_page']:
        return render_template('accessdenied.html')
    else:
        # calls user ID from the session and then looks up the number of failed login attempts for the user
        user_id = session.get('user_id', None)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute ("SELECT count(user_id) as login_attempts FROM user_login WHERE user_id = %s and failed_login = 'yes'", (user_id,))
        results = cursor.fetchone()
        attempts = results['login_attempts']
        if request.method == 'POST':
            login_experience = request.form['login_experience']
            login_frustration = request.form['login_frustration']
            # if the user fails login more than 3 times, we ask the user to answer an additional question and store responses in the database
            if attempts >=3:
                recall = request.form['recall']
                cursor.execute("INSERT INTO post_login_survey (user_id, login_experience, login_frustration, recall) VALUES (%s, %s, %s, %s)", (user_id, login_experience, login_frustration, recall))
                mysql.connection.commit()
                cursor.close()
            # if the user logs in successfully, we ask two initial questions and store responses in the database
            else:
                recall = ""
                cursor.execute("INSERT INTO post_login_survey (user_id, login_experience, login_frustration, recall) VALUES (%s, %s, %s, %s)", (user_id, login_experience, login_frustration, recall))
                mysql.connection.commit()
                cursor.close()
            return redirect(url_for('phase_two_thank_you')) # calls phase 2 thank you message
        return render_template('post_login_survey.html', attempts = attempts)

"""Renders phase 2 thank you message page"""
@app.route('/phase-two-thank-you')
def phase_two_thank_you():
        return render_template('phase_two_thank_you.html')
    
if __name__ == "__main__":
    app.run(debug=True)