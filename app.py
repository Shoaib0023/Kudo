import os

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    render_template,
    redirect,
    request,
    url_for,
)

from twilio.rest import Client


load_dotenv()
app = Flask(__name__)
app.secret_key = "ssssh don't tell anyone"

TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Returns a collection of messages that were sent from the number
def get_sent_messages():
    messages = []
    messages = client.messages.list(from_=TWILIO_PHONE_NUMBER)
    return messages

# Send the text message
def send_message(to, body):
    message = client.messages.create(
            to=to,
            from_=TWILIO_PHONE_NUMBER,
            body=body
    )

    return

@app.route("/", methods=["GET"])
def index():
    messages = get_sent_messages()
    return render_template("home.html", messages=messages)


@app.route("/add-compliment", methods=["POST"])
def add_compliment():
    try:
        sender = request.values.get('sender')
        receiver = request.values.get('receiver')
        compliment = request.values.get('compliment')
        to = request.values.get('to')
        sender = 'Someone' if len(sender) == 0 else sender
        receiver = "Someone" if len(receiver) == 0 else receiver
        compliment = 'an amazing Person' if len(compliment) == 0 else compliment
        body = f'{sender} says: {receiver} is {compliment}. See more compliments at {request.url_root}'
        send_message(to, body)
        flash('Your message was successfully sent')

    except:
        flash('Please fill the Receiver number')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
