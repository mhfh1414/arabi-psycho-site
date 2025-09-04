def recommend_by_score(score: int):
    if score <= 1:
        return "نتيجتك منخفضة: راقب الأعراض فقط."
    if score <= 3:
        return "نتيجتك متوسطة: جرّب تمارين CBT أولية."
    return "نتيجتك مرتفعة: يُفضّل استشارة متخصص."
