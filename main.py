from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return "Shaakir Data Reseller Service - Twilio Webhook Ready!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    # Get incoming message details from Twilio webhook
    incoming_msg = request.form.get('Body', '').strip()
    sender = request.form.get('From', '')
    
    print(f"📩 Fariin WhatsApp ka timid {sender}: {incoming_msg}")
    
    # Create TwiML response
    resp = MessagingResponse()
    msg = resp.message()
    
    # Process the message and respond accordingly
    if not incoming_msg:
        msg.body("🛑 Fadlan qor fariin.")
    elif 'hormuud' in incoming_msg.lower():
        msg.body("✅ Waxaad dooratay Hormuud Telecom.\n\n📱 Fadlan geli:\n- Lambarka telefoonka\n- Qadarka data (1GB, 2GB, 5GB, iwm)\n\nTusaale: 252613123456 2GB")
    elif 'somtel' in incoming_msg.lower():
        msg.body("✅ Waxaad dooratay Somtel.\n\n📱 Fadlan geli:\n- Lambarka telefoonka\n- Qadarka data (1GB, 2GB, 5GB, iwm)\n\nTusaale: 252615123456 1GB")
    elif 'somnet' in incoming_msg.lower():
        msg.body("✅ Waxaad dooratay Somnet.\n\n📱 Fadlan geli:\n- Lambarka telefoonka\n- Qadarka data (1GB, 2GB, 5GB, iwm)\n\nTusaale: 252617123456 5GB")
    elif 'help' in incoming_msg.lower() or 'caawimo' in incoming_msg.lower():
        msg.body("🆘 *Shaakir Data Reseller*\n\nDooro mid ka mid ah:\n• Hormuud\n• Somtel\n• Somnet\n\nAma qor 'caawimo' wixii su'aal ah.")
    else:
        # Check if it might be a phone number and data amount
        words = incoming_msg.split()
        if len(words) >= 2 and any(word.startswith('252') for word in words):
            msg.body("📋 Waan helay codsigaaga:\n" + incoming_msg + "\n\n⏳ Waan ka shaqeynayaa... Waxaan kuu soo diri doonaa xaqiijin dhow.")
        else:
            msg.body("🛑 Fariinta lama fahmin.\n\n📋 Dooro:\n• Hormuud\n• Somtel  \n• Somnet\n\nAma qor 'caawimo' caawimada dheeraad ah.")
    
    return str(resp)


port = int(os.environ.get("PORT", 10000))
app.run(host="0.0.0.0", port=port)
