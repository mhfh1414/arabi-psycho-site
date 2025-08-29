import os

# نحدد المسارات المحتملة لمجلد DSM5
possible_dirs = ["DSM5", os.path.join("src", "DSM5")]

target_dir = None
for d in possible_dirs:
    if os.path.isdir(d):
        target_dir = d
        break

if not target_dir:
    print("❌ لم يتم العثور على مجلد DSM5")
    exit(1)

print(f"🔧 جاري تعديل الملفات داخل: {target_dir}")

for fn in os.listdir(target_dir):
    if not fn.endswith(".py"):
        continue
    path = os.path.join(target_dir, fn)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    if not lines:
        continue
    # حذف أول سطر
    lines = lines[1:]
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"✓ تم تعديل: {fn}")

print("✅ انتهى التعديل، الآن جرّب تشغيل السيرفر من جديد.")
