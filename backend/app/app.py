
# All Imports needed from third party resources along with some Python libraries
from flask import Flask, send_from_directory, jsonify, render_template, request, make_response, redirect, url_for, escape, send_file
import json
from flask_cors import CORS
import os
import sys
import hashlib
import secrets
import base64

# Add all system paths here for when files get created.
sys.path.append('/application/backend/database')
sys.path.append('/application/backend/database/exceptions')
sys.path.append('/application/backend/database/user')

# Adding imports from other files
import database
import exceptions
import User


app = Flask(__name__, static_folder="../../frontend", template_folder="../../frontend")
CORS(app)

@app.route("/")
def homepage():
    return render_template("index.html")

