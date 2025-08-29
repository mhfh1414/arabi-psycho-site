import os

DSM_DIR = "DSM5"  # مسار مجلد ملفات DSM5

for fn in os.listdir(DSM_DIR):
    if not fn.endswith(".py"):
        continue
    path = os.path.join(DSM_DIR, fn)

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    if not lines:
        continue

    # احذف أي سطر فيه كلمة coding (غالباً السطر الأول)
    new_lines = [l for l in lines if "coding" not in l.lower()]

    # اكتب الملف من جديد بعد التنظيف
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"✓ Cleaned {fn}")

print("✅ انتهى تنظيف جميع ملفات DSM5. الآن أعد تشغيل السيرفر.")
