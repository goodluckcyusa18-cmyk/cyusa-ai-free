from flask import Flask, request, jsonify
import os
from groq import Groq

app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

HTML = """<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>CYUSA AI</title><style>body{margin:0;background:#0f172a;color:white;font-family:sans-serif}.header{background:#1e293b;padding:15px;text-align:center;border-bottom:2px solid #3b82f6}.header h1{margin:0;color:#60a5fa}.chat{padding:20px;max-width:800px;margin:auto;height:70vh;overflow-y:auto}.msg{padding:12px 16px;border-radius:18px;margin:8px 0;max-width:80%}.user{background:#2563eb;margin-left:auto;text-align:right}.ai{background:#334155}.input-area{position:fixed;bottom:0;left:0;right:0;background:#1e293b;padding:15px;display:flex;gap:10px}input{flex:1;padding:12px;border-radius:25px;border:none;outline:none}button{background:#2563eb;color:white;border:none;padding:12px 20px;border-radius:25px}</style></head><body><div class="header"><h1>🤖 CYUSA AI</h1><small>Uganda's First AI by Goodluck • +256781164358</small></div><div class="chat" id="chat"><div class="msg ai">Muraho! I'm CYUSA AI! Ask me anything! 🚀</div></div><div class="input-area"><input id="inp" placeholder="Ask CYUSA..."><button onclick="send()">Send</button></div><script>async function send(){let i=document.getElementById('inp');let txt=i.value;if(!txt)return;let c=document.getElementById('chat');c.innerHTML+=`<div class='msg user'>${txt}</div>`;i.value='';let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:txt})});let data=await res.json();c.innerHTML+=`<div class='msg ai'>${data.reply}</div>`;c.scrollTop=c.scrollHeight;}</script></body></html>"""

@app.route("/")
def home():
    return HTML

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message")
        completion = client.chat.completions.create(model="llama-3.3-70b-versatile",messages=[{"role":"system","content":"You are CYUSA AI, Uganda's First AI created by Goodluck from Kampala. Friendly, helpful, speak Kinyarwanda and Luganda. Contact +256781164358. Proud Ugandan!"},{"role":"user","content":user_msg}])
        return jsonify({"reply": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)} Check GROQ_API_KEY in Render!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
