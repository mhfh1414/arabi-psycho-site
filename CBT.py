# -*- coding: utf-8 -*-
# CBT.py — نسخة موسّعة جدًا (تعليمي/إرشادي)
# أدوات: سجل أفكار متقدم، تنشيط سلوكي يومي/أسبوعي، سُلّم تعرّض،
# استبيان Beck المبسّط للقلق والاكتئاب (نسخة تعليمية مختصرة)،
# مقاييس تقدير ذاتي مبسطة، خطة علاج قابلة للطباعة، تمارين يقظة/تنفّس،
# دفاتر متابعة أسبوعية، ومكتبة "تشوّهات معرفية" مع اقتراحات تلقائية.

from typing import Dict, List, Any

class CBT:
    def __init__(self) -> None:
        # ===== سجل الأفكار (متقدم) =====
        self.سجل_الأفكار_حقول = [
            "الموقف",
            "الفكرة_الأوتوماتيكية",
            "الشعور_قبل (0-100)",
            "الأدلة_مع",
            "الأدلة_ضد",
            "التشوه_المعرفي",
            "الفكرة_المتوازنة",
            "السلوك/النتيجة",
            "الشعور_بعد (0-100)"
        ]

        # ===== قائمة تشوهات معرفية شائعة =====
        self.تشوهات_معرفية: Dict[str, str] = {
            "قراءة_أفكار": "أفترض أن الآخرين يفكرون سلبيًا تجاهي دون دليل.",
            "تعميم_مفرط": "نتيجة واحدة سلبية تعني أن كل شيء سيتكرر سلبًا.",
            "فلترة_سلبية": "أركز فقط على الجانب السلبي وأتجاهل الإيجابي.",
            "تفكير_قطبي": "كل شيء أبيض/أسود بلا درجات وسط.",
            "تهويل/تقليل": "أعظّم السلبي وأقلل من الإيجابي.",
            "واجبات/يجب": "أحكم على نفسي بعبارات (لازم/يجب) صارمة.",
            "تسمية": "أعطي نفسي/الآخرين تصنيفًا شاملًا من موقف واحد.",
            "تنبؤ_كارثي": "أتوقع أسوأ سيناريو دون أدلة كافية."
        }

        # ===== تمارين مساندة =====
        self.تمارين: Dict[str, List[str]] = {
            "تنفّس_هادئ (4-2-6)": ["استنشق 4", "احبس 2", "ازفر 6", "كرّر ×5"],
            "تأريض_حسي 5-4-3-2-1": ["5 مرئيات", "4 لمسات", "3 أصوات", "2 روائح", "1 طعم/نَفَس"],
            "يقظة_ذهنية (ملاحظة)": [
                "ركّز على التنفّس دقيقة",
                "سَمِّ الفكرة: 'مجرد فكرة'",
                "ارْجِع للحظة الحالية"
            ],
            "استرخاء_عضلي_تدريجي": [
                "شدّ عضلات القدم 5 ثوان ثم أرخِ",
                "اصعد للساقين ثم الفخذين ... حتى الكتفين/الوجه"
            ]
        }

        # ===== خطط اضطراب محددة =====
        self.خطط: Dict[str, Dict[str, Any]] = {
            "القلق": {
                "مكوّنات": ["تحديد محفزات", "سُلّم تعرّض", "إعادة تقييم", "تنفّس/استرخاء", "تتبّع تقدّم أسبوعي"],
                "أمثلة_تدرّج": ["سؤال موظف متجر", "مكالمة قصيرة", "عرض وجيز أمام 3 أشخاص", "موقف اجتماعي أكبر"]
            },
            "الاكتئاب": {
                "مكوّنات": ["تنشيط سلوكي يومي", "تحديد أفكار سلبية", "إعادة هيكلة", "روتين نوم/حركة/تغذية", "شبكة دعم"],
                "نشاطات_مقترحة": ["مشي 10-20 دقيقة", "اتصال بصديق", "قراءة 5 صفحات", "ترتيب ركن صغير"]
            },
            "الوسواس": {
                "مكوّنات": ["ERP (تعرّض + منع استجابة)", "إعادة تقييم الاحتمال/الخطورة", "تدريب تحمل القلق"],
                "أمثلة_ERP": ["تقليل فحص الباب", "امتناع عن سؤال الاطمئنان", "لمس محفّز مع منع الغسل"]
            }
        }

        # ===== تنشيط سلوكي =====
        self.تنشيط_سلوكي_حقول = ["التاريخ", "النشاط", "المتعة (0-10)", "القيمة (0-10)", "ملاحظات"]

        # ===== سُلّم تعرّض =====
        self.سلم_تعرّض_حقول = ["البند", "الدرجة_المتوقعة (0-10)", "خطوات_التدرّج", "النتيجة_بعد (0-10)"]

        # ===== دفاتر متابعة أسبوعية =====
        self.متابعة_أسبوعية_حقول = [
            "أهم_الأهداف_هذا_الأسبوع",
            "أفضل_شيء_تم",
            "تحدّي_واجهته",
            "مهارة_استخدمتها",
            "شيء_تود_تجربته_الأسبوع_القادم"
        ]

        # ===== استبيانات مبسطة (تعليمية) =====
        # Beck المبسّط: 7 بنود (0-3) للقلق + 7 للاكتئاب — إجمالي 0..21
        self.بيك_قلق_أسئلة = [
            "توتر/عصبية", "قلق مفرط", "صعوبة التهدئة", "أعراض جسدية (خفقان/تعرّق)", "قلق استباقي", "تجنّب بسبب القلق", "تأثير على الأداء"
        ]
        self.بيك_اكتئاب_أسئلة = [
            "مزاج منخفض", "فقد متعة", "تعب/بطء", "نوم مضطرب", "شعور بالذنب/قيمة ذاتية منخفضة", "صعوبات تركيز", "أفكار سلبية مستقبلية"
        ]

    # ===== اقتراح تلقائي للفكرة المتوازنة =====
    def اقترح_فكرة_متوازنة(self, فكرة: str, تشوه: str = "") -> str:
        if تشوه in self.تشوهات_معرفية:
            # اقتراح مخصص لكل تشوه
            mapping = {
                "قراءة_أفكار": "لا أقرأ عقول الآخرين؛ الأفضل أن أتحقق أو أقبل عدم اليقين.",
                "تعميم_مفرط": "موقف واحد لا يعني قاعدة عامة—لكل موقف ظروفه.",
                "فلترة_سلبية": "ما الدليل الإيجابي الذي أغفلته؟",
                "تفكير_قطبي": "هناك درجات وسط وحلول جزئية.",
                "تهويل/تقليل": "قَيِّم الاحتمال والنتيجة بواقعية، ثم ضع خطة.",
                "واجبات/يجب": "أبدّل (يجب) بـ (أفضل/أسعى) لتخفيف الضغط.",
                "تسمية": "أصف السلوك بدلاً من وصم الذات كلها.",
                "تنبؤ_كارثي": "جرّب تنبؤًا بديلًا وخطة احتياط."
            }
            return mapping.get(تشوه, "جَرِّب تفسيرًا بديلاً واقعيًا.")
        # إن لم يُذكر التشوه صراحةً
        txt = (فكرة or "")
        if "كارث" in txt or "مصيب" in txt:
            return "الموقف مزعج لكنه قابل للإدارة بخطوات صغيرة وخطة بديلة."
        if "فاشل" in txt:
            return "أخطاء الماضي لا تُلغي قدراتي—أستطيع التحسّن بالتدريب."
        if "لن أتحمل" in txt:
            return "صعب لكن يمكن تقسيمه وطلب دعم لتخفيف الحمل."
        return "ما الدليل مع وضد؟ ما البدائل؟ ما الأكثر احتمالًا؟"

    # ===== HTML للنماذج والنتائج =====
    def _safe(self, s: str) -> str:
        return (s or "").replace("<", "&lt;").replace(">", "&gt;")

    def html_نموذج_سجل_أفكار(self) -> str:
        inputs = []
        for name in self.سجل_الأفكار_حقول:
            tag = "textarea"
            rows = 2 if "الموقف" not in name and "السلوك" not in name else 3
            inputs.append(f"<label>{name}</label><{tag} name='{name}' rows='{rows}' style='width:100%'></{tag}>")
        # قائمة التشوّهات
        options = "".join([f"<option value='{k}'>{k}</option>" for k in [""] + list(self.تشوهات_معرفية.keys())])
        inputs.insert(5, f"<label>التشوه_المعرفي (اختياري)</label><select name='التشوه_المعرفي'>{options}</select>")
        return f"""
        <form method="post" action="/cbt/thought-record">
            {' '.join(inputs)}
            <button type="submit">عرض النتيجة/طباعة</button>
        </form>
        """

    def html_عرض_سجل(self, سجل: Dict[str, str]) -> str:
        rows = []
        for k, v in سجل.items():
            rows.append(f"<tr><th style='text-align:right'>{k}</th><td>{self._safe(v)}</td></tr>")
        اقتراح = self.اقترح_فكرة_متوازنة(
            سجل.get("الفكرة_الأوتوماتيكية",""),
            سجل.get("التشوه_المعرفي","")
        )
        rows.append(f"<tr><th style='text-align:right'>اقتراح تلقائي</th><td>{self._safe(اقتراح)}</td></tr>")
        return "<table class='table'>%s</table>" % "".join(rows)

    def html_خطة(self, نوع: str) -> str:
        خطة = self.خطط.get(نوع, {})
        if not خطة:
            return "<p>الخطة غير متاحة.</p>"
        parts = [f"<h2>خطة {نوع}</h2>"]
        for section in ("مكوّنات", "أمثلة_تدرّج", "نشاطات_مقترحة"):
            if section in خطة:
                items = "".join([f"<li>{x}</li>" for x in خطة[section]])
                title = "المكوّنات" if section == "مكوّنات" else ("أمثلة تدرّج" if section == "أمثلة_تدرّج" else "نشاطات مقترحة")
                parts.append(f"<h3>{title}</h3><ul>{items}</ul>")
        parts.append("<p class='note'>محتوى تثقيفي—استشر مختصًا عند الحاجة.</p>")
        return "\n".join(parts)

    def html_نموذج_تنشيط(self) -> str:
        inputs = [f"<label>{n}</label><input name='{n}'/>" for n in self.تنشيط_سلوكي_حقول]
        return f"<form method='post' action='/cbt/activation'>{' '.join(inputs)}<button type='submit'>إضافة/عرض</button></form>"

    def html_عرض_تنشيط(self, صف: Dict[str, str]) -> str:
        cells = "".join([f"<tr><th>{k}</th><td>{self._safe(v)}</td></tr>" for k, v in صف.items()])
        return "<table class='table'>%s</table>" % cells

    def html_نموذج_سلم_تعرّض(self) -> str:
        inputs = []
        for n in self.سلم_تعرّض_حقول:
            tag = "textarea" if "خطوات" in n else "input"
            field = f"<textarea name='{n}' style='width:100%'></textarea>" if tag == "textarea" else f"<input name='{n}' style='width:100%'/>"
            inputs.append(f"<label>{n}</label>{field}")
        return f"<form method='post' action='/cbt/exposure'>{' '.join(inputs)}<button type='submit'>إضافة/عرض</button></form>"

    def html_عرض_سلم(self, بند: Dict[str, str]) -> str:
        cells = "".join([f"<tr><th>{k}</th><td>{self._safe(v)}</td></tr>" for k, v in بند.items()])
        return "<table class='table'>%s</table>" % cells

    # ===== استبيانات Beck المبسّطة / تقدير ذاتي =====
    def html_بيك_نموذج(self, نوع: str) -> str:
        if نوع == "قلق":
            أسئلة = self.بيك_قلق_أسئلة
            action = "/cbt/beck/anx"
        else:
            أسئلة = self.بيك_اكتئاب_أسئلة
            action = "/cbt/beck/dep"
        options = "<option value='0'>0: لا</option><option value='1'>1: خفيف</option><option value='2'>2: متوسط</option><option value='3'>3: مرتفع</option>"
        ins = [f"<label>{i}) {q}</label><select name='q{i}'>{options}</select>" for i, q in enumerate(أسئلة, 1)]
        return f"<form method='post' action='{action}'>{' '.join(ins)}<button type='submit'>احسب النتيجة</button></form>"

    def html_بيك_عرض(self, مجموع: int, نوع: str) -> str:
        # تفسير مبسّط تعليمي
        if مجموع <= 4: تفسير = "منخفض"
        elif مجموع <= 9: تفسير = "خفيف"
        elif مجموع <= 14: تفسير = "متوسط"
        else: تفسير = "مرتفع"
        return f"<p><b>استبيان Beck ({نوع}) — نتيجة:</b> {مجموع}/21 — {تفسير} (تثقيفي)</p>"

    # ===== متابعة أسبوعية =====
    def html_نموذج_متابعة(self) -> str:
        inputs = [f"<label>{n}</label><textarea name='{n}' rows='2' style='width:100%'></textarea>" for n in self.متابعة_أسبوعية_حقول]
        return f"<form method='post' action='/cbt/weekly'>{' '.join(inputs)}<button type='submit'>حفظ/عرض</button></form>"

    def html_عرض_متابعة(self, صف: Dict[str, str]) -> str:
        cells = "".join([f"<tr><th>{k}</th><td>{self._safe(v)}</td></tr>" for k, v in صف.items()])
        return "<table class='table'>%s</table>" % cells

    # ===== قالب خطة علاج عامة =====
    def html_قالب_خطة_علاج(self) -> str:
        حقول = ["الأهداف_العامة", "أهداف_قصيرة", "العوائق", "الاستراتيجيات", "الدعم_المتوفر", "خطة_طارئة", "مؤشرات_التقدم"]
        inputs = [f"<label>{h}</label><textarea name='{h}' rows='2' style='width:100%'></textarea>" for h in حقول]
        return f"<form method='post' action='/cbt/plan'>{' '.join(inputs)}<button type='submit'>عرض/طباعة</button></form>"

    def html_عرض_خطة(self, بيانات: Dict[str, str]) -> str:
        rows = "".join([f"<tr><th>{k}</th><td>{self._safe(v)}</td></tr>" for k, v in بيانات.items()])
        return "<table class='table'>%s</table>" % rows
