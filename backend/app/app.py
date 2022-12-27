
# All Imports needed from third party resources along with some Python libraries
from flask import Flask, send_from_directory, jsonify, render_template, request, make_response, redirect, url_for, escape, send_file
import json
from flask_cors import CORS
import os
import sys
import hashlib
import secrets
import base64
from datetime import datetime, date

# Add all system paths here for when files get created.
sys.path.append('/application/backend/database')
sys.path.append('/application/backend/database/user')

# Adding imports from other files
import database
import User


app = Flask(__name__, static_folder="../../frontend/static", template_folder="../../frontend/templates")
CORS(app) # Needed for cross origin access


# This is where a user will be able to start off their adventure!
@app.route("/")
def begin():
    return render_template("index.html")


@app.route("/homepage", methods=["POST"])
def homepage():
    new_request = request
    new_request_data = new_request.form.to_dict()
    if (new_request_data["user"] == ""):
        data = "A username was not entered. Please enter a username."
        return render_template("index.html", data=data)
    
    plain_token = secrets.token_hex(32)
    token = hashlib.sha256(plain_token.encode()).digest()
    data = {
        "username" : new_request_data["user"],
        "lastQuestionSubmitted" : 1,
        "lastTime" : datetime.now().time(),
        "token" : token
    }
    
    success_user = database.insert_data(data)
    
    if success_user == -1:
        data = "This username already exists, please try a different username."
        return render_template("index.html", data=data)
    
    
    resp = redirect("/conference-room")
    resp.set_cookie("token", plain_token)
    return resp


# This route will be the main hub.
# All other routes will have some sort of linkage back to this route
@app.route("/conference-room", methods=["GET", "POST"])
def conference_room():
    if request.method == "GET":
        return render_template("conference_room.html")
    
    if request.method == "POST":
        formData = request.form.to_dict()
        print(formData)
        if "Look through the papers on the table" in formData.values():
            return redirect("/pages")
        elif "Go to the lab" in formData.values():
            return redirect("/lab-room")
        elif "Try to enter the code" in formData.values():
            return redirect("/keypad")
        elif "Read the writing on the whiteboard." in formData.values():
            return redirect("/whiteboard")
        else:
            return redirect("/conference-room")
    

@app.route("/pages")
def pages():
    return render_template("pages.html")


@app.route("/lab-room", methods=["GET", "POST"])
def lab_room():

    if request.method == "GET":

        token = request.cookies.get("token")
        # Check if the user already did this question
        passedAlready = database.check_modem_question(token)
        if passedAlready:
            new_data = "Wow! Everything is plugged in correctly and the printer is working. The printer prints out the following:"
            code = """
            R
            G
            B
            """
            return render_template("lab.html", new_data=new_data, code=code)
        return render_template("lab.html")
    
    else:

        newData = request.form.to_dict()
        token = request.cookies.get("token")

        # Check if the user already did this question
        passedAlready = database.check_modem_question(token)
        if passedAlready:
            new_data = "Wow! Everything is plugged in correctly and the printer is working. The printer prints out the following:"
            code = """
            R
            G
            B
            """
            return render_template("lab.html", new_data=new_data, code=code)



        # Implement logic to make sure their attempt does not go 
        # through until a certain amount of time has passed. This
        # should be handled before so they won't know if it is right or not.

        currTime = datetime.now().time()
        timeFromLastSubmission = database.get_time(token, currTime)

        timeDifference = datetime.combine(date.min, currTime) - datetime.combine(date.min, timeFromLastSubmission)

        timeDifference = timeDifference.seconds


        if timeDifference < 45:
            data = "You submitted too quickly! Please think about your answer choices"
            return render_template("lab.html", data=data)

        # Check if their answer is right.
        if newData["item-1"] != "Modem" or newData["item-2"] != "Router" or newData["item-3"] != "Printer":
            data = "One of your values is incorrect. Please try again"
            return render_template("lab.html", data=data)


        database.set_modem_true(token)
        new_data = "Wow! Everything is plugged in correctly and the printer is working. The printer prints out the following:"
        code = """
        R
        G
        B
        """
        return render_template("lab.html", new_data=new_data, code=code)
        


# ALL CSS ROUTES
@app.route('/<path:path>')
def serve(path):
     path_dir = os.path.abspath("../../frontend/static/css") #path react build
     if path != "" and os.path.exists(os.path.join(path_dir, path)):
         return send_from_directory(os.path.join(path_dir), path)
     else:
         return send_from_directory(os.path.join(path_dir),'index.html')



if __name__ == "__main__":
    app.run("0.0.0.0", 8080)