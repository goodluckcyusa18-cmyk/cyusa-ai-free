from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return '''
<!DOCTYPE html>
<html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{margin:0;background:#0f172a;color:white;font-family:Arial}
.header{background:#1e293b;padding:15px;text-align:center;font-weight:bold}
.chat{padding:15px;height:70vh;overflow-y:auto}
.msg{padding:10px;margin:8px;border-radius:10px;max-width:80%}
.ai{background:#334155} .user{background:#2563eb;margin-left:auto}
.bar{position:fixed;bottom:0;left:0;right:0;background:#1e293b;padding:10px;display:flex;gap:10px}
input{flex:1;padding:12px;border-radius:20px;border:none}
button{padding:12px 20px;border-radius:20px;border:none;background:#2563eb;color:white;font-weight:bold}
</style></head><body><div class="header"><h2 style="margin:0">CYUSA AI 🇺🇬</h2></div>
<div class="chat" id="chat"><div class="msg ai">Muraho! I'm CYUSA AI - Uganda's First AI by Goodluck! How can I help?</div></div>
<div class="bar"><input id="inp" placeholder="Ask CYUSA..."><button onclick="send()">Send</button></div>
<script>async function send(){let i=document.getElementById('inp');let c=document.getElementById('chat');
let m=i.value;if(!m)return;c.innerHTML+=`<div class="msg user">${m}</div>`;i.value='';
let r=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})});
let d=await r.json();c.innerHTML+=`<div class="msg ai">${d.reply}</div>`;c.scrollTop=c.scrollHeight}
document
