from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>CYUSA AI IS ONLINE! Ugandas AI by Goodluck +256781164358 WORKING</h1>"

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
