# Addiction.py — برنامج مختصر لعلاج الإدمان (تعليمي)

HTML = """
<h1>🚭 علاج الإدمان — برنامج مختصر</h1>
<p class="muted">محتوى تعليمي، ويُنصح بمراجعة مختص/عيادة عند الحاجة.</p>

<h2>1) التقييم الأولي</h2>
<div class="grid">
  <input placeholder="المادة/السلوك"/>
  <input placeholder="المدة والكمية"/>
  <input placeholder="أهم المحفزات"/>
  <input placeholder="أعراض انسحاب ظهرت سابقًا؟"/>
</div>

<h2>2) خطة الإقلاع</h2>
<ul>
  <li>موعد بدء واضح + دعم أسري/صديق مسؤول.</li>
  <li>إزالة المحفزات من البيئة (أماكن/أرقام/أدوات).</li>
  <li>استبدالات صحية: مشي، تنفس 4-7-8، تواصل مع داعم.</li>
</ul>

<h2>3) الوقاية من الانتكاس</h2>
<div class="grid">
  <textarea style="width:100%;height:80px" placeholder="المحفزات الشخصية (أماكن/أشخاص/مشاعر)"></textarea>
  <textarea style="width:100%;height:80px" placeholder="خطة التعامل مع كل محفز (تأجيل 10 دقائق، خروج من الموقف، اتصال بشخص داعم…)"></textarea>
</div>

<h2>4) متابعة أسبوعية</h2>
<div class="grid">
  <input placeholder="أيام الامتناع هذا الأسبوع"/>
  <input placeholder="مواقف عالية الخطورة"/>
  <input placeholder="مكافأة ذاتية صحية"/>
</div>

<h2>مصادر دعم</h2>
<p class="muted">يمكنك التواصل معنا من صفحة “تواصل” لجدولة استشارة.</p>

<button class="submit" onclick="window.print()">🖨️ طباعة الخطة</button>
"""

def main() -> str:
    return HTML
