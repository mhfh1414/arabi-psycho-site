/* === Arabi Psycho – Royal Navy & Gold === */
:root{
  /* كُحلي عميق */
  --bg-0:#070c18;               /* خلفية عامة كحلي داكن جدًا */
  --bg-1:#0b1224;               /* طبقة ثانية */
  --navy:#0e1a33;               /* كُحلي أساسي للبطاقات */

  /* ذهبي معدني (درجات) */
  --gold-1:#8f6b00;  /* ظل غامق */
  --gold-2:#b38800;  /* وسط */
  --gold-3:#d4af37;  /* ذهبي كلاسيك */
  --gold-4:#f5cc58;  /* إضاءة */
  --gold-5:#ffe8a0;  /* لمعة */

  /* ألوان مساعدة */
  --success:#22c55e;
  --danger:#ef4444;

  /* نصوص وحدود */
  --text:#f3f6ff;
  --muted:#b9c3da;
  --border:rgba(255,255,255,.08);

  /* توّهجات */
  --navy-glow: 0 14px 34px rgba(15,27,51,.45);
  --gold-glow: 0 10px 28px rgba(244,204,88,.35), 0 4px 10px rgba(212,175,55,.35);

  /* تدرجات ذهبيّة/كُحليّة */
  --grad-gold: linear-gradient(92deg, var(--gold-1), var(--gold-3) 45%, var(--gold-4) 60%, var(--gold-2));
  --grad-navy: linear-gradient(180deg, #0b1329, #0b1224);
}

/* خلفيّة ملكيّة */
body{
  margin:0; color:var(--text);
  background:
    radial-gradient(1200px 720px at 85% -10%, rgba(245,204,88,.12), transparent 60%),
    radial-gradient(900px 600px at -10% 70%, rgba(15,27,51,.55), transparent 60%),
    var(--grad-navy);
  font-family:"Tajawal",system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
  letter-spacing:.2px;
}

/* حاوية */
.container{max-width:1150px;margin:auto;padding:30px 18px;}

/* شريط علوي زجاجي بلمعة ذهبية خفيفة */
.appbar{
  position:sticky;top:0;z-index:50;
  background:linear-gradient(180deg, rgba(7,12,24,.86), rgba(7,12,24,.55));
  backdrop-filter:blur(10px);
  border-bottom:1px solid var(--border);
  box-shadow: 0 6px 14px rgba(0,0,0,.35);
}

/* بطاقات كُحليّة زجاجيّة بحواف ذهبية دقيقة */
.card{
  background:linear-gradient(180deg, rgba(14,26,51,.85), rgba(14,26,51,.72));
  border:1px solid rgba(245,204,88,.18);
  border-radius:22px; overflow:hidden;
  box-shadow:var(--navy-glow);
}
.card--gold{
  border-image: var(--grad-gold) 1;
  box-shadow: var(--gold-glow), var(--navy-glow);
}

/* عناوين بلمعة ذهبية معدنية متحركة */
h1,h2,h3{
  margin:.1rem 0 .6rem; font-weight:800; line-height:1.08;
  background:linear-gradient(90deg, var(--gold-2), var(--gold-4) 45%, var(--gold-5) 55%, var(--gold-3));
  -webkit-background-clip:text; background-clip:text; color:transparent;
  position:relative;
}
h1{font-size:clamp(30px,3.8vw,48px)}
h2{font-size:clamp(22px,2.6vw,32px)}
h3{font-size:clamp(18px,2vw,24px)}
/* لمعة عابرة */
h1::after,h2::after{
  content:""; position:absolute; inset:0 auto 0 -120%;
  width:120px; transform:skewX(-18deg);
  background:linear-gradient(90deg, transparent, rgba(255,255,255,.7), transparent);
  filter:blur(2px); animation:shimmer 4.2s linear infinite;
}
@keyframes shimmer{ 0%{left:-120%} 60%{left:140%} 100%{left:140%} }

.lead{color:var(--muted);font-size:clamp(16px,1.6vw,18px);line-height:1.8}

/* أزرار ملكيّة */
.btn{
  display:inline-flex;align-items:center;gap:10px;
  padding:12px 18px;border-radius:16px;font-weight:800;
  color:#1a1300;text-shadow:0 1px 0 rgba(255,255,255,.4);
  background:var(--grad-gold); border:1px solid rgba(213,176,55,.5);
  box-shadow: var(--gold-glow);
  transition: transform .12s ease, filter .12s ease, box-shadow .12s ease;
}
.btn:hover{transform:translateY(-2px) scale(1.02);filter:saturate(1.12) brightness(1.02);}
.btn:active{transform:none;filter:saturate(1);}
.btn:focus-visible{outline:2px solid transparent;box-shadow:0 0 0 6px rgba(245,204,88,.35), var(--gold-glow);}

/* أزرار ثانوية بكُحلي وحواف ذهبية */
.btn--ghost{
  color:var(--text); text-shadow:none;
  background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
  border:1px solid rgba(245,204,88,.35); box-shadow: var(--navy-glow);
}
.btn--success{ background:linear-gradient(92deg,#2bb255,#5ae08d); color:#06100a; }
.btn--danger{  background:linear-gradient(92deg,#f14646,#ff7b7b); color:#240404; }

/* رقاقات */
.chip{
  display:inline-flex;align-items:center;gap:8px;padding:10px 14px;border-radius:28px;
  color:var(--text);
  background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
  border:1px solid rgba(245,204,88,.22);
}
.chip--on{ box-shadow:0 0 0 3px rgba(245,204,88,.25) inset; }

/* إدخالات */
.input, select, textarea{
  width:100%;color:var(--text);
  background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
  border:1px solid rgba(245,204,88,.25); border-radius:14px; padding:12px 14px;
  transition:border-color .12s ease, box-shadow .12s ease;
}
.input::placeholder{color:#c9d1ea}
.input:focus{outline:none;border-color:var(--gold-4);box-shadow:0 0 0 6px rgba(245,204,88,.22)}

/* أقسام */
.section{padding:28px}
.section--hero{
  background:linear-gradient(180deg, rgba(212,175,55,.10), rgba(15,27,51,.35));
  border:1px solid rgba(245,204,88,.25); border-radius:26px;
  box-shadow: var(--gold-glow);
}

/* سايدبار */
.sidebar{position:sticky; top:84px; display:flex; flex-direction:column; gap:12px;}
.sidebar .btn{width:100%;justify-content:flex-start}

/* فاصل ذهبي ناعم */
.hr{
  height:1px; border:none; margin:18px 0;
  background:linear-gradient(90deg, transparent, rgba(245,204,88,.55), transparent);
}

/* تذييل */
footer{
  margin-top:28px; padding:22px; text-align:center; color:var(--muted);
  border-top:1px solid rgba(245,204,88,.25);
  background:linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.02));
}

/* حركات بسيطة */
.fade-in{animation:fade .6s ease both}
@keyframes fade{from{opacity:0;transform:translateY(6px)} to{opacity:1;transform:none}}

/* وضع فاتح (اختياري) */
html.light{
  --bg-0:#f7f4ea; --bg-1:#f4efe1; --navy:#ffffff;
  --text:#0b1224; --muted:#303a52; --border:rgba(11,18,36,.12);
  --navy-glow:0 10px 24px rgba(11,18,36,.12);
  --gold-glow:0 8px 20px rgba(212,175,55,.25);
}
