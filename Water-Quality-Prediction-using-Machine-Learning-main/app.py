from flask import Flask, render_template, request
from flask import Flask, render_template, request
import joblib
import numpy as np
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import joblib
import numpy as np

# Initialize Flask App
app = Flask(__name__, static_folder='static', template_folder='templates')

# Load trained model
model = joblib.load('water_model.pkl')


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
        # Read all input values from form
        data = [float(x) for x in request.form.values()]
        final_input = np.array([data])

        # Make prediction
        prediction = model.predict(final_input)

        # Static confidence score (for display)
        probability = 80.0

        # Result message
        if prediction[0] == 1:
            result = "✅ Water is Drinkable"
            color = "green"
        else:
            result = "🚫 Water is Not Drinkable"
            color = "red"

        # WHO Safe Limits
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

        return render_template(
            'result.html',
            prediction_text=result,
            color=color,
            score=round(probability, 2),
            limits=safe_limits
        )

    except Exception as e:
        return render_template(
            'result.html',
            prediction_text=f"⚠️ Error Occurred: {str(e)}",
            color="red",
            score=0,
            limits={}
        )


# About Page
@app.route('/about')
def about():
    return render_template('about.html')


# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')
# Contact Form Submission Route
# Contact Form Submission Route (Full setup with CSV + Gmail)
@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # 1️⃣ Save message to CSV file
        with open('contact_messages.csv', mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([name, email, message])
        

        # 2️⃣ Send email notification to Sonal
        sender_email = "sonalpaswan011@gmail.com"  # temporary project email
        receiver_email = "sonalpaswan011@gmail.com"
        password = "dezq vbmf bxjj wxcn"
        

        subject = f"New Contact Message from {name}"
        body = f"""
        You have received a new message from your Water Quality Prediction Project.

        👤 Name: {name}
        📧 Email: {email}
        💬 Message: {message}
        """

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Gmail SMTP setup
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())

        return render_template('contact.html', success_message="✅ Message sent successfully and saved to record!")

    except Exception as e:
        return render_template('contact.html', error_message=f"⚠️ Error occurred: {str(e)}")
    # Admin Dashboard to view messages
@app.route('/messages')
def view_messages():
    messages = []
    try:
        with open('contact_messages.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    messages.append({'name': row[0], 'email': row[1], 'message': row[2]})
    except FileNotFoundError:
        pass
    return render_template('messages.html', messages=messages)



# Run App
if __name__ == "__main__":
    app.run(debug=True)
