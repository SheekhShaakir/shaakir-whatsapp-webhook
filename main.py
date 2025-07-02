from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Xogta lacagaha
payments = {
    '0.24': '*712*617313335*0.24#',
    '0.44': '*712*617313335*0.44#',
    '0.85': '*712*617313335*0.85#',
    '1.75': '*712*617313335*1.75#',
    '3.55': '*712*617313335*3.55#',
    '4.45': '*712*617313335*4.45#',
    '8.95': '*712*617313335*8.95#',
}

packages = {
    '1': {
        'name': 'Anfac Plus',
        'details': [
            "1. $0.24 → 400MB + 10min (10 days)",
            "2. $0.44 → 850MB + 30min (14 days)",
            "3. $0.85 → 2GB + 80min (14 days)",
            "4. $1.75 → 5GB + 160min (30 days)",
            "5. $3.55 → 10GB + 320min + 200SMS (30 days)",
            "6. $4.45 → 12GB + 400min + 150SMS (30 days)",
            "7. $8.95 → 28GB + 800min + 300SMS (45 days)",
        ],
    }
}

# Kaydinta xogta dadka
users_paid = set()
user_selected_amount = {}

@app.route("/sms", methods=['POST'])
def sms_reply():
    from_number = request.form.get('From')
    text = request.form.get('Body', '').strip().lower()

    resp = MessagingResponse()
    msg = resp.message()

    if from_number not in users_paid:
        if text in payments:
            user_selected_amount[from_number] = text
            pkg = packages.get('1')
            details_text = "\n".join(pkg['details'])
            code = payments[text]
            msg.body(
                f"✅ Waxaad dooratay ${text}.\n\n"
                f"📦 {pkg['name']} Packages:\n{details_text}\n\n"
                f"💵 Si aad lacagta u bixiso, isticmaaal code-kan:\n{code}\n\n"
                "Kadib markaad lacag bixiso, dir 'Done'"
            )
        elif text in ['done', 'ok', 'ready']:
            users_paid.add(from_number)
            msg.body(
                "✅ Lacagta waa la xaqiijiyay. Waxaad hadda isticmaali kartaa adeegyada:\n\n"
                "1️⃣ Anfac Plus\n\n"
                "Fadlan qor lambarka adeegga aad rabto (tusaale: 1)"
            )
        else:
            msg.body(
                "💰 Fadlan dooro mid ka mid ah lacagaha:\n" +
                "\n".join([f"- ${k}" for k in payments.keys()]) +
                "\nAma dir 'Done' haddii aad lacag bixisay."
            )
        return str(resp)

    # User horay lacag ayuu u bixiyay
    if text == '1':
        pkg = packages.get('1')
        details_text = "\n".join(pkg['details'])
        msg.body(f"📦 {pkg['name']} Packages:\n{details_text}")
    else:
        msg.body("Fadlan qor 1 si aad u doorato Anfac Plus, ama dir /start si aad u bilowdo.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
