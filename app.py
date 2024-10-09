from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from action_decider import ActionDecider
from scheduler import start_scheduler


app = Flask(__name__)

# הגדרת Webhook לקבלת הודעות


@app.route("/whatsapp", methods=['POST'])
def whatsapp_webhook():
    incoming_message = request.values.get('Body', '').lower()
    phone_number = request.values.get('From', '')


    decider = ActionDecider(incoming_message, phone_number)
    bot_response = decider.decide_action()


    # תשובה למשתמש
    response = MessagingResponse()
    response.message(bot_response)

    return str(response)


if __name__ == "__main__":
    start_scheduler()

    app.run(debug=True, port=11996)
