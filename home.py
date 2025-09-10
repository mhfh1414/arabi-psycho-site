# -*- coding: utf-8 -*-
from flask import Blueprint, render_template_string

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home_page():
    return render_template_string("""
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="utf-8">
        <title>عربي سايكو</title>
        <style>
            body { font-family: Tahoma; background:#f0f4f8; text-align:center; }
            h1 { color:#2c3e50; }
            .btn { 
                display:block; width:250px; margin:15px auto; padding:12px; 
                background:#3498db; color:white; text-decoration:none; 
                border-radius:8px; font-size:18px;
            }
            .btn:hover { background:#2980b9; }
        </style>
    </head>
    <body>
        <h1>مرحباً بك في موقع عربي سايكو</h1>
        <a class="btn" href="/dsm">📋 التشخيص + دراسة حالة (DSM)</a>
        <a class="btn" href="/cbt">🧠 العلاج السلوكي المعرفي (CBT)</a>
        <a class="btn" href="/addiction">🚭 الإدمان والتعافي</a>
        <a class="btn" href="https://t.me/Mhfh1414">📞 تواصل عبر التليجرام</a>
    </body>
    </html>
    """)
