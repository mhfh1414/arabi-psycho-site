# -*- coding: utf-8 -*-
from flask import url_for, render_template_string

# حدّث روابط التواصل:
WA_LINK   = "https://wa.me/9665XXXXXXXX"         # رقم واتساب بصيغة دولية
TG_LINK   = "https://t.me/USERNAME"              # يوزر تيليجرام
EMAIL_LINK= "mailto:info@arabipsycho.com"        # بريد إلكتروني

def render_home():
    html = """
    <!doctype html>
    <html lang="ar" dir="rtl">
    <head>
      <meta charset="utf-8">
      <title>عربي سايكو | الرئيسية</title>
      <meta name="viewport" content="width=device-width, initial-scale=1"/>
      <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;600;800&display=swap" rel="stylesheet">
      <style>
        :root{
          --bg1:#0b3a75; --bg2:#0a65b0; --gold:#f4b400; --ink:#0a1330; --muted:#cfe0ff; --glass:rgba(255,255,255,.06);
        }
        *{box-sizing:border-box}
        body{
          margin:0; font-family:"Tajawal",system-ui; -webkit-font-smoothing:antialiased;
          background:
            radial-gradient(1200px 600px at 80% -10%, #1a4bbd22, transparent),
            linear-gradient(135deg,var(--bg1),var(--bg2));
          color:#fff;
        }
        .wrap{max-width:1240px; margin:auto; padding:28px 20px}
        header{
          display:flex; align-items:center; justify-content:space-between; gap:16px;
          position:sticky; top:0; z-index:10; backdrop-filter:blur(6px);
          background:linear-gradient(180deg, rgba(7,19,56,.35), transparent 80%);
          padding-bottom:8px;
        }
        .brand{display:flex; align-items:center; gap:14px}
        .badge{
          width:56px; height:56px; border-radius:16px; background:#0d2c54;
          border:1px solid #ffffff33; display:grid; place-items:center; font-weight:800; letter-spacing:.5px;
          box-shadow:0 8px 24px rgba(0,0,0,.25), inset 0 0 0 1px #ffffff22;
        }
        .title{margin:0; font-size:32px; line-height:1}
        .subtitle{margin:.25rem 0 0; color:var(--muted)}
        .actions{display:flex; align-items:center; gap:10px}
        .iconbtn{
          display:inline-flex; align-items:center; justify-content:center; gap:8px;
          text-decoration:none; color:#fff; padding:10px 12px; border-radius:12px;
          border:1px solid #ffffff22; background:var(--glass);
          transition:.2s ease; min-width:44px;
        }
        .iconbtn:hover{background:rgba(255,255,255,.12); transform:translateY(-1px)}
        .ico{width:18px; height:18px; display:inline-block; vertical-align:middle}
        .hero{
          margin:22px 0 26px; padding:22px;
          background:var(--glass); border:1px solid #ffffff22; border-radius:18px; backdrop-filter:blur(6px);
        }
        .btn{
          display:inline-flex; align-items:center; gap:10px; text-decoration:none; font-weight:800;
          background:linear-gradient(180deg,#ffd86a,#f4b400); color:#2b1b02;
          padding:14px 18px; border-radius:14px; box-shadow:0 6px 18px rgba(244,180,0,.28);
          transition:.2s ease;
        }
        .btn:hover{filter:brightness(1.04); transform:translateY(-1px)}
        .btn--alt{
          background:linear-gradient(180deg,#9cc5ff,#63a4ff); color:#04122c; box-shadow:0 6px 18px rgba(60,130,255,.28);
        }
        .grid{display:grid; grid-template-columns:repeat(3,1fr); gap:16px}
        @media (max-width:1020px){ .grid{grid-template-columns:1fr} }
        .card{
          background:var(--glass); border:1px solid #ffffff22; border-radius:16px; padding:18px;
          backdrop-filter:blur(6px); box-shadow:0 10px 26px rgba(0,0,0,.18);
        }
        .card h3{margin:0 0 8px}
        .card p{margin:0 0 12px; color:#dbe9ff}
        footer{
          margin-top:26px; display:flex; justify-content:space-between; gap:12px; color:#cfe0ff; opacity:.9;
          border-top:1px dashed #ffffff2a; padding-top:14px; font-size:.95rem;
        }
        .right-align{ text-align:right }
      </style>
    </head>
    <body>
      <div class="wrap">
        <!-- الهيدر: الشعار على اليمين + أيقونات التواصل -->
        <header>
          <div class="brand right-align">
            <div class="badge">AS</div>
            <div>
              <h1 class="title">عربي سايكو</h1>
              <p class="subtitle">مركز عربي سايكو يرحّب بكم — نخدمك أينما كنت</p>
            </div>
          </div>
          <nav class="actions">
            <a class="iconbtn" href="{{ url_for('contact_whatsapp') }}" title="واتساب">
              <!-- WhatsApp SVG -->
              <svg class="ico" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M20 3.9A10 10 0 0 0 3.5 17.4L3 21l3.7-.9A10 10 0 1 0 20 3.9Zm-8 17a8.4 8.4 0 0 1-4.3-1.2l-.3-.2-2.5.6.5-2.4-.2-.3A8.5 8.5 0 1 1 12 20.9Zm4.7-6.3-.6-.3c-.3-.1-1.8-.9-2-.9s-.5-.1-.7.3-.8.9-.9 1-.3.2-.6.1a7 7 0 0 1-2-1.2 7.4 7.4 0 0 1-1.4-1.7c-.1-.2 0-.4.2-.5l.5-.6.2-.3v-.3l-.1-.3-1-2c-.2-.6-.5-.5-.7-.5h-.6l-.3.1a1.4 1.4 0 0 0-.4 1.1 4.9 4.9 0 0 0 1 2.4 11.2 11.2 0 0 0 4.3 4 4.8 4.8 0 0 0 2.8.9c.6 0 1.2 0 1.7-.3a3.8 3.8 0 0 0 1.3-1 .9.9 0 0 0 .2-1c-.1-.2-.5-.3-.8-.5Z"/>
              </svg>
              <span>واتساب</span>
            </a>
            <a class="iconbtn" href="{{ url_for('contact_telegram') }}" title="تلجرام">
              <!-- Telegram SVG -->
              <svg class="ico" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M9.1 16.3 8.9 20c.4 0 .6-.2.9-.4l2.1-2 4.3 3.1c.8.5 1.4.3 1.6-.8l2.9-13.4c.3-1.2-.4-1.7-1.2-1.4L2.8 9.7c-1.1.4-1.1 1.1-.2 1.4l4.3 1.3 10-6.3c.5-.3.9-.1.5.2l-8.1 7- .2 0Z"/>
              </svg>
              <span>تلجرام</span>
            </a>
            <a class="iconbtn" href="{{ url_for('contact_email') }}" title="إيميل">
              <!-- Mail SVG -->
              <svg class="ico" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 4-8 5-8-5V6l8 5 8-5v2Z"/>
              </svg>
              <span>إيميل</span>
            </a>
          </nav>
        </header>

        <!-- هيرو: أزرار كبيرة واضحة للأقسام -->
        <section class="hero">
          <div style="display:flex; flex-wrap:wrap; gap:12px; align-items:center; justify-content:flex-start">
            <a class="btn" href="{{ url_for('dsm') }}">🗂️ دراسة الحالة + التشخيص (DSM)</a>
            <a class="btn btn--alt" href="{{ url_for('cbt') }}">💡 العلاج السلوكي المعرفي + الاختبارات</a>
            <a class="btn" href="{{ url_for('addiction') }}">🚭 علاج الإدمان</a>
          </div>
        </section>

        <!-- بطاقات تعريفية -->
        <section class="grid">
          <div class="card">
            <h3>📖 DSM-5</h3>
            <p>قاعدة اضطرابات موسّعة + مطابقة كلمات لنتيجة تقديرية فورية عبر دراسة حالة.</p>
            <a class="btn" href="{{ url_for('dsm') }}">ابدأ الآن</a>
          </div>
          <div class="card">
            <h3>🧪 الاختبارات + CBT</h3>
            <p>PHQ-9 | GAD-7 | PCL-5 | Big Five — تُسند خطة CBT الأولية بناءً على النتائج.</p>
            <a class="btn btn--alt" href="{{ url_for('cbt') }}">افتح لوحة الاختبارات</a>
          </div>
          <div class="card">
            <h3>🚭 علاج الإدمان</h3>
            <p>تقييم أولي لمسار آمن + خطة علاجية وإحالة طبية عند الحاجة.</p>
            <a class="btn" href="{{ url_for('addiction') }}">ابدأ التقييم</a>
          </div>
        </section>

        <footer>
          <div>© {{ year }} عربي سايكو — جميع الحقوق محفوظة</div>
          <div>واجهة مُحسّنة بأزرق/ذهبي — تصميم رشيق يمنح هيبة وثقة</div>
        </footer>
      </div>
    </body>
    </html>
    """
    return render_template_string(html, year=2025)
