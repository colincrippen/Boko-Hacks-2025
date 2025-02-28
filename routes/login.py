from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from flask_mailman import EmailMessage
from models.user import User
from extensions import db, mail
import time
login_bp = Blueprint("login", __name__)

MAX_ATTEMPTS = 3 # max fails
TIMEOUT_SECONDS = 180
@login_bp.route("/login", methods=["GET", "POST"])
def login():
    #timeout
    if "lockout_time" in session:
        elapsed_time = time.time() - session["lockout_time"]
        if elapsed_time < TIMEOUT_SECONDS:
            remaining_time = int(TIMEOUT_SECONDS - elapsed_time)
            flash(f"Too many failed attempts. Try again in {remaining_time} seconds.", "error")
            return render_template("login.html")
        else:
            session.pop("lockout_time", None)
            session["attempts"] = 0
    #fail attempt counter
    if "attempts" not in session:
        session["attempts"] = 0 # default set fails to 0
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        if user:
            if user.check_password(password):
                session["user"] = user.username
                session.pop("attempts", None)
                session.pop("lockout_time", None)
                #send email saying someone has logged into their account
                send_login_email(user.email)
                flash("Login successful!", "success")
                return redirect(url_for("hub.hub"))
            else:
                session["attempts"] += 1 # addition to fail counter
                remaining_attempts = MAX_ATTEMPTS - session["attempts"]
                if session["attempts"] >= MAX_ATTEMPTS:
                    #send email to user saying they account is trying to be accesed 
                    send_login_email(user.email, lockout=True)
                    session["lockout_time"] = time.time()
                    flash(f"Too many failed attempts. Try again in {TIMEOUT_SECONDS} seconds.", "error")
                else:
                    flash(f"Invalid username or password. Attempts left: {remaining_attempts}", "error")


    return render_template("login.html")

@login_bp.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("attempts", None)
    session.pop("lockout_time", None)
    session.pop('_flashes',None)
    session.pop('admin_logged_in', False) #logs out of admin log in
    flash("You have been logged out.", "info")
    return redirect(url_for("login.login"))


def send_login_email(email: str, lockout: bool = False) -> None:
    """Send an email alert when a login attempt is made."""
    print(f"attempting to send email to {email}")
    subject = "New login successful"
    body = "A new login has been detected! If this wasn't you, good luck."

    if lockout:
        body = "Someone failed to log into your account 3 times! Yikes!"

    msg = EmailMessage(subject, body, to=[email])
    msg.send()