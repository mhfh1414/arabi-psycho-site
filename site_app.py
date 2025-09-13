/* === Arabi Psycho – Vibrant Theme === */
:root{
  /* أساس الألوان */
  --bg-0:#0b1020;                /* خلفية عامة داكنة */
  --bg-1:#0f1733;                /* طبقة ثانية */
  --card:rgba(16,24,48,.72);     /* بطاقات زجاجية */
  --border:rgba(255,255,255,.08);

  /* ألوان العلامة */
  --primary:#3A7AFE;             /* أزرق أساسي */
  --primary-2:#00D4FF;           /* سماوي */
  --accent:#9B5CFF;              /* بنفسجي فخم */
  --success:#22c55e;
  --warning:#f59e0b;
  --danger:#ef4444;

  /* نصوص */
  --text:#EAF0FF;
  --muted:#A9B4D0;

  /* هالات وإضاءات */
  --ring:rgba(58,122,254,.55);
  --glow: 0 10px 30px rgba(58,122,254,.35), 0 6px 14px rgba(0,212,255,.25);

  /* تدرجات */
  --grad-1:#1a2a6c; --grad-2:#2a6cf6; --grad-3:#00d4ff;
}

/* خلفية ديناميكيّة */
body{
  margin:0; color:var(--text); background: radial-gradient(1200px 700px at 85% -10%, rgba(0,212,255,.12), transparent 60%),
                                   radial-gradient(900px 600px at -10% 70%, rgba(155,92,255,.10), transparent 60%),
                                   linear-gradient(180deg, var(--bg-0), var(--bg-1));
  font-family: "Tajawal", system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  letter-spacing:.2px;
}

/* حاوية عامة */
.container{
  max-width:1100px; margin:auto; padding:28px 18px;
}

/* شريط علوي */
.appbar{
  position:sticky; top:0; z-index:50;
  backdrop-filter: blur(10px);
  background: linear-gradient(180deg, rgba(11,16,32,.85), rgba(11,16,32,.55));
  border-bottom:1px solid var(--border);
}

/* البطاقات */
.card{
  background: var(--card);
  border:1px solid var(--border);
  border-radius:20px;
  box-shadow: 0 10px 20px rgba(0,0,0,.25);
  overflow:hidden;
}
.card--glow{ box-shadow: var(--glow); }

/* العناوين والنص */
h1{ font-size: clamp(28px, 3.6vw, 46px); margin:0 0 14px; line-height:1.08;
    background:linear-gradient(90deg,var(--primary),var(--primary-2),var(--accent));
    -webkit-background-clip:text; background-clip:text; color:transparent; font-weight:800;}
h2{ font-size: clamp(22px,2.6vw,32px); margin:0 0 8px; font-weight:700;}
.lead{ color:var(--muted); font-size:clamp(16px,1.6vw,18px); line-height:1.7}

/* أزرار فاخرة */
.btn{
  --bg: var(--primary);
  display:inline-flex; align-items:center; gap:10px;
  background: linear-gradient(92deg, var(--primary) 0%, var(--primary-2) 50%, var(--accent) 100%);
  color:#fff; padding:12px 18px; border-radius:14px;
  border:1px solid rgba(255,255,255,.08);
  box-shadow: var(--glow);
  text-decoration:none; font-weight:700;
  transition: transform .12s ease, box-shadow .12s ease, filter .12s ease;
}
.btn:hover{ transform: translateY(-2px) scale(1.02); filter:saturate(1.2); }
.btn:active{ transform: translateY(0); }
.btn:focus-visible{ outline:2px solid transparent; box-shadow:0 0 0 6px var(--ring), var(--glow); }
.btn--ghost{
  background: linear-gradient(180deg, rgba(58,122,254,.12), rgba(0,212,255,.12));
  color:var(--text); box-shadow:none; border:1px solid rgba(58,122,254,.35);
}
.btn--success{ background:linear-gradient(92deg,#22c55e,#00d38b); }
.btn--warning{ background:linear-gradient(92deg,#f59e0b,#f97316); }
.btn--danger{  background:linear-gradient(92deg,#ef4444,#f43f5e); }

/* كبسات صغيرة للفلاتر */
.chip{
  display:inline-flex; align-items:center; gap:8px;
  padding:10px 14px; border-radius:30px;
  background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
  border:1px solid var(--border); color:var(--text); font-weight:600;
}
.chip--on{ border-color:rgba(58,122,254,.55); box-shadow:0 0 0 3px rgba(58,122,254,.20) inset; }

/* قائمة جانبية */
.sidebar{
  position:sticky; top:84px;
  display:flex; flex-direction:column; gap:12px;
}
.sidebar .btn{ width:100%; justify-content:flex-start; }

/* مربعات الإدخال */
.input, select, textarea{
  width:100%; color:var(--text);
  background:linear-gradient(180deg, rgba(255,255,255,.06), rgba(255,255,255,.03));
  border:1px solid var(--border);
  border-radius:14px; padding:12px 14px;
  transition: box-shadow .12s ease, border-color .12s ease;
}
.input::placeholder{ color:#b9c3da; }
.input:focus{ outline: none; border-color: rgba(58,122,254,.55);
  box-shadow:0 0 0 5px rgba(58,122,254,.20); }

/* فواصل وتذييل */
.section{ padding:28px; }
.section--hero{
  background:linear-gradient(180deg, rgba(58,122,254,.20), rgba(155,92,255,.10), rgba(0,212,255,.12));
  border:1px solid var(--border); border-radius:24px;
}
footer{
  margin-top:24px; padding:22px; text-align:center; color:var(--muted);
  border-top:1px solid var(--border);
  background:linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.02));
}

/* تحسينات حركية بسيطة */
.fade-in{ animation:fade .6s ease both; }
@keyframes fade{ from{opacity:0; transform: translateY(6px)} to{opacity:1; transform:none} }

/* وضع فاتح (اختياري) – غيّره بإضافة .light على <html> */
html.light{
  --bg-0:#f7f9ff; --bg-1:#f0f4ff; --card:rgba(255,255,255,.85);
  --text:#0f1733; --muted:#334155; --border:rgba(15,23,51,.10);
  --ring: rgba(58,122,254,.30);
  --glow: 0 10px 30px rgba(58,122,254,.18), 0 6px 14px rgba(0,212,255,.14);
}
