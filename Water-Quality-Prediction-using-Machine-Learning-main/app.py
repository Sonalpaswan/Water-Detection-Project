from flask import Flask, render_template, request
import joblib
import numpy as np
import csv
import os

# Initialize Flask App
app = Flask(__name__, static_folder='static', template_folder='templates')

# ✅ Safe Model Loading (IMPORTANT for Render)
model = None
model_path = os.path.join(os.path.dirname(__file__), "water_model.pkl")

if os.path.exists(model_path):
    model = joblib.load(model_path)
    print("✅ Model loaded successfully")
else:
    print("❌ Model file not found")

# Home Page
@app.route('/')
def home():
    return render_template('index.html')

# Predict Page
@app.route('/predict_page')
def predict_page():
    return render_template('predict.html')

# Prediction Logic
@app.route('/predict', methods=['POST'])
def predict():
    try:
        if model is None:
            return render_template('result.html',
                                   prediction_text="❌ Model not loaded",
                                   color="red",
                                   score=0,
                                   limits={})

        data = [float(x) for x in request.form.values()]
        final_input = np.array([data])

        prediction = model.predict(final_input)
        probability = 80.0

        if prediction[0] == 1:
            result = "✅ Water is Drinkable"
            color = "green"
        else:
            result = "🚫 Water is Not Drinkable"
            color = "red"

        safe_limits = {
            "pH": "6.5–8.5",
            "Hardness": "0–300 mg/L",
            "Solids": "0–500 mg/L",
            "Chloramines": "0–4 mg/L",
            "Sulfate": "0–250 mg/L",
            "Conductivity": "0–800 μS/cm",
            "Organic Carbon": "0–5 mg/L",
            "Trihalomethanes": "0–100 µg/L",
            "Turbidity": "0–5 NTU"
        }

        return render_template('result.html',
                               prediction_text=result,
                               color=color,
                               score=round(probability, 2),
                               limits=safe_limits)

    except Exception as e:
        return render_template('result.html',
                               prediction_text=f"⚠️ Error Occurred: {str(e)}",
                               color="red",
                               score=0,
                               limits={})

# About Page
@app.route('/about')
def about():
    return render_template('about.html')

# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Send Message
@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        with open('contact_messages.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, email, message])

        return render_template('contact.html', success_message="✅ Message saved!")

    except Exception as e:
        return render_template('contact.html', error_message=str(e))

# View Messages
@app.route('/messages')
def view_messages():
    messages = []
    try:
        with open('contact_messages.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    messages.append({
                        'name': row[0],
                        'email': row[1],
                        'message': row[2]
                    })
    except FileNotFoundError:
        pass

    return render_template('messages.html', messages=messages)

# ✅ Run for Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)