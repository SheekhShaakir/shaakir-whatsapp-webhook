
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re
import os

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms_reply():
    """Jawaab bixinta fariimaha Twilio webhook"""

    # Fariin iyo sender-ka hel
    incoming_msg = request.values.get('Body', '').lower().strip()
    from_number = request.values.get('From', '')

    # TwiML response samee
    resp = MessagingResponse()

    # Jawaabaha kala duwan
    if 'hormuud' in incoming_msg:
        reply = """✅ Waxaad dooratay Hormuud Telecom.

📱 Fadlan geli:
- Lambarka telefoonka
- Qadarka data (1GB, 2GB, 5GB, iwm)

Tusaale: 252613123456 2GB"""

    elif 'somtel' in incoming_msg:
        reply = """✅ Waxaad dooratay Somtel.

📱 Fadlan geli:
- Lambarka telefoonka  
- Qadarka data (1GB, 2GB, 5GB, iwm)

Tusaale: 252615123456 1GB"""

    elif 'somnet' in incoming_msg:
        reply = """✅ Waxaad dooratay Somnet.

📱 Fadlan geli:
- Lambarka telefoonka
- Qadarka data (1GB, 2GB, 5GB, iwm)

Tusaale: 252617123456 3GB"""

    elif 'help' in incoming_msg or 'caawimo' in incoming_msg:
        reply = """🆘 *Shaakir Data Reseller*

Dooro mid ka mid ah:
• Hormuud
• Somtel  
• Somnet

Ama qor 'caawimo' wixii su'aal ah."""

    else:
        # Phone number iyo data pattern baadh
        phone_pattern = r'252[6-7]\d{8}'
        data_pattern = r'\d+GB|\d+gb'

        phone_match = re.search(phone_pattern, incoming_msg)
        data_match = re.search(data_pattern, incoming_msg, re.IGNORECASE)

        if phone_match and data_match:
            phone = phone_match.group()
            data = data_match.group().upper()
            reply = f"""📋 Waan helay codsigaaga:
{phone} {data}

⏳ Waan ka shaqeynayaa... Waxaan kuu soo diri doonaa xaqiijin dhow."""
        else:
            reply = """🆘 *Shaakir Data Reseller*

Dooro mid ka mid ah:
• Hormuud
• Somtel
• Somnet

Ama qor 'caawimo' wixii su'aal ah."""

    resp.message(reply)
    return str(resp)

@app.route('/')
def home():
    return """
    <h1>🌟 Shaakir Data Reseller Webhook</h1>
    <p>✅ Webhook service wuu shaqeynayaa!</p>
    <p>📱 Webhook URL: /sms</p>
    """
@app.route("/status", methods=["POST"])
def message_status():
    message_sid = request.form.get("MessageSid")
    message_status = request.form.get("MessageStatus")
    print(f"📡 Fariin {message_sid} ayaa status-keedu yahay: {message_status}")
    return "OK", 200

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=True)


