from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Cyusa AI is ONLINE! WhatsApp +256781164358 Ready!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
