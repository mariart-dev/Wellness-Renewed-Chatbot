from flask import Flask, request, render_template, jsonify
from nltk.chat.util import Chat, reflections
import re

app = Flask(__name__, template_folder="")

pairs = [
    [
        r".*services.*",
        ["We offer a variety of massages, including Swedish massages, deep tissue massages, hot stone massages, aromatherapy, Thai massage, shiatsu, reflexology, and more."]
    ],
    [
        r".*(hour|hours|schedule).*",
        ["We are open from Monday to Friday from 9:00 AM to 6:00 PM."]
    ],
    [
        r".*(appointment|book|reservation|schedule|date|reserve).*",
        ["You can schedule an appointment by calling us at (123) 456-7890 or by completing our online form."]
    ],
    [
        r".*(location|find|city|country|place).*",
        ["We are located in Dublin, Ireland."]
    ],
    [
        r".*(payment|money|payment methods).*",
        ["We accept various payment methods, including cash, credit card, debit card, bank transfer (we work with local banks like Bank A, Bank B, Bank C), and online payment through our secure platform."]
    ],
    [
        r".*(products|oils|supplies).*",
        ["We use a wide variety of high-quality supplies in our massages, including:\n\n- Premium natural oils\n- Therapeutic lotions\n- Relaxing aromas\n- Hot compresses\n- Moisturizing creams\n- Aromatic candles\n\nThese supplies are designed to provide you with an exceptional and relaxing massage experience."]
    ],
    [
        r".*(types of massages|massages).*",
        ["We offer a wide range of massages, including:\n\n1. Swedish Massages\n2. Deep Tissue Massages\n3. Hot Stone Massages\n4. Aromatherapy\n5. Therapeutic Massages\n6. Relaxation Massages\n7. Sports Massages\n8. Reflexology\n\nDo you have any specific preferences or would you like to know more about any of these massages?"]
    ],
    [
        r".*(duration|time).*",
        ["The typical duration of our massages is 60 minutes, but we also offer 30-minute and 90-minute sessions to suit your needs."]
    ],
    [
        r".*(prices|cost|rate|price|pricing).*",
        ["Our prices vary depending on the type of massage and duration. Here are some examples in euros:\n\n"
         " - Swedish Massage: €50 for 60 minutes\n"
         " - Deep Tissue Massage: €60 for 60 minutes\n"
         " - Hot Stone Massage: €65 for 75 minutes\n"
         " - Relaxation Aromatherapy: €55 for 60 minutes\n\n"
         "Please visit our online price page for detailed information."]
    ]
]


chatbot = Chat(pairs, reflections)


massage_types = {
    "swedish": "Swedish massages are known for their gentle and relaxing strokes.",
    "relaxation": "Swedish massages are known for their gentle and relaxing strokes.",
    "gentle": "Swedish massages are known for their gentle and relaxing strokes.",
    "relaxing": "Swedish massages are known for their gentle and relaxing strokes.",
    "relax": "Swedish massages are known for their gentle and relaxing strokes.",

    "deep tissue": "Deep tissue massages focus on deeper layers of muscle tissue to relieve tension.",
    "tension": "Deep tissue massages focus on deeper layers of muscle tissue to relieve tension.",

    "hot stone": "Hot stone massages use heated stones to relax the muscles.",
    "stones": "Hot stone massages use heated stones to relax the muscles.",

    "aromatherapy": "Aromatherapy uses essential oils to promote relaxation and well-being.",
    "fragrance": "Aromatherapy uses essential oils to promote relaxation and well-being.",
    "scent": "Aromatherapy uses essential oils to promote relaxation and well-being.",

    "therapeutic": "Therapeutic massages focus on specific muscle issues or injuries.",
    "injuries": "Therapeutic massages focus on specific muscle issues or injuries.",
    "muscle issues": "Therapeutic massages focus on specific muscle issues or injuries.",

    "sports": "Sports massages are designed for athletes and focus on muscle recovery and performance.",
    "athletes": "Sports massages are designed for athletes and focus on muscle recovery and performance.",
    "recovery": "Sports massages are designed for athletes and focus on muscle recovery and performance.",
    "performance": "Sports massages are designed for athletes and focus on muscle recovery and performance.",
    "muscles": "Sports massages are designed for athletes and focus on muscle recovery and performance.",
    "bodybuilding": "Sports massages are designed for athletes and focus on muscle recovery and performance.",

    "reflexology": "Reflexology is based on stimulating points on the feet to promote relaxation and well-being.",
    "stimulation": "Reflexology is based on stimulating points on the feet to promote relaxation and well-being.",
    "feet": "Reflexology is based on stimulating points on the feet to promote relaxation and well-being.",
}


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/get")
def get_bot_response():
    user_message = request.args.get("user_message")
    print("User message:", user_message)
    
    for massage, description in massage_types.items():
        if massage in user_message.lower():
            bot_response = [f"{description}"]
            return jsonify({"bot_response": bot_response})

    
    for pattern, response in pairs:
        if re.match(pattern, user_message, re.IGNORECASE):
            bot_response = response
            return jsonify({"bot_response": bot_response})

    
    default_response = ["I'm sorry, I can't answer that question right now. Can I assist you with something else?"]
    return jsonify({"bot_response": default_response})


if __name__ == "__main__":
    app.run(debug=True)
