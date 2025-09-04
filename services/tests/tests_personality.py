# ملف اختبارات الشخصية - tests_personality.py
# يقدّم اختبار شخصية بسيط مع نتائج مفسّرة

def personality_test(answers: list[str]) -> str:
    """
    يقيم شخصية العميل بناءً على الإجابات (نعم/لا أو Y/N).
    """
    score = 0
    for ans in answers:
        if ans.strip().lower() in ["نعم", "y", "yes"]:
            score += 1

    if score >= 7:
        return "شخصية قيادية: تحب السيطرة واتخاذ القرارات."
    elif score >= 4:
        return "شخصية متوازنة: تميل للتعاون وتحب المشاركة."
    else:
        return "شخصية هادئة: تفضل العزلة والتفكير قبل اتخاذ القرارات."
