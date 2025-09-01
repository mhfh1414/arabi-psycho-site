from __future__ import annotations

# اختبارات شخصية (مثال مبسّط Big Five قصير)
PERS_TESTS = {
    "bfi10": {
        "title": "BFI-10 (العوامل الخمسة المختصر)",
        "scale": {1:"لا أوافق إطلاقًا",2:"لا أوافق",3:"محايد",4:"أوافق",5:"أوافق جدًا"},
        "items": [{"id": i+1, "text": f"عبارة شخصية {i+1}"} for i in range(10)],
        "domains": ["الانبساط", "القبول", "الضمير", "العصابية", "الانفتاح"]
    }
}

def score_personality(test_key: str, answers: dict) -> dict:
    test = PERS_TESTS.get(test_key)
    if not test:
        return {"total": 0, "profile": {}}
    total = sum(int(answers.get(i["id"], 0)) for i in test["items"])
    # توزيع صوري: كل مجال = مجموع بندين
    profile = {}
    for idx, dom in enumerate(test["domains"]):
        a = int(answers.get(idx*2+1, 0))
        b = int(answers.get(idx*2+2, 0))
        profile[dom] = a + b
    return {"total": total, "profile": profile}
