from flask import Flask, request, jsonify, render_template_string
import os

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except:
    HAS_GEMINI = False

app = Flask(__name__)

API_KEY = os.getenv("GEMINI_API_KEY", "")
model = None
if HAS_GEMINI and API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

HTML = """<!DOCTYPE html><html><head><title>Cyusa AI</title><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{font-family:Arial;background:#0f172a;color:white;margin:0;display:flex;flex-direction:column;height:100vh}.header{background:#1e293b;padding:15px;text-align:center;font-size:20px;font-weight:bold;color:#38bdf8}.chat{flex:1;overflow-y:auto;padding:15px}.msg{margin:10px 0;padding:12px;border-radius:10px;max-width:85%}.user{background:#2563eb;margin-left:auto}.bot{background:#334155}.input-area{display:flex;padding:15px;background:#1e293b}input{flex:1;padding:12px;border-radius:20px;border:none;outline:none}button{margin-left:10px;padding:12px 20px;border-radius:20px;border:none;background:#38bdf8;color:black;font-weight:bold}</style></head><body><div class='header'>CYUSA AI - Uganda's AI<br><small style='font-size:12px;color:#94a3b8'>WhatsApp +256781164358</small></div><div id='chat' class='chat'><div class='msg bot'>Hello! I'm Cyusa AI built by Goodluck! Ask me anything!</div></div><div class='input-area'><input id='q' placeholder='Ask me anything...' onkeypress="if(event.key==='Enter')send()"><button onclick='send()'>Send</button></div><script>async function send(){let i=document.getElementById('q');let t=i.value.trim();if(!t)return;let c=document.getElementById('chat');c.innerHTML+=`<div class='msg user'>${t}</div>`;i.value='';c.scrollTop=c.scrollHeight;let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:t})});let d=await r.json();c.innerHTML+=`<div class='msg bot'>${d.reply}</div>`;c.scrollTop=c.scrollHeight;}</script></body></html>"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message","")
        if not model:
            return jsonify({"reply": f"You said: {user_msg} <br><br> I am online! Add GEMINI_API_KEY to make me smarter!"})
        response = model.generate_content(f"You are Cyusa AI by Goodluck Cyusa from Uganda. Be helpful. User: {user_msg}")
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
