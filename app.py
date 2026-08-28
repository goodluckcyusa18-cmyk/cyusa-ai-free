from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{margin:0;background:#0f172a;color:white;font-family:Arial}
.header{background:#1e293b;padding:15px;text-align:center}
.chat{padding:15px;height:70vh;overflow-y:auto}
.msg{padding:10px;margin:8px;border-radius:10px;max-width:80%}
.ai{background:#334155}.user{background:#2563eb;margin-left:auto}
.bar{position:fixed;bottom:0;left:0;right:0;background:#1e293b;padding:10px;display:flex;gap:10px}
input{flex:1;padding:12px;border-radius:20px;border:none}
button{padding:12px 20px;border-radius:20px;border:none;background:#2563eb;color:white;font-weight:bold}
</style>
</head>
<body>
<div class="header"><h2>CYUSA AI Uganda</h2></div>
<div class="chat" id="chat"><div class="msg ai">Muraho! I am CYUSA AI - Ugandas First AI by Goodluck!</div></div>
<div class="bar"><input id="inp" placeholder="Ask CYUSA..."><button onclick="send()">Send</button></div>
<script>
async function send(){
let i=document.getElementById('inp');
let c=document.getElementById('chat');
let m=i.value;
if(!m)return;
c.innerHTML+=`<div class=msg user>${m}</div>`;
i.value='';
let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})});
let d=await r.json();
c.innerHTML+=`<div class=msg ai>${d.reply}</div>`;
c.scrollTop=c.scrollHeight
}
document.getElementById('inp').addEventListener('keypress',function(e){if(e.key==='Enter')send()})
</script>
</body>
</html>
"""

@app.route("/chat", methods=["POST"])
def chat():
    try:
        from groq import Groq
        api_key = os.environ.get("GROQ_API_KEY")
        client = Groq(api_key=api_key)
        msg = request.json.get("message","")
        comp = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role":"system","content":"You are CYUSA AI, Ugandas First AI by Goodluck."},
                {"role":"user","content":msg}
            ],
            max_tokens=500
        )
        return jsonify({"reply": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
