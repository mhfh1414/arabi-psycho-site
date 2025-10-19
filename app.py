# -*- coding: utf-8 -*-
# Arabi Psycho — One-File App (Home + Case + CBT + Addiction)

from flask import Flask, render_template_string

app = Flask(__name__)

# -----------------[ إعدادات عامة ]-----------------
BRAND  = "عربي سايكو"
LOGO   = "🧠"
TG_URL = "https://t.me/Mhfh1414"
WA_URL = "https://wa.me/966500000000"

# -----------------[ قالب موحّد ]-----------------
def shell(title, content):
    return render_template_string(f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>{BRAND} - {title}</title>
<style>
  :root{{--p:#3949ab;--g:#f9a825;--bg:#fafafa;--ink:#222}}
  *{{box-sizing:border-box}} body{{margin:0;font-family:Tahoma,Arial,sans-serif;background:var(--bg);color:var(--ink)}}
  header{{background:#283593;color:#fff;padding:14px;text-align:center;font-size:20px}}
  .wrap{{max-width:980px;margin:20px auto;padding:0 12px}}
  .card{{background:#fff;border:1px solid #eee;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,.05);padding:18px;margin-bottom:14px}}
  h1,h2,h3{{color:#283593;margin:.4rem 0}}
  .btn{{display:inline-block;background:var(--p);color:#fff;text-decoration:none;border:none;border-radius:10px;padding:9px 14px;margin:4px 4px 0 0;cursor:pointer}}
  .btn.gold{{background:var(--g);color:#222}} .btn.alt{{background:#6d4c41}}
  .btn.wa{{background:#25D366}} .btn.tg{{background:#0088cc}}
  input,select,textarea{{width:100%;padding:10px;border:1px solid #ddd;border-radius:10px;margin:6px 0}}
  .table{{width:100%;border-collapse:collapse;margin-top:8px}}
  .table th,.table td{{border:1px solid #ddd;padding:6px;text-align:center}}
  footer{{text-align:center;color:#777;padding:12px 0;font-size:13px}}
</style>
</head>
<body>
  <header>{LOGO} {BRAND}</header>
  <div class="wrap">
    <div class="card">
      <nav>
        <a class="btn gold" href="/">الرئيسية</a>
        <a class="btn" href="/case">دراسة الحالة</a>
        <a class="btn" href="/cbt">CBT</a>
        <a class="btn" href="/addiction">برنامج الإدمان</a>
        <a class="btn tg" href="{TG_URL}" target="_blank" rel="noopener">تيليجرام</a>
        <a class="btn wa" href="{WA_URL}" target="_blank" rel="noopener">واتساب</a>
      </nav>
    </div>
    <div class="card">
      {content}
    </div>
  </div>
  <footer>© جميع الحقوق محفوظة لـ {BRAND} — 2025</footer>
</body>
</html>
""")

# -----------------[ الرئيسية ]-----------------
@app.route("/")
def home():
    html = """
      <h1>مرحبًا بك 👋</h1>
      <p>اختر الصفحة المناسبة:</p>
      <a class="btn gold" href="/case">📋 دراسة الحالة</a>
      <a class="btn" href="/cbt">🧠 العلاج المعرفي السلوكي (CBT)</a>
      <a class="btn" href="/addiction">🚭 برنامج الإدمان</a>
    """
    return shell("الرئيسية", html)

# -----------------[ دراسة الحالة ]-----------------
@app.route("/case")
def case_form():
    html = """
    <h1>📋 دراسة الحالة</h1>
    <p>املأ الحقول التالية ثم احفظها كـ JSON عند الحاجة.</p>
    <form id="caseForm" onsubmit="return false;">
      <label>اسم المريض:</label>
      <input type="text" id="name">

      <label>العمر:</label>
      <input type="number" id="age">

      <label>الحالة الاجتماعية:</label>
      <select id="status">
        <option>أعزب</option><option>متزوج</option><option>منفصل</option><option>أرمل</option>
      </select>

      <h3>الأعراض</h3>
      <div>
        <label><input type="checkbox" class="sym" value="اكتئاب"> اكتئاب</label>
        <label><input type="checkbox" class="sym" value="قلق"> قلق</label>
        <label><input type="checkbox" class="sym" value="هلع"> هلع</label>
        <label><input type="checkbox" class="sym" value="وسواس"> وسواس</label>
        <label><input type="checkbox" class="sym" value="أرق"> أرق</label>
        <label><input type="checkbox" class="sym" value="شهية/وزن"> شهية/وزن</label>
      </div>

      <label>تفاصيل الأعراض:</label>
      <textarea id="symptoms" rows="4" placeholder="اكتب جميع الأعراض بالتفصيل..."></textarea>

      <label>المدة:</label>
      <input type="text" id="duration" placeholder="مثال: 3 أشهر">

      <label>علاجات سابقة:</label>
      <textarea id="treatments" rows="3"></textarea>

      <label>تشخيص مبدئي:</label>
      <input type="text" id="diagnosis">

      <button type="button" class="btn gold" onclick="saveCase()">💾 حفظ كـ JSON</button>
      <a class="btn" href="/cbt">الانتقال إلى CBT</a>
    </form>

    <script>
      function saveCase(){
        const checked=[...document.querySelectorAll('.sym:checked')].map(x=>x.value);
        const data = {
          name:document.getElementById('name').value,
          age:document.getElementById('age').value,
          status:document.getElementById('status').value,
          symptoms_list:checked,
          symptoms_text:document.getElementById('symptoms').value,
          duration:document.getElementById('duration').value,
          treatments:document.getElementById('treatments').value,
          diagnosis:document.getElementById('diagnosis').value
        };
        const a=document.createElement('a');
        a.href=URL.createObjectURL(new Blob([JSON.stringify(data,null,2)],{type:'application/json'}));
        a.download='case_study.json';
        a.click();
        URL.revokeObjectURL(a.href);
        alert('تم حفظ دراسة الحالة ✅');
      }
    </script>
    """
    return shell("دراسة الحالة", html)

# -----------------[ CBT ]-----------------
@app.route("/cbt")
def cbt():
    html = r"""
    <h1>🧠 العلاج المعرفي السلوكي (CBT)</h1>
    <p>اختر خطة واحدة، ثم أنشئ جدول 7/10/14 يوم. يعمل بدون أي ملفات خارجية.</p>

    <div>
      <label>الخطة:</label>
      <select id="plan">
        <option value="BA">BA — تنشيط سلوكي</option>
        <option value="TR">TR — سجل أفكار</option>
        <option value="SH">SH — نظافة النوم</option>
        <option value="ERP">ERP — وسواس قهري</option>
        <option value="SS">SS — مهارات اجتماعية</option>
      </select>

      <label>الأيام:</label>
      <select id="days">
        <option value="7">7</option>
        <option value="10">10</option>
        <option value="14">14</option>
      </select>

      <button type="button" class="btn gold" onclick="build()">إنشاء الجدول</button>
      <button type="button" class="btn" onclick="save()">تنزيل JSON</button>
      <button type="button" class="btn alt" onclick="window.print()">طباعة</button>
    </div>

    <div id="out" style="margin-top:10px"></div>

    <script>
      const TASKS = {
        "BA": ["نشاط ممتع","قياس المزاج","نشاط اجتماعي"],
        "TR": ["موقف","فكرة تلقائية","فكرة بديلة"],
        "SH": ["إغلاق الشاشات","موعد نوم ثابت","تقليل الكافيين"],
        "ERP": ["تعرّض","منع الطقوس","قياس القلق"],
        "SS": ["بدء محادثة","تواصل بصري","رد حازم"]
      };

      function build(){
        const plan=document.getElementById('plan').value;
        const days=parseInt(document.getElementById('days').value,10);
        const tasks=TASKS[plan]||[];
        let html = "<h3>خطة " + plan + " لمدة " + days + " يوم</h3>";
        html += "<table class='table'><thead><tr><th>اليوم</th>";
        for (let t of tasks) html += "<th>"+t+"</th>";
        html += "</tr></thead><tbody>";
        for (let d=1; d<=days; d++){
          html += "<tr><td><b>"+d+"</b></td>";
          for (let i=0;i<tasks.length;i++) html += "<td><input type='checkbox'></td>";
          html += "</tr>";
        }
        html += "</tbody></table>";
        document.getElementById('out').innerHTML = html;
      }

      function save(){
        const tbl = document.getElementById('out').innerHTML || "";
        const blob = new Blob([tbl], {type:"text/html"});
        const a=document.createElement('a');
        a.href=URL.createObjectURL(blob);
        a.download="cbt_plan.html";
        a.click();
        URL.revokeObjectURL(a.href);
      }
    </script>

    <div style="margin-top:10px">
      <a class="btn" href="/case">ربط مع دراسة الحالة</a>
      <a class="btn" href="/addiction">الذهاب لبرنامج الإدمان</a>
    </div>
    """
    return shell("CBT", html)

# -----------------[ برنامج الإدمان ]-----------------
@app.route("/addiction")
def addiction():
    html = """
    <h1>🚭 برنامج الإدمان</h1>
    <p>مسار مبسّط: تقييم أولي → سحب آمن → تأهيل → رعاية لاحقة → منع الانتكاس.</p>

    <h3>الخطوات</h3>
    <ol>
      <li><b>التقييم الأولي:</b> تاريخ التعاطي، الشدة، عوامل الخطر، شبكة الدعم.</li>
      <li><b>السحب (Detox):</b> إشراف طبي، توازن السوائل، النوم، التغذية.</li>
      <li><b>التأهيل (Rehab):</b> CBT للإدمان، مهارات الرفض، إدارة المثيرات، خطط بديلة.</li>
      <li><b>الرعاية اللاحقة (Aftercare):</b> متابعة أسبوعية، نشاطات صحية، مجموعات دعم.</li>
      <li><b>منع الانتكاس:</b> قائمة مثيرات شخصية، بدائل فورية، شبكة تواصل.</li>
    </ol>

    <div style="margin-top:10px">
      <a class="btn" href="/case">اربط مع دراسة الحالة</a>
      <a class="btn" href="/cbt">فتح CBT</a>
      <a class="btn tg" href="{TG}" target="_blank" rel="noopener">تيليجرام</a>
      <a class="btn wa" href="{WA}" target="_blank" rel="noopener">واتساب</a>
    </div>
    """.format(TG=TG_URL, WA=WA_URL)
    return shell("برنامج الإدمان", html)

# -----------------[ تشغيل ]-----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
