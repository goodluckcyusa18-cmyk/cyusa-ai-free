from flask import Flask, request, jsonify
import os, google.generativeai as genai

app = Flask(__name__)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "AIzaSyDUMMY"))

MODEL = genai.GenerativeModel("gemini-1.5-flash")

HTML = """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>CYUSA AI - Uganda's AI</title>
<style>
body{margin:0;background:#0f172a;color:white;font-family:Arial;display:flex;flex-direction:column;height:100vh}
header{background:#1e293b;padding:15px;text-align:center;border-bottom:2px solid #38bdf8}
#chat{flex:1;overflow-y:auto;padding:15px}
.msg{margin:10px 0;padding:12px;border-radius:12px;max-width:85%}
.user{background:#2563eb;margin-left:auto}
.ai{background:#1e293b;border:1px solid #334155}
#inputBar{display:flex;padding:10px;background:#1e293b;gap:10px}
input{flex:1;padding:12px;border-radius:20px;border:none;outline:none}
button{padding:12px 20px;border-radius:20px;border:none;background:#38bdf8;font-weight:bold}
</style></head><body>
<header><h2 style="margin:0;color:#38bdf8">🤖 CYUSA AI</h2><small>Uganda's First AI by Goodluck • +256781164358</small></header>
<div id="chat"><div class="msg ai">Muraho! I'm CYUSA AI! Ask me anything! 🚀</div></div>
<div id="inputBar"><input id="inp" placeholder="Ask CYUSA..."><button onclick="send()">Send</button></div>
<script>
async function send(){
 let i=document.getElementById('inp'); let t=i.value.trim(); if(!t) return;
 let c=document.getElementById('chat');
 c.innerHTML+=`<div class="msg user">${t}</div>`; i.value='';
 c.scrollTop=c.scrollHeight;
 let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});
 let d=await r.json();
 c.innerHTML+=`<div class="msg ai">${d.reply}</div>`;
 c.scrollTop=c.scrollHeight;
}
document.getElementById('inp').addEventListener('keypress',e=>{if(e.key==='Enter')send()});
</script></body></html>
"""

@app.route("/")
def home(): return HTML

@app.route("/chat", methods=["POST"])
def chat():
    try:
        msg = request.json.get("message","")
        resp = MODEL.generate_content(f"You are CYUSA AI, Uganda's AI created by Goodluck Cyusa. Helpful, friendly. User: {msg}")
        return jsonify({"reply": resp.text})
    except Exception as e:
        return jsonify({"reply": f"CYUSA AI Error: {str(e)[:200]}. Add GEMINI_API_KEY in Render settings!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
