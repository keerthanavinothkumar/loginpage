import pyrebase

config = {
"apiKey": "AIzaSyD3wb0yFOBtuUPG1EmtESi_3cXg5yboNU8",
"authDomain": "test-5d0a9.firebaseapp.com",
"databaseURL": "https://test-5d0a9-default-rtdb.firebaseio.com",
"projectId": "test-5d0a9",
"storageBucket": "test-5d0a9.appspot.com",
"messagingSenderId": "29300325919",
"appId": "1:29300325919:web:b8aa97f6ac3f4eb8cfdf2a",
"measurementId": "G-63VM8J5WG6"
}


#initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
print ("\n\n\nDBBBBBBBBBBBBBBBB", db)

from flask import Flask, redirect, url_for, request, render_template
app = Flask(__name__, template_folder='template', static_folder='static')

#Initialze person as dictionary
person = {"is_logged_in": False, "name": "", "email": "", "uid": ""}

#Login
#@app.route("/")
@app.route('/')
def base():
    #return "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    return redirect(url_for('login'))

#Login
#@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    #return "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    return render_template("login.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")



#Welcome page
@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if person["is_logged_in"] == True:
        return render_template("welcome.html", email = person["email"], name = person["name"])
    else:
        return redirect(url_for('login'))


#If someone clicks on login, they are redirected to /result
@app.route("/result", methods = ['POST', 'GET'])
def result():
    print ("\n\n\n\nCallingg")
    if request.method == 'POST':        #Only if data has been posted
        result = request.form           #Get the data
        email = result["email"]
        password = result["pass"]
        try:

            #Try signing in the user with the given information
            user = auth.sign_in_with_email_and_password(email, password)

            #Insert the user data in the global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            #Get the name of the user
            data = db.child("users").get()
            person["name"] = data.val()[person["uid"]]["name"]
            #Redirect to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect back to login
            return redirect(url_for('login'))
    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

#If someone clicks on register, they are redirected to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
    print ("\n\n\n\nCallingg Register")
    print ("request.method", request.method)
    if request.method == "POST":        #Only listen to POST
        result = request.form
        print ("result-----", result)        #Get the data submitted
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        try:
            print ("--------\n\n\n\n", email, password)
            #Try creating the user account using the provided data
            auth.create_user_with_email_and_password(email, password)
            print ("1\n\n\n\n11111")
            #Login the user
            user = auth.sign_in_with_email_and_password(email, password)
            print ("2222222222")
            #Add data to global person
            global person
            person["is_logged_in"] = True
            person["email"] = user["email"]
            person["uid"] = user["localId"]
            person["name"] = name
            print ("33333", person)
            #Append data to the firebase realtime database
            data = {"name": name, "email": email}
            db.child("users").child(person["uid"]).set(data)
            #Go to welcome page
            return redirect(url_for('welcome'))
        except:
            #If there is any error, redirect to register
            return redirect(url_for('register'))

    else:
        if person["is_logged_in"] == True:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('register'))



if __name__ == "__main__":
    app.run(debug=True)
