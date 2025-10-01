# -*- coding: utf-8 -*-
# ipb.py — سيرفر ويب يربط DSM.py / CBT.py / Addiction.py (بدون مكتبات خارجية).
# مناسب للخطة المجانية على Render. للتشغيل محليًا: python ipb.py ثم افتح http://127.0.0.1:8080

import os
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

from DSM import DSM
from CBT import CBT
from Addiction import Addiction

PORT = int(os.environ.get("PORT", "8080"))
dsm, cbt, addx = DSM(), CBT(), Addiction()

# تخزين مؤقت داخل الذاكرة (غير دائم)
STORE = {
    "thoughts": [],     # سجلات أفكار
    "activation": [],   # تنشيط سلوكي
    "exposure": [],     # سُلّم تعرّض
    "weekly": [],       # متابعة أسبوعية
    "craving": []       # تتبّع الرغبة (إدمان)
}

def layout(title: str, body: str) -> bytes:
    html = f"""<!doctype html><html lang="ar" dir="rtl"><head>
<meta charset="utf-8"/><meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{title}</title>
<style>
body{{font-family:system-ui,Tahoma,Arial;background:#f5f7fb;color:#222;margin:0}}
header{{background:#22395d;color:#fff;padding:14px 18px}}
nav a{{color:#fff;margin-left:14px;text-decoration:none}}
.container{{max-width:1000px;margin:22px auto;background:#fff;padding:18px 18px 60px;border-radius:16px;box-shadow:0 8px 25px rgba(0,0,0,.06)}}
.card{{background:#fafafa;border:1px solid #eee;padding:12px 14px;border-radius:12px;margin:12px 0}}
.table{{width:100%;border-collapse:collapse}}
.table th,.table td{{text-align:right;border:1px solid #eee;padding:8px;vertical-align:top}}
.btns a,.btns button{{display:inline-block;margin:6px 4px;padding:8px 12px;border-radius:10px;border:1px solid #ddd;background:#f4f6ff;cursor:pointer;text-decoration:none;color:#223}}
.note{{background:#fff7d6;border:1px solid #f1d48f;padding:8px 10px;border-radius:8px}}
label{{display:block;margin-top:8px;font-weight:600}} input,textarea,select{{border:1px solid #ddd;border-radius:10px;padding:8px;width:100%}}
footer{{text-align:center;color:#666;padding:22px 0 40px}}
.search{{display:flex;gap:8px;align-items:center;margin:8px 0}}
.search input{{flex:1}}
</style></head><body>
<header><div class="nav"><strong>عربي سايكو</strong>
<nav style="float:left">
  <a href="/">الرئيسية</a>
  <a href="/dsm">DSM</a>
  <a href="/cbt">CBT</a>
  <a href="/addiction">علاج الإدمان</a>
</nav></div></header>
<div class="container">{body}</div>
<footer><small>محتوى تثقيفي—لا يغني عن الرعاية الطبية المتخصصة.</small></footer>
</body></html>"""
    return html.encode("utf-8")

def home() -> bytes:
    body = """
    <h1>مرحبًا يا أبو فارس 👋</h1>
    <p>نسخة ويب موسّعة — ثلاثة ملفات محتوى + هذا الملف للتشغيل. بدون مكتبات خارجية، جاهزة للخطة المجانية.</p>
    <div class="card">
      <h3>الأقسام</h3>
      <ul>
        <li><b>DSM:</b> موسّع جدًا مع معايير مختصرة/عوامل خطورة/تشخيص تفريقي ومقاييس تثقيفية.</li>
        <li><b>CBT:</b> سجل أفكار متقدم، تنشيط، سُلّم تعرّض، Beck مبسّط، متابعة أسبوعية، خطة علاج، تمارين.</li>
        <li><b>الإدمان:</b> تصنيفات، انسحاب، مراحل علاج، دعم غير دوائي، خيارات عامة، تتبّع رغبة، وقاية انتكاس.</li>
      </ul>
      <div class="btns">
        <a href="/dsm">فتح DSM</a>
        <a href="/cbt">فتح CBT</a>
        <a href="/addiction">فتح علاج الإدمان</a>
      </div>
    </div>
    """
    return layout("الرئيسية", body)

# ================= DSM =================
def page_dsm(query: dict, method: str, environ=None) -> bytes:
    # بحث نصي بسيط داخل DSM
    if method == "POST" and environ:
        try:
            size = int(environ.get("CONTENT_LENGTH","0"))
        except ValueError:
            size = 0
        data = environ["wsgi.input"].read(size).decode("utf-8")
        form = parse_qs(data)
        كلمة = (form.get("q", [""])[0] or "").strip()
        نتائج = dsm.بحث_نصي(كلمة)
        if not نتائج:
            body = f"<h1>DSM — بحث</h1><p>لا نتائج لـ: <b>{كلمة}</b></p><div class='btns'><a href='/dsm'>رجوع</a></div>"
            return layout("DSM — بحث", body)
        links = "".join([f"<li><a href='/dsm/find?d={n}'>{n}</a></li>" for n in نتائج])
        body = f"<h1>DSM — نتائج البحث</h1><ul>{links}</ul><div class='btns'><a href='/dsm'>رجوع</a></div>"
        return layout("DSM — بحث", body)

    cat = query.get("cat", [""])[0]
    dis = query.get("d", [""])[0]
    if dis:
        body = dsm.html_اضطراب(dis) + "<div class='btns'><a href='/dsm?cat=%s'>رجوع</a> <a href='/dsm'>التصنيفات</a></div>" % (cat or "")
        return layout("DSM — " + dis, body)
    if cat:
        links = " ".join([f"<a class='btns' href='/dsm?cat={cat}&d={n}'>{n}</a>" for n in dsm.قائمة_الاضطرابات(cat)])
        body = ("<div class='card'><form class='search' method='post' action='/dsm'>"
                "<input name='q' placeholder='ابحث داخل DSM (اسم/أعراض/تشخيص تفريقي)'>"
                "<button type='submit'>بحث</button></form></div>")
        body += f"<div class='btns'>{links}</div>" + dsm.html_تصنيف(cat) + "<div class='btns'><a href='/dsm'>كل التصنيفات</a></div>"
        return layout("DSM — " + cat, body)
    items = "".join([f"<li><a href='/dsm?cat={c}'>{c}</a></li>" for c in dsm.التصنيفات()])
    search = ("<div class='card'><form class='search' method='post' action='/dsm'>"
              "<input name='q' placeholder='ابحث داخل DSM'>"
              "<button type='submit'>بحث</button></form></div>")
    return layout("DSM — التصنيفات", search + f"<h1>DSM</h1><ul>{items}</ul>")

# ================= CBT =================
def page_cbt_get() -> bytes:
    body = f"""
    <h1>CBT — أدوات موسّعة</h1>
    <div class="card"><h3>سجل الأفكار (متقدم)</h3>{cbt.html_نموذج_سجل_أفكار()}</div>
    <div class="card"><h3>تنشيط سلوكي — إدخال بند</h3>{cbt.html_نموذج_تنشيط()}</div>
    <div class="card"><h3>سُلّم تعرّض — إضافة بند</h3>{cbt.html_نموذج_سلم_تعرّض()}</div>
    <div class="card"><h3>استبيان Beck المبسّط — القلق</h3>{cbt.html_بيك_نموذج('قلق')}</div>
    <div class="card"><h3>استبيان Beck المبسّط — الاكتئاب</h3>{cbt.html_بيك_نموذج('اكتئاب')}</div>
    <div class="card"><h3>متابعة أسبوعية</h3>{cbt.html_نموذج_متابعة()}</div>
    <div class="card"><h3>خطة علاج — قالب مختصر</h3>{cbt.html_قالب_خطة_علاج()}</div>
    <div class="card"><h3>تمارين مساندة</h3>{cbt.html_تمارين()}</div>
    <div class="btns"><a href="/cbt/store">عرض السجلات المخزّنة مؤقتًا</a></div>
    """
    return layout("CBT", body)

def _parse_form(environ):
    try:
        size = int(environ.get("CONTENT_LENGTH","0"))
    except ValueError:
        size = 0
    data = environ["wsgi.input"].read(size).decode("utf-8")
    return parse_qs(data)

def page_cbt_post(environ, path: str) -> bytes:
    form = _parse_form(environ)

    if path == "/cbt/thought-record":
        rec = {f: (form.get(f,[""])[0] or "").strip() for f in cbt.سجل_الأفكار_حقول}
        STORE["thoughts"].append(rec)
        body = "<h1>نتيجة سجل الأفكار</h1>" + cbt.html_عرض_سجل(rec) + "<div class='btns'><a href='/cbt'>رجوع</a> <button onclick='window.print()'>طباعة</button></div>"
        return layout("CBT — سجل أفكار", body)

    if path == "/cbt/activation":
        row = {f: (form.get(f,[""])[0] or "").strip() for f in cbt.تنشيط_سلوكي_حقول}
        STORE["activation"].append(row)
        body = "<h1>تنشيط سلوكي — آخر إدخال</h1>" + cbt.html_عرض_تنشيط(row) + "<div class='btns'><a href='/cbt/store'>عرض الكل</a> <a href='/cbt'>رجوع</a></div>"
        return layout("CBT — تنشيط", body)

    if path == "/cbt/exposure":
        row = {f: (form.get(f,[""])[0] or "").strip() for f in cbt.سلم_تعرّض_حقول}
        STORE["exposure"].append(row)
        body = "<h1>سُلّم تعرّض — آخر إدخال</h1>" + cbt.html_عرض_سلم(row) + "<div class='btns'><a href='/cbt/store'>عرض الكل</a> <a href='/cbt'>رجوع</a></div>"
        return layout("CBT — تعرّض", body)

    if path.endswith("/beck/anx") or path.endswith("/beck/dep"):
        vals = []
        for i in range(1, 8):
            try:
                v = int((form.get(f"q{i}",["0"])[0] or "0"))
            except ValueError:
                v = 0
            vals.append(0 if v<0 else (3 if v>3 else v))
        total = sum(vals)
        body = "<h1>نتيجة تقديرية</h1>" + cbt.html_بيك_عرض(total, "قلق" if path.endswith("/anx") else "اكتئاب") + "<div class='btns'><a href='/cbt'>رجوع</a> <button onclick='window.print()'>طباعة</button></div>"
        return layout("CBT — Beck", body)

    if path == "/cbt/weekly":
        row = {f: (form.get(f,[""])[0] or "").strip() for f in cbt.متابعة_أسبوعية_حقول}
        STORE["weekly"].append(row)
        body = "<h1>متابعة أسبوعية — معاينة</h1>" + cbt.html_عرض_متابعة(row) + "<div class='btns'><a href='/cbt/store'>عرض الكل</a> <a href='/cbt'>رجوع</a> <button onclick='window.print()'>طباعة</button></div>"
        return layout("CBT — متابعة", body)

    if path == "/cbt/plan":
        fields = ["الأهداف_العامة","أهداف_قصيرة","العوائق","الاستراتيجيات","الدعم_المتوفر","خطة_طارئة","مؤشرات_التقدم"]
        row = {f: (form.get(f,[""])[0] or "").strip() for f in fields}
        table = cbt.html_عرض_خطة(row)
        body = "<h1>خطة علاج — معاينة</h1>" + table + "<div class='btns'><a href='/cbt'>رجوع</a> <button onclick='window.print()'>طباعة</button></div>"
        return layout("CBT — خطة", body)

    return layout("CBT", "<p>طلب غير معروف.</p>")

def page_cbt_store() -> bytes:
    def render(title, rows, renderer):
        if not rows:
            return f"<div class='card'><h3>{title}</h3><p>لا يوجد بيانات بعد.</p></div>"
        parts = [f"<div class='card'><h3>{title}</h3>"]
        for r in rows[::-1][:15]:
            parts.append(renderer(r))
        parts.append("</div>")
        return "\n".join(parts)

    body = "<h1>المخزّن مؤقتًا</h1>"
    body += render("سجلات أفكار", STORE["thoughts"], cbt.html_عرض_سجل)
    body += render("تنشيط سلوكي", STORE["activation"], cbt.html_عرض_تنشيط)
    body += render("سُلّم تعرّض", STORE["exposure"], cbt.html_عرض_سلم)
    body += render("متابعة أسبوعية", STORE["weekly"], cbt.html_عرض_متابعة)
    body += "<div class='btns'><a href='/cbt'>رجوع</a></div>"
    return layout("CBT — المخزن المؤقت", body)

# ================= Addiction =================
def page_addiction_get() -> bytes:
    body = """
    <h1>علاج الإدمان</h1>
    <div class="card">%s</div>
    <div class="card">%s</div>
    <div class="card">%s</div>
    <div class="card">%s</div>
    <div class="card">%s</div>
    <div class="card"><h3>خطة وقاية من الانتكاس — نموذج</h3>%s</div>
    <div class="card"><h3>تتبّع يومي للرغبة (Craving)</h3>%s</div>
    """ % (
        addx.html_المواد(),
        addx.html_انسحاب(),
        addx.html_مراحل(),
        addx.html_دعم(),
        addx.html_خيارات(),
        addx.html_قالب_انتكاس(),
        addx.html_تتبع_نموذج()
    )
    return layout("علاج الإدمان", body)

def page_addiction_post(environ, path: str) -> bytes:
    try:
        size = int(environ.get("CONTENT_LENGTH","0"))
    except ValueError:
        size = 0
    data = environ["wsgi.input"].read(size).decode("utf-8")
    form = parse_qs(data)

    if path == "/addiction/relapse-plan":
        fields = ["محفزات","مهارات","دعم","نمط"]
        row = {f: (form.get(f,[""])[0] or "").strip() for f in fields}
        body = "<h1>خطة وقاية من الانتكاس — معاينة</h1>" + addx.html_عرض_انتكاس(row) + "<div class='btns'><a href='/addiction'>رجوع</a> <button onclick='window.print()'>طباعة</button></div>"
        return layout("علاج الإدمان — خطة", body)

    if path == "/addiction/craving":
        row = {f: (form.get(f,[""])[0] or "").strip() for f in addx.تتبّع_الرغبة_حقول}
        STORE["craving"].append(row)
        body = "<h1>تتبّع الرغبة — آخر إدخال</h1>" + addx.html_تتبع_عرض(row) + "<div class='btns'><a href='/addiction'>رجوع</a> <button onclick='window.print()'>طباعة</button></div>"
        return layout("علاج الإدمان — تتبّع", body)

    return layout("علاج الإدمان", "<p>طلب غير معروف.</p>")

# ================= Router =================
def application(environ, start_response):
    path = environ.get("PATH_INFO","/")
    method = environ.get("REQUEST_METHOD","GET")
    query = parse_qs(environ.get("QUERY_STRING",""))

    if path in ("/",""):
        start_response("200 OK",[("Content-Type","text/html; charset=utf-8")]); return [home()]

    # DSM
    if path == "/dsm" and method == "GET":
        start_response("200 OK",[("Content-Type","text/html; charset=utf-8")]); return [page_dsm(query, "GET")]
    if path == "/dsm" and method == "POST":
        start_response("200 OK",[("Content-Type","text/html; charset=utf-8")]); return [page_dsm(query, "POST", environ)]
    if path.startswith("/dsm"):
        start_response("200 OK",[("Content-Type","text/html; charset=utf-8")]); return [page_dsm(query, "GET")]

    # CBT
    if path == "/cbt" and method == "GET":
        start_response("200 OK",[("Content-Type","text/html; charset=utf-8")]); return [page_cbt_get()]
    if path.startswith("/cbt/") and method == "POST":
        start_response("200 OK",[("Content-Type","text/html; charset=utf-8")]); return [page_cbt_post(environ, path)]
    if path == "/cbt/store" and method == "GET":
        start_response("200 OK",[("Content-Type","text/html; charset=utf-8")]); return [page_cbt_store()]

    # Addiction
    if path == "/addiction" and method == "GET":
        start_response("200 OK",[("Content-Type","text/html; charset=utf-8")]); return [page_addiction_get()]
    if path.startswith("/addiction/") and method == "POST":
        start_response("200 OK",[("Content-Type","text/html; charset=utf-8")]); return [page_addiction_post(environ, path)]

    start_response("404 Not Found",[("Content-Type","text/html; charset=utf-8")])
    return [layout("غير موجود", "<h1>المسار غير موجود</h1><div class='btns'><a href='/'>الرئيسية</a></div>")]

if __name__ == "__main__":
    with make_server("", PORT, application) as httpd:
        print(f"Serving on port {PORT} ...")
        httpd.serve_forever()
