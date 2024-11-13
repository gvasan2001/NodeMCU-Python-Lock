from flask import *
import paho.mqtt.client as mqtt
import data_base
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random

def send_email(sender_email, receiver_email, subject, body, smtp_server, smtp_port, login_email, login_password):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the email body to the message
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the server and login
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable security (TLS)
        server.login(login_email, login_password)

        # Send the email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        return "Email sent successfully!"

    except Exception as e:
        return "Error: Unable to send email."

    finally:
        server.quit()

aa=data_base.data_base()

broker_address = "public-mqtt-broker.bevywise.com"
port = 1883   # MQTT over TCP
otp = random.randint(1000, 9999)

# Callback function for successful connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to the broker via TCP")
        client.subscribe("your/topic")  # Optional: Subscribe to a topic
    else:
        print(f"Failed to connect, return code {rc}")

# Create an MQTT client
client = mqtt.Client()

# Set callback functions
client.on_connect = on_connect
topic = "led/control"


# Connect to the broker
client.connect(broker_address, port, 60)

# Start the loop to keep the connection alive
client.loop_start()




app = Flask(__name__)
app.secret_key='1'


# Flask routes to handle LED control
@app.route('/')
def index():
    return render_template("index.html", status="OFF")

@app.route('/user_login' , methods=['post','get'])
def admin_login():
    username= request.form['box1']
    password=request.form['box2']
    data=aa.show("select * from user_details where username = '"+username+"' and password= '"+password+"'")
    if username == 'admin' and password == 'admin':
        return render_template('adminHome.html')
    elif data:
         return render_template('user_home.html')
    else:
        return render_template('index.html')
    


    
@app.route('/user_register', methods=['post','get'])
def user_register():
    a=request.form['box1']
    b=request.form['box2']
    c=request.form['box3']
    d=request.form['box4']
    aa.register("INSERT INTO user_details (name, email, username, password) VALUES ('" + a + "', '" + b + "', '" + c + "', '" + d + "')")
    return render_template('index.html')


@app.route('/otp_generate',methods=['post'])
def otp_generate():
    email= request.form['box1']
    randomNumber = random.randint(1000,9999)
    session['key']= randomNumber
    client.publish(topic, randomNumber)
    final=send_email(
    sender_email="gokulavasan640@gmail.com",
    receiver_email=email,
    subject="Lock passworld",
    body="This is your OTP" + " "+ str(randomNumber),
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    login_email="gokulavasan640@gmail.com",
    login_password="xvao kbab zjqi ffzh"  # Use an app-specific password or environment variable for better security
)
    
    return render_template("adminHome.html",data=final)



@app.route('/led/on', methods=['POST'])
def led_on():
    s=request.form['box1']
    a=session['key']
    if str(s)==str(a):
        client.publish(topic, "on")
        return render_template("user_home.html", status="ON")
    else:
        return render_template("user_home.html", status="key is not match")

@app.route('/led')
def led_off():
    client.publish(topic, "off")
    return render_template("user_home.html", status="OFF")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)