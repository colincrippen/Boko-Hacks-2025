import requests
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from extensions import db
import re
import os

register_bp = Blueprint("register", __name__)

# Load reCAPTCHA secret key from environment variables
RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY")

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        recaptcha_response = request.form.get("g-recaptcha-response")

        # Verify reCAPTCHA
        if not verify_recaptcha(recaptcha_response):
            flash("reCAPTCHA verification failed. Please try again.", "error")
            return redirect(url_for("register.register"))

        if not valid_password(password):
            flash("Password not secure enough. Please try again.", "error")
            return redirect(url_for("register.register"))

        if password != confirm_password:
            flash("Passwords do not match. Please try again.", "error")
            return redirect(url_for("register.register"))

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for("register.register"))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login.login"))

    return render_template("register.html")

def verify_recaptcha(recaptcha_response):
    """Verify reCAPTCHA response with Google's API."""
    if not recaptcha_response:
        return False

    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": RECAPTCHA_SECRET_KEY,
        "response": recaptcha_response
    }
    
    try:
        response = requests.post(url, data=data)
        result = response.json()
        return result.get("success", False)
    except requests.exceptions.RequestException:
        return False

def valid_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

    return True