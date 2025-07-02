from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route("/sms", methods=["POST"])
def sms_reply():
    incoming_msg = request.form.get("Body")
    sender = request.form.get("From")

    resp = MessagingResponse()
    msg = resp.message()

    if "hormuud" in incoming_msg.lower():
        msg.body("✅ Waxaad dooratay Hormuud. Geli lambarka iyo qadarka.")
    elif "somtel" in incoming_msg.lower():
        msg.body("✅ Waxaad dooratay Somtel. Geli lambarka iyo qadarka.")
    elif "somnet" in incoming_msg.lower():
        msg.body("✅ Waxaad dooratay Somnet. Geli lambarka iyo qadarka.")
    else:
        msg.body("🛑 Fariinta lama fahmin. Fadlan dooro Hormuud, Somtel ama Somnet.")

    return str(resp)

# Waa in PORT laga helo deegaanka Render
port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
