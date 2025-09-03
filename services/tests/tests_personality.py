
# دوال شخصية (BIG5 مبسطة) — للتشغيل الفوري بدون تبعيات

def score_big5(answers):
    """
    يحسب نتائج مبسطة لعوامل BIG5.
    :param answers: dict مثل:
        {
          "O": [1,0,1,1],  # Openness
          "C": [0,1,1,1],  # Conscientiousness
          "E": [1,1,0,1],  # Extraversion
          "A": [1,1,1,0],  # Agreeableness
          "N": [0,1,0,0],  # Neuroticism (تعكس للهدوء)
        }
      كل عنصر 0 أو 1 لسهولة التشغيل
    :return: dict بدرجات 0..100 لكل عامل
    """
    if not isinstance(answers, dict):
        return {"status": "error", "message": "answers يجب أن تكون dict"}

    def pct(lst):
        total = max(len(lst), 1)
        return int(100 * sum(int(bool(x)) for x in lst) / total)

    result = {
        "Openness": pct(answers.get("O", [])),
        "Conscientiousness": pct(answers.get("C", [])),
        "Extraversion": pct(answers.get("E", [])),
        "Agreeableness": pct(answers.get("A", [])),
        "Neuroticism": pct(answers.get("N", [])),  # نسبة أعلى = عُصابية أعلى
    }
    return {"status": "ok", "scores": result}
