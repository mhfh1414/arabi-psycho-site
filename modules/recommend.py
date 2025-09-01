# التوصيات بناءً على النتائج

def recommend_tests_from_case(case):
    """توصية باختبارات بناءً على الحالة"""
    if "حزن" in case or "اكتئاب" in case:
        return ["اختبار الاكتئاب", "اختبار القلق"]
    elif "توتر" in case or "قلق" in case:
        return ["اختبار القلق"]
    else:
        return ["اختبار الشخصية (الانطوائية/الانبساطية)"]
