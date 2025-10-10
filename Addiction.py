# addiction.py — صفحة برنامج الإدمان كبلوپرنت مستقل
from flask import Blueprint, current_app, Markup

addiction_bp = Blueprint("addiction", __name__)

def _page(content_html: str) -> str:
    shell = current_app.config["SHELL"]
    load_count = current_app.config["LOAD_COUNT"]
    return shell("علاج الإدمان", content_html, load_count())

def _brand_urls():
    return current_app.config["BRAND"], current_app.config["WA_URL"]

ADDICTION_HTML = """
<div class="card">
  <h1>🚭 برنامج الإدمان — مسار واضح</h1>
  <p class="small">تقييم → سحب آمن → تأهيل → رعاية لاحقة → خطة منع الانتكاس.</p>
  <div class="grid">
    <div class="tile"><h3>1) التقييم الأولي</h3><ul><li>تاريخ التعاطي والمواد والشدة.</li><li>فحوصات السلامة والمخاطر.</li></ul></div>
    <div class="tile"><h3>2) Detox</h3><ul><li>سحب آمن بإشراف طبي.</li><li>ترطيب ونوم ودعم غذائي.</li></ul></div>
    <div class="tile"><h3>3) Rehab</h3><ul><li>CBT للإدمان، مهارات رفض، إدارة مثيرات.</li><li>مجموعات دعم/أسرة.</li></ul></div>
    <div class="tile"><h3>4) Aftercare</h3><ul><li>متابعة أسبوعية أول 3 أشهر.</li><li>نشاطات بديلة صحية.</li></ul></div>
    <div class="tile"><h3>5) منع الانتكاس</h3><ul><li>قائمة مثيرات شخصية + بدائل.</li><li>شبكة تواصل فوري.</li></ul></div>
  </div>
  <div class="row" style="margin-top:12px">
    <a class="btn gold" href="/case">اربط مع دراسة الحالة</a>
    <a class="btn" href="/book">📅 احجز جلسة</a>
  </div>
</div>
"""

@addiction_bp.get("/addiction")
def addiction_page():
    return _page(Markup(ADDICTION_HTML))
