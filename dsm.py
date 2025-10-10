# dsm.py — مرجع DSM كبلوپرنت مستقل
from flask import Blueprint, current_app, Markup

dsm_bp = Blueprint("dsm", __name__)

def _page(content_html: str) -> str:
    shell = current_app.config["SHELL"]
    load_count = current_app.config["LOAD_COUNT"]
    return shell("DSM — مرجع", content_html, load_count())

DSM_HTML = """
<div class="card">
  <h1>📘 DSM — ملخّص داخلي</h1>
  <p class="small">مرجع سريع لقراءة النتائج وتوجيه الخطط.</p>
  <div class="grid">
    <div class="tile"><h3>الاكتئاب (MDD)</h3><ul>
      <li>مزاج منخفض/فقد المتعة + ≥4 (نوم/شهية/طاقة/تباطؤ/ذنب/تركيز/أفكار إيذاء).</li>
      <li>المدة ≥ أسبوعين + تأثير وظيفي.</li>
    </ul></div>
    <div class="tile"><h3>القلق المعمّم</h3><ul><li>قلق زائد ≥6 أشهر + توتر/إجهاد/تركيز/نوم..</li></ul></div>
    <div class="tile"><h3>الهلع</h3><ul><li>نوبات مفاجئة + خشية التكرار وتجنّب.</li></ul></div>
    <div class="tile"><h3>القلق الاجتماعي</h3><ul><li>خشية تقييم الآخرين وتجنّب.</li></ul></div>
    <div class="tile"><h3>الوسواس القهري (OCD)</h3><ul><li>وساوس + أفعال قهرية تؤثر على الأداء.</li></ul></div>
    <div class="tile"><h3>PTSD</h3><ul><li>استرجاعات/كوابيس/تجنّب/يقظة مفرطة.</li></ul></div>
    <div class="tile"><h3>طيف الفصام</h3><ul><li>ذهانية ± أعراض سلبية؛ النوع حسب المدة والأداء.</li></ul></div>
    <div class="tile"><h3>ثنائي القطب</h3><ul><li>هوس (≥7 أيام/دخول) أو هوس خفيف + اكتئاب.</li></ul></div>
    <div class="tile"><h3>تعاطي المواد</h3><ul><li>اشتهاء/انسحاب/استخدام رغم الضرر… الشدة حسب عدد المعايير.</li></ul></div>
  </div>
</div>
"""

@dsm_bp.get("/dsm")
def dsm_page():
    return _page(Markup(DSM_HTML))
