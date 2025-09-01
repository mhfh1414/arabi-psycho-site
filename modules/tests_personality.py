# اختبارات الشخصية

PERS_TESTS = [
    {
        "id": "intro_extro",
        "name": "الانطوائية مقابل الانبساطية",
        "questions": [
            "هل تفضل قضاء الوقت بمفردك؟",
            "هل تشعر بالنشاط عند مقابلة أشخاص جدد؟",
            "هل تستمتع بالعمل الجماعي أكثر من الفردي؟",
        ],
        "options": ["نعم", "لا"]
    }
]

def score_personality(test_id, answers):
    """حساب نتيجة اختبار الشخصية"""
    test = next((t for t in PERS_TESTS if t["id"] == test_id), None)
    if not test:
        return {"error": "اختبار غير موجود"}

    score = sum(answers)
    return {"test": test["name"], "score": score}
