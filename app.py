from flask import Flask, request, jsonify, render_template_string
import os
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini
API_KEY = os.getenv("GEMINI_API_KEY", "")
if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Cyusa AI - Uganda's AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { font-family: Arial; background: #0f172a; color: white; margin:0; display:flex; flex-direction:column; height:100vh; }
.header { background:#1e293b; padding:15px; text-align:center; font-size:22px; font-weight:bold; color:#38bdf8; }
.chat { flex:1; overflow-y:auto; padding:15px; }
.msg { margin:10px 0; padding:12px; border-radius:10px; max-width:85%; }
.user { background:#2563eb; margin-left:auto; }
.bot { background:#334155; }
.input-area { display:flex; padding:15px; background:#1e293b; }
input { flex:1; padding:12px; border-radius:20px; border:none; outline:none; }
button { margin-left:10px; padding:12px 20px; border-radius:20px; border:none; background:#38bdf8; color:black; font-weight:bold; cursor:pointer; }
</style>
</head>
<body>
<div class="header">🤖 CYUSA AI - Uganda's Smart AI 🇺🇬<br><small style="font-size:12px;color:#94a3b8">WhatsApp: +256781164358</small></div>
<div id="chat" class="chat">
<div class="msg bot">Hello! I'm Cyusa AI, built by Goodluck Cyusa! How can I help you today? 🚀</div>
</div>
<div class="input-area">
<input id="q" placeholder="Ask me anything..." onkeypress="if(event.key==='Enter')send()">
<button onclick="send()">Send</button>
</div>
<script>
async function send(){
 let input=document.getElementById('q');
 let text=input.value.trim();
 if(!text)return;
 let chat=document.getElementById('chat');
 chat.innerHTML+=`<div class='msg user'>${text}</div>`;
 input.value='';
 chat.scrollTop=chat.scrollHeight;
 let res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:text})});
 let data=await res.json();
 chat.innerHTML+=`<div class='msg bot'>${data.reply}</div>`;
 chat.scrollTop=chat.scrollHeight;
}
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_msg = request.json.get("message","")
        if not model:
            return jsonify({"reply": f"You said: {user_msg} <br><br>⚠️ Add GEMINI_API_KEY in Render to make me super smart! I am online though! ✅"})
        response = model.generate_content(f"You are Cyusa AI, created by Goodluck Cyusa from Uganda. Be helpful, friendly, short. User: {user_msg}")
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
