from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from extensions import db
import re

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        email = request.form.get("email")
        captcha_response = request.form.get("captcha")
        stored_captcha = session.get("captcha_text")

        if not valid_password(password):
            flash("Password not secure enough. Please try again.", "error")
            return redirect(url_for("register.register"))

        if password != confirm_password:
            flash("Passwords do not match. Please try again.", "error")
            return redirect(url_for("register.register"))
        if not is_valid_email(email):
            flash("Email not Valid. Please try again.", "error")
            return redirect(url_for("register.register"))
        if not stored_captcha or captcha_response.upper() != stored_captcha:
            flash("Invalid CAPTCHA. Please try again.", "error")
            return redirect(url_for("register.register"))

        session.pop("captcha_text", None)

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for("register.register"))
        
        existing_email = User.query.filter_by(email=email).first()

        if existing_email:
            flash("Email already exists. Please choose a different one.", "error")
            return redirect(url_for("register.register"))
        
        new_user = User(username=username)
        new_user.set_password(password)
        new_user.email(email)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for("login.login"))

    return render_template("register.html")

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

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None