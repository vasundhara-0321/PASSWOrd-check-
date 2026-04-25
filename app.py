from flask import Flask, render_template, request
import re
import math
import random
import string

app = Flask(__name__)

history = []

def generate_password():
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(random.choice(chars) for _ in range(12))

def check_strength(password):
    score = 0

    if len(password) >= 12: score += 25
    elif len(password) >= 8: score += 15

    if re.search(r'[A-Z]', password): score += 10
    if re.search(r'[a-z]', password): score += 10
    if re.search(r'\d', password): score += 15
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): score += 15

    charset = 0
    if re.search(r'[a-z]', password): charset += 26
    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'\d', password): charset += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): charset += 32

    entropy = len(password) * math.log2(charset) if charset else 0

    if score >= 85:
        strength = "ELITE"
    elif score >= 70:
        strength = "EXCELLENT"
    elif score >= 55:
        strength = "STRONG"
    elif score >= 40:
        strength = "MODERATE"
    else:
        strength = "WEAK"

    history.append((password, strength))

    return strength, score, round(entropy, 2)

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    generated = None

    if request.method == 'POST':
        if 'generate' in request.form:
            generated = generate_password()
        else:
            password = request.form['password']
            result = check_strength(password)

    return render_template('index.html', result=result, history=history[-5:], generated=generated)

if __name__ == "__main__":
    app.run(debug=True)
    
