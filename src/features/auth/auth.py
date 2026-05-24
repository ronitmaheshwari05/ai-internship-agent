import os
import pyrebase
from dotenv import load_dotenv

load_dotenv()

firebaseConfig = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
};

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

def signup(email, password):

    try:

        user = auth.create_user_with_email_and_password(
            email,
            password
        )

        return user

    except Exception as e:

        return str(e)


def login(email, password):

    try:

        user = auth.sign_in_with_email_and_password(
            email,
            password
        )

        return user

    except Exception as e:

        return str(e)