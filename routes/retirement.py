from flask import Blueprint, render_template, jsonify, request, session
from extensions import db
from models.user import User
import time
from sqlalchemy import text
from threading import Lock

lock = Lock()

retirement_bp = Blueprint("retirement", __name__, url_prefix="/apps/401k")

user_accounts: dict[str, dict[str, int]] = {
    "alice": {"funds": 10000_00, "balance_401k": 5000_00},
    "bob": {"funds": 12000_00, "balance_401k": 7500_00},
    "charlie": {"funds": 15000_00, "balance_401k": 8084_00},
    "admin": {"funds": 20000_00, "balance_401k": 12000_00}
}

@retirement_bp.route("/")
def retirement_dashboard():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    return render_template("401k.html", username=session["user"])

@retirement_bp.route("/balance")
def get_balance():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    username = session["user"]
    if username not in user_accounts:
        user_accounts[username] = {"funds": 10000_00, "balance_401k": 0}
        
    return jsonify(user_accounts[username])

@retirement_bp.route("/contribute", methods=["POST"])
def contribute():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    data = request.get_json()
    amount: int = data.get("amount", 0)
    
    username = session["user"]
    if username not in user_accounts:
        user_accounts[username] = {"funds": 10000_00, "balance_401k": 0}
    
    with lock:
        user_data = user_accounts[username]

        if amount <= 0:
            return jsonify({
                "message": "Invalid contribution amount!", 
                "funds": user_data["funds"],
                "balance_401k": user_data["balance_401k"]
            }), 400
        
        if amount > user_data["funds"]:
            return jsonify({
                "message": "Insufficient personal funds for this contribution!", 
                "funds": user_data["funds"],
                "balance_401k": user_data["balance_401k"]
            }), 400


        time.sleep(2)  

        company_match = round(amount * 0.5)
        total_contribution = amount + company_match

        user_data["funds"] -= amount  # Deduct funds
        user_data["balance_401k"] += total_contribution  # Add to 401k balance

    return jsonify({
        "message": f"Contributed ${amount // 100}.{(amount % 100):02}. Employer matched ${company_match // 100}.{(company_match % 100):02}!",
        "funds": user_data["funds"],
        "balance_401k": user_data["balance_401k"]
    })

@retirement_bp.route("/reset", methods=["POST"])
def reset_account():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401
        
    username = session["user"]
    if username not in user_accounts:
        return jsonify({
            "message": "Account not found!", 
            "funds": 0,
            "balance_401k": 0
        }), 404
    
    user_accounts[username] = {"funds": 10000_00, "balance_401k": 0}
    print(user_accounts[username]["balance_401k"])
    
    return jsonify({
        "message": "Account reset successfully!",
        "funds": user_accounts[username]["funds"],
        "balance_401k": user_accounts[username]["balance_401k"]
    })