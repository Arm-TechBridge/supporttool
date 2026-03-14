"""
ARM TechBridge AI Workspace SerDesk
-----------------------------------

SETUP INSTRUCTIONS

1) Install dependencies

pip install flask flask-jwt-extended flask-bcrypt flask-socketio
pip install psycopg2-binary python-dotenv openai

2) Supabase Setup
Create database in Supabase
Copy credentials

Replace below:

SUPABASE_HOST
SUPABASE_DB
SUPABASE_USER
SUPABASE_PASSWORD

3) Gmail SMTP

Enable app password in Gmail

Set:

SMTP_EMAIL = "armtechbridge@gmail.com"
SMTP_PASSWORD = "APP_PASSWORD"

4) Run server

python app.py

Master Admin Default Login

Email: armtechbridge@gmail.com
Password: Temp@1234
"""

from flask import Flask, request, jsonify, render_template_string
from flask_jwt_extended import (
create_access_token,
jwt_required,
JWTManager,
get_jwt_identity
)
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
import psycopg2
import smtplib
import random
import datetime
import openai

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "arm-techbridge-secret"

jwt = JWTManager(app)
bcrypt = Bcrypt(app)
socketio = SocketIO(app)

# ---------------------------------
# DATABASE CONFIG
# ---------------------------------

DB_HOST = "SUPABASE_HOST"
DB_NAME = "SUPABASE_DB"
DB_USER = "SUPABASE_USER"
DB_PASS = "SUPABASE_PASSWORD"

def get_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# ---------------------------------
# MASTER ADMIN AUTO CREATION
# ---------------------------------

def create_master_admin():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE role='master_admin'")
    admin = cur.fetchone()

    if not admin:

        password = bcrypt.generate_password_hash("Temp@1234").decode()

        cur.execute("""
        INSERT INTO users (email,password,role)
        VALUES (%s,%s,%s)
        """,(
        "armtechbridge@gmail.com",
        password,
        "master_admin"
        ))

        conn.commit()

    conn.close()

create_master_admin()

# ---------------------------------
# LOGIN PAGE
# ---------------------------------

login_page = """

<html>
<head>

<title>ARM TechBridge AI Workspace</title>

<script src="https://cdn.tailwindcss.com"></script>

</head>

<body class="bg-gray-900 text-white flex items-center justify-center h-screen">

<div class="bg-gray-800 p-10 rounded-xl w-96">

<h1 class="text-2xl mb-5 font-bold">SerDesk Login</h1>

<input id="email" class="w-full p-2 mb-3 bg-gray-700 rounded" placeholder="Email">

<input id="password" type="password" class="w-full p-2 mb-3 bg-gray-700 rounded" placeholder="Password">

<button onclick="login()" class="bg-blue-600 w-full p-2 rounded">Login</button>

</div>

<script>

async function login(){

let email=document.getElementById("email").value
let password=document.getElementById("password").value

let r=await fetch("/api/login",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({email,password})
})

let d=await r.json()

if(d.token){
localStorage.token=d.token
window.location="/dashboard"
}else{
alert("Login failed")
}

}

</script>

</body>
</html>

"""

@app.route("/")
def login():
    return render_template_string(login_page)

# ---------------------------------
# LOGIN API
# ---------------------------------

@app.route("/api/login",methods=["POST"])
def api_login():

    data=request.json
    email=data["email"]
    password=data["password"]

    conn=get_db()
    cur=conn.cursor()

    cur.execute("SELECT id,password FROM users WHERE email=%s",(email,))
    user=cur.fetchone()

    if not user:
        return jsonify({"error":"user not found"})

    if bcrypt.check_password_hash(user[1],password):

        token=create_access_token(identity=user[0])

        return jsonify({"token":token})

    return jsonify({"error":"invalid credentials"})

# ---------------------------------
# DASHBOARD UI
# ---------------------------------

dashboard_html="""

<html>
<head>

<script src="https://cdn.tailwindcss.com"></script>

</head>

<body class="bg-gray-900 text-white">

<div class="flex">

<div class="w-60 bg-gray-800 h-screen p-5">

<h1 class="text-xl mb-6">SerDesk</h1>

<a href="#" onclick="loadTickets()" class="block mb-3">Tickets</a>

<a href="#" onclick="loadNotes()" class="block mb-3">Notes</a>

</div>

<div class="flex-1 p-6">

<h2 class="text-2xl mb-5">Dashboard</h2>

<div id="content"></div>

</div>

</div>

<script>

async function loadTickets(){

let r=await fetch("/api/tickets",{
headers:{
Authorization:"Bearer "+localStorage.token
}
})

let d=await r.json()

let html="<h2>Tickets</h2>"

d.forEach(t=>{
html+=`<div class='p-3 bg-gray-800 mb-2'>${t.title}</div>`
})

document.getElementById("content").innerHTML=html

}

async function loadNotes(){

let r=await fetch("/api/notes",{
headers:{
Authorization:"Bearer "+localStorage.token
}
})

let d=await r.json()

let html="<h2>Notes</h2>"

d.forEach(n=>{
html+=`<div class='p-3 bg-gray-800 mb-2'>${n.content}</div>`
})

document.getElementById("content").innerHTML=html

}

</script>

</body>
</html>

"""

@app.route("/dashboard")
def dashboard():
    return render_template_string(dashboard_html)

# ---------------------------------
# TICKETS API
# ---------------------------------

@app.route("/api/tickets")
@jwt_required()
def tickets():

    conn=get_db()
    cur=conn.cursor()

    cur.execute("SELECT id,title FROM tickets")

    rows=cur.fetchall()

    tickets=[{"id":r[0],"title":r[1]} for r in rows]

    return jsonify(tickets)

# ---------------------------------
# NOTES API
# ---------------------------------

@app.route("/api/notes")
@jwt_required()
def notes():

    conn=get_db()
    cur=conn.cursor()

    cur.execute("SELECT id,content FROM notes")

    rows=cur.fetchall()

    notes=[{"id":r[0],"content":r[1]} for r in rows]

    return jsonify(notes)

# ---------------------------------
# PASSWORD RESET OTP
# ---------------------------------

SMTP_EMAIL="armtechbridge@gmail.com"
SMTP_PASS="SMTP_PASSWORD"

def send_otp(email,otp):

    s=smtplib.SMTP("smtp.gmail.com",587)
    s.starttls()

    s.login(SMTP_EMAIL,SMTP_PASS)

    msg=f"Your OTP is {otp}"

    s.sendmail(SMTP_EMAIL,email,msg)

    s.quit()

@app.route("/api/forgot",methods=["POST"])
def forgot():

    email=request.json["email"]

    otp=random.randint(100000,999999)

    conn=get_db()
    cur=conn.cursor()

    cur.execute("""
    INSERT INTO otp_codes(email,otp,expiry)
    VALUES(%s,%s,%s)
    """,(
    email,
    otp,
    datetime.datetime.utcnow()+datetime.timedelta(minutes=10)
    ))

    conn.commit()

    send_otp(email,otp)

    return jsonify({"message":"OTP sent"})

# ---------------------------------
# AI SEARCH
# ---------------------------------

openai.api_key="OPENAI_API_KEY"

@app.route("/api/ai-search",methods=["POST"])
@jwt_required()
def ai_search():

    query=request.json["query"]

    res=openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[
    {"role":"user","content":query}
    ]
    )

    return jsonify(res.choices[0].message.content)

# ---------------------------------

if __name__=="__main__":

    socketio.run(app,port=5000)
