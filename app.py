from flask import Flask, render_template, request, redirect, jsonify,flash,session
import mysql.connector

app = Flask(__name__)

app.secret_key = "food_wastage_project_2026"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sanu2924",
    database="food_tracking_db"
)

cursor = db.cursor()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cursor.execute(
            "INSERT INTO users (name,email,password) VALUES (%s,%s,%s)",
            (name,email,password)
        )
        db.commit()
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Step 1: check empty
        if not email or not password:
            flash("⚠ Please enter both email and password!", "error")
            return redirect('/login')

        # Step 2: check DB
        cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
        user = cursor.fetchone()

        if user:
            session['user'] = email   # ⭐ IMPORTANT LINE
            flash("✅ Login successful!", "success")
            return redirect('/dashboard')
        else:
            flash("❌ Invalid email or password!", "error")
            return redirect('/login')

    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    if 'user' not in session:
        flash("⚠ Please login first!", "error")
        return redirect('/login')

    return render_template("dashboard.html")

@app.route('/accept_food/<int:id>')
def accept_food(id):
    cursor.execute("UPDATE food_posts SET status='accepted' WHERE id=%s", (id,))
    db.commit()
    return "success"

# ADD FOOD
@app.route('/add_food', methods=['POST'])
def add_food():
    food = request.form['food']
    qty = request.form['qty']
    expiry = request.form['expiry']
    contact = request.form['contact']
    phone = request.form['phone']

    cursor.execute(
        "INSERT INTO food_posts (food,qty,expiry,contact,phone,status) VALUES (%s,%s,%s,%s,%s,'available')",
        (food,qty,expiry,contact,phone)
    )
    db.commit()
    return "success"

# GET FOOD
@app.route('/get_food')
def get_food():
    cursor.execute("SELECT * FROM food_posts")
    data = cursor.fetchall()

    result = []
    for row in data:
        result.append({
            "id": row[0],
            "food": row[1],
            "qty": row[2],
            "expiry": str(row[3]),
            "contact": row[4],
            "phone": row[5],
            "status": row[6]
        })

    return jsonify(result)

@app.route('/ngo')
def ngo():
    return render_template('ngo.html')

@app.route('/org')
def org():
    return render_template('org.html')

@app.route('/register_ngo', methods=['POST'])
def register_ngo():
    ngoName = request.form['ngoName']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']
    password = request.form['password']

    try:
         cursor.execute(
        "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
        (ngoName, email, password, "NGO")
         )
    
         db.commit()
         flash("NGO Registered Successfully!", "success")
         return redirect('/login')

    except mysql.connector.IntegrityError:
        flash("⚠ Email already registered! Please login.", "error")
        return redirect('/login')
        
        
    

@app.route('/register_org', methods=['POST'])
def register_org():
    orgName = request.form['orgName']
    contactPerson = request.form['contactPerson']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']
    password = request.form['password']

    try:
        cursor.execute(
        "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
        (orgName, email, password, "Organization")
        )
        
    
        db.commit()
        flash("Organization Registered Successfully!", "success")
        return redirect('/login')

    except mysql.connector.IntegrityError:
        flash("⚠ Email already registered! Please login.", "error")
        return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


    
if __name__ == '__main__':
    app.run(debug=True)
