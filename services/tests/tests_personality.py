# اختبارات شخصية بسيطة (تجريبية)

def personality_test(user_answers=None):
    """
    اختبار شخصية تجريبي
    :param user_answers: قائمة اجابات مثل ["A", "B", "C"]
    :return: dict يحتوي score ورسالة
    """
    if not user_answers:
        return {"status": "ok", "score": 0, "message": "لم تدخل إجابات"}

    # نحسب النقاط بناءً على عدد الإجابات
    score = len(user_answers)

    # نص بسيط يوضح النتيجة
    if score <= 3:
        message = "شخصية هادئة ومتحفظة"
    elif score <= 6:
        message = "شخصية متوازنة واجتماعية"
    else:
        message = "شخصية قيادية ونشيطة"

    return {"status": "ok", "score": score, "message": message}


def personality_info():
    """معلومات/وصف مختصر للاختبار"""
    return "هذا مجرد اختبار شخصية تجريبي (tests_personality)."
