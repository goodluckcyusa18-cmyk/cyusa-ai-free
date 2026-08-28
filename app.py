from flask import Flask, request, jsonify
import os
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route("/")
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CYUSA AI</title>
<style>
body{margin:0;background:#0f172a;color:white;font-family:sans-serif}
.header{background:#1e293b;padding:15px;text-align:center;border-bottom:2px solid #3b82f6}
.chat{padding:20px;max-width:800px;margin:auto;height:70vh;overflow-y:auto}
.msg{padding:12px 16px;border-radius:18px;margin:8px 0;max-width:80%}
.user{background:#2563eb;margin-left:auto}
.ai{background:#334155}
.bar{position:fixed;bottom:0;left:0;right:0;background:#1e293b;padding:15px;display:flex;gap:10px}
input{flex:1;padding:12px;border-radius:25px;border:none}
button{background:#2563eb;color:white;border:none;padding:12px 20px;border-radius:25px}
</style>
</head>
<body>
<div class="header"><h1>CYUSA AI</h1><small>Uganda's First AI by Goodluck +256781164358</small></div>
<div class="chat" id="chat"><div class="msg ai">Muraho! I'm CYUSA AI! Ask me anything! 🚀</div></div>
<div class="bar"><input id="inp" placeholder="Ask CYUSA..."><button onclick="send()">Send</button></div>
<script>
async function send(){
let i=document.getElementById('inp');let t=i.value;if(!t)return;
let c=document.getElementById('chat');c.innerHTML+=`<div class='msg user'>${t}</div>`;i.value='';
let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
let d=await r.json();c.innerHTML+=`<div class='msg ai'>${d.reply}</div>`;c.scrollTop=c.scrollHeight;
}
</script>
</body>
</html>
'''

@app.route("/chat", methods=["POST"])
def chat():
    try:
        msg = request.json.get("message")
        comp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role":"system","content":"You are CYUSA AI, Uganda's first AI created by Goodluck from Kampala Uganda. Friendly, proud Ugandan. Contact +256781164358"},
                {"role":"user","content":msg}
            ]
        )
        return jsonify({"reply": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Add GROQ_API_KEY in Render! Error: {e}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
