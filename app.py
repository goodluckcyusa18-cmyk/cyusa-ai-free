from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return '''
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1"><title>CYUSA AI</title>
<style>body{margin:0;background:#0f172a;color:white;font-family:sans-serif}.header{background:#1e293b;padding:15px;text-align:center;border-bottom:2px solid #3b82f6}.chat{padding:20px;max-width:800px;margin:auto;height:78vh;overflow-y:auto;padding-bottom:80px}.msg{padding:12px 16px;border-radius:18px;margin:8px 0;max-width:80%;line-height:1.4}.user{background:#2563eb;margin-left:auto}.ai{background:#334155}.bar{position:fixed;bottom:0;left:0;right:0;background:#1e293b;padding:15px;display:flex;gap:10px}input{flex:1;padding:12px 16px;border-radius:25px;border:none;outline:none}button{background:#2563eb;color:white;border:none;padding:12px 22px;border-radius:25px;font-weight:bold}</style>
</head><body><div class="header"><h2 style="margin:0">CYUSA AI</h2><small>Uganda's First AI by Goodluck +256781164358</small></div>
<div class="chat" id="chat"><div class="msg ai">Muraho! I'm CYUSA AI! Ask me anything! 🚀</div></div>
<div class="bar"><input id="inp" placeholder="Ask CYUSA..." onkeypress="if(event.key==='Enter')send()"><button onclick="send()">Send</button></div>
<script>async function send(){let i=document.getElementById('inp');let t=i.value.trim();if(!t)return;let c=document.getElementById('chat');c.innerHTML+=`<div class='msg user'>${t}</div>`;i.value='';c.scrollTop=c.scrollHeight;try{let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});let d=await r.json();c.innerHTML+=`<div class='msg ai'>${d.reply}</div>`;}catch(e){c.innerHTML+=`<div class='msg ai'>Error: ${e}</div>`}c.scrollTop=c.scrollHeight;}</script></body></html>
'''

@app.route("/chat", methods=["POST"])
def chat():
    try:
        from groq import Groq
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            return jsonify({"reply":"❌ GROQ_API_KEY not found in Render! Go to Render Dashboard > Environment > Add GROQ_API_KEY = gsk_..."})
        client = Groq(api_key=api_key)
        msg = request.json.get("message","")
        # Use the most stable free model
        comp = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role":"system","content":"You are CYUSA AI, Uganda's First AI created by Goodluck from Kampala, Uganda. You are friendly, helpful, speak some Luganda and Kinyarwanda, and you are proud to be Ugandan. Phone: +256781164358"},
                {"role":"user","content":msg}
            ],
            max_tokens=500
        )
        return jsonify({"reply": comp.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": f"⚠️ CYUSA Error: {str(e)}. If key error, check Render Environment GROQ_API_KEY is correct gsk_..." })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
