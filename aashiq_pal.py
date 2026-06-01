# aashiq_pal.py - Complete AutoMsg System (2 files total)
import os
import threading
import time
from flask import Flask, request, render_template_string, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

app = Flask(__name__)
app.secret_key = 'aashiqpal_secret_2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------- Database Model ----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    unique_key = db.Column(db.String(100), default='')

    def set_password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin')
        admin.set_password('admin123')
        admin.unique_key = 'AASHIQPAL@2025'
        db.session.add(admin)
        db.session.commit()

# ---------- Automation ----------
def auto_send(phone, file_path, delay, hater_name):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get('https://web.whatsapp.com')
        input("✅ Scan QR code in opened window, then press Enter here...")

        with open(file_path, 'r', encoding='utf-8') as f:
            msgs = [line.strip() for line in f if line.strip()]
        if not msgs:
            return
        driver.get(f'https://web.whatsapp.com/send?phone={phone}')
        wait = WebDriverWait(driver, 30)
        box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')))
        for msg in msgs:
            full = f"👿 {hater_name}: {msg}"
            box.send_keys(full + Keys.ENTER)
            time.sleep(delay)
        driver.quit()
    except Exception as e:
        print("Error:", e)

# ---------- HTML Templates (embedded) ----------
home_html = '''
<!DOCTYPE html>
<html>
<head><title>Aashiq Pal AutoMsg Pro</title><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:linear-gradient(135deg,#0a0f1f,#000);font-family:Segoe UI,sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center}.card{background:rgba(0,0,0,0.7);backdrop-filter:blur(12px);border:1px solid cyan;border-radius:30px;padding:40px;width:400px;text-align:center;color:white;box-shadow:0 0 20px cyan}h1{color:cyan;margin-bottom:20px}.btn{display:inline-block;background:cyan;color:black;padding:10px 25px;margin:10px;border-radius:40px;text-decoration:none;font-weight:bold}.contact{margin-top:20px;font-size:14px}
</style></head>
<body>
<div class="card">
<h1>🚀 Aashiq Pal AutoMsg Pro</h1>
<p>Advance AutoMessaging | Unique Key Access</p>
<a href="/signup" class="btn">SIGN UP</a>
<a href="/login" class="btn">LOG IN</a>
<div class="contact">📞 CONTACT VIA WHATSAPP: +919876543210</div>
</div>
</body>
</html>
'''

form_html = '''
<!DOCTYPE html>
<html>
<head><title>{{title}}</title><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:linear-gradient(135deg,#0a0f1f,#000);font-family:Segoe UI,sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center}.card{background:rgba(0,0,0,0.7);backdrop-filter:blur(12px);border:1px solid cyan;border-radius:30px;padding:40px;width:400px;text-align:center;color:white;box-shadow:0 0 20px cyan}input{width:100%;padding:12px;margin:10px 0;background:#1a1a2e;border:1px solid cyan;border-radius:40px;color:white}button{background:cyan;color:black;padding:10px 25px;border-radius:40px;border:none;font-weight:bold;cursor:pointer}a{color:cyan}.flash{background:#ffaa00;color:black;padding:10px;border-radius:20px;margin-top:15px}
</style></head>
<body>
<div class="card">
<h2>{{title}}</h2>
<form method="post">
{% if title == "SIGN UP" %}
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
{% else %}
<input type="text" name="username" placeholder="Username" required>
<input type="password" name="password" placeholder="Password" required>
{% endif %}
<button type="submit">{{button}}</button>
</form>
<a href="{{link_url}}">{{link_text}}</a>
{% with messages = get_flashed_messages() %}
  {% if messages %}<div class="flash">{{messages[0]}}</div>{% endif %}
{% endwith %}
</div>
</body>
</html>
'''

key_html = '''
<!DOCTYPE html>
<html>
<head><title>Unique Key - Aashiq Pal</title><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:linear-gradient(135deg,#0a0f1f,#000);font-family:Segoe UI,sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center}.card{background:rgba(0,0,0,0.7);backdrop-filter:blur(12px);border:1px solid cyan;border-radius:30px;padding:40px;width:400px;text-align:center;color:white;box-shadow:0 0 20px cyan}input{width:100%;padding:12px;margin:10px 0;background:#1a1a2e;border:1px solid cyan;border-radius:40px;color:white}button{background:cyan;color:black;padding:10px 25px;border-radius:40px;border:none;font-weight:bold;cursor:pointer}.flash{background:#ffaa00;color:black;padding:10px;border-radius:20px;margin-top:15px}
</style></head>
<body>
<div class="card">
<h2>🔑 ENTER UNIQUE KEY</h2>
<p style="color:cyan;">Contact admin to get your key</p>
<form method="post">
<input type="text" name="unique_key" placeholder="Unique Key" required>
<button type="submit">ACCESS SYSTEM</button>
</form>
{% with messages = get_flashed_messages() %}
  {% if messages %}<div class="flash">{{messages[0]}}</div>{% endif %}
{% endwith %}
</div>
</body>
</html>
'''

dashboard_html = '''
<!DOCTYPE html>
<html>
<head><title>Dashboard - Aashiq Pal</title><style>
*{margin:0;padding:0;box-sizing:border-box}body{background:linear-gradient(135deg,#0a0f1f,#000);font-family:Segoe UI,sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center}.card{background:rgba(0,0,0,0.7);backdrop-filter:blur(12px);border:1px solid cyan;border-radius:30px;padding:40px;width:600px;max-width:90%;text-align:center;color:white;box-shadow:0 0 20px cyan}input,select{width:100%;padding:12px;margin:10px 0;background:#1a1a2e;border:1px solid cyan;border-radius:40px;color:white}button{background:cyan;color:black;padding:10px 25px;border-radius:40px;border:none;font-weight:bold;cursor:pointer;margin-top:10px}.flash{background:#ffaa00;color:black;padding:10px;border-radius:20px;margin-top:15px}.note{font-size:12px;margin-top:20px;color:#aaa}a{color:cyan}
</style></head>
<body>
<div class="card">
<h1>📨 Aashiq Pal AutoMsg Panel</h1>
<p>Welcome, {{username}} | <a href="/logout">Logout</a></p>
<form method="post" enctype="multipart/form-data">
<label>📁 Choose TXT File</label>
<input type="file" name="txt_file" accept=".txt" required>
<label>⏱️ Delay (Seconds)</label>
<input type="number" name="delay" value="20" required>
<label>👤 Hater Name</label>
<input type="text" name="hater_name" placeholder="Enter Name" required>
<label>📞 WhatsApp Number (with country code)</label>
<input type="text" name="phone" placeholder="+919876543210" required>
<button type="submit">🚀 START AUTO MESSAGE</button>
</form>
{% with messages = get_flashed_messages() %}
  {% if messages %}<div class="flash">{{messages[0]}}</div>{% endif %}
{% endwith %}
<div class="note">⚡ After clicking START, you will need to scan WhatsApp Web QR code (once). Then messages will be sent automatically.</div>
</div>
</body>
</html>
'''

# ---------- Routes ----------
@app.route('/')
def home():
    return render_template_string(home_html)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists!')
            return redirect(url_for('signup'))
        user = User(username=username)
        user.set_password(password)
        user.unique_key = ''
        db.session.add(user)
        db.session.commit()
        flash('Signup successful! Please login.')
        return redirect(url_for('login'))
    return render_template_string(form_html, title="SIGN UP", button="CREATE ACCOUNT", link_url="/login", link_text="Already have account? Login")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('key_page'))
        flash('Invalid credentials')
    return render_template_string(form_html, title="LOGIN", button="LOGIN", link_url="/signup", link_text="New user? Signup")

@app.route('/key', methods=['GET','POST'])
def key_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        entered = request.form['unique_key']
        if entered == 'AASHIQPAL@2025' or entered == user.unique_key:
            user.unique_key = entered
            db.session.commit()
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid Unique Key. Access denied.')
    return render_template_string(key_html)

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if not user.unique_key:
        flash('Please enter your unique key first')
        return redirect(url_for('key_page'))
    if request.method == 'POST':
        phone = request.form['phone']
        delay = int(request.form['delay'])
        hater = request.form['hater_name']
        file = request.files['txt_file']
        if file and file.filename.endswith('.txt'):
            os.makedirs('uploads', exist_ok=True)
            path = f"uploads/{user.id}_{file.filename}"
            file.save(path)
            thread = threading.Thread(target=auto_send, args=(phone, path, delay, hater))
            thread.start()
            flash('Automation started! Check WhatsApp Web window.')
        else:
            flash('Please upload a .txt file')
    return render_template_string(dashboard_html, username=user.username)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)