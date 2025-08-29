# -*- coding: utf-8 -*-
"""
Fix/remove broken 'coding: utf-8' headers in DSM5/*.py
- يحذف أي سطر ترميز في أول سطرين، سواء كان مع # أو بدونه أو بشرطات غريبة
- يزيل BOM إن وُجد
- يختبر الاستيراد لكل ملف بعد الإصلاح
"""

import os, io, re, importlib.util, sys

ROOT = os.path.dirname(__file__)
DSM_DIR = os.path.join(ROOT, "DSM5")

# يطابق كل الأشكال الممكنة لسطر الترميز (مع # أو بدونه)
coding_any_re = re.compile(r"""
    ^\s*              # مسافات بالبداية
    (?:\#\s*)?        # اختيارياً #
    (?:-+\*-\s*)?     # اختيارياً -*- ببعض التحريفات
    (?:coding)        # كلمة coding
    \s*:\s*
    utf-?8            # utf-8 أو utf8
    (?:\s*\*-\-)?     # اختيارياً -*- بنهاية السطر
    \s*$
""", re.IGNORECASE | re.VERBOSE)

def clean_one(path: str) -> bool:
    with io.open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        lines = f.readlines()

    if not lines:
        return False

    changed = False

    # أزل BOM من أول سطر إن وُجد
    if lines[0].startswith("\ufeff"):
        lines[0] = lines[0].lstrip("\ufeff")
        changed = True

    # افحص أول سطرين: إذا أي واحد يحتوي تعليمة ترميز بأي شكل -> احذفه
    to_delete = []
    for i in range(min(2, len(lines))):
        if coding_any_re.match(lines[i]):
            to_delete.append(i)
    if to_delete:
        # احذف من الأخير للأول حتى لا تتغير الفهارس
        for i in reversed(to_delete):
            del lines[i]
        changed = True

    if changed:
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(lines)

    return changed

def import_test(path: str):
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(mod)  # type: ignore

def main():
    if not os.path.isdir(DSM_DIR):
        print("⚠️ لم يتم العثور على مجلد DSM5/ بجانب هذا السكربت.", file=sys.stderr)
        sys.exit(1)

    total = 0
    edited = 0
    failed = []

    print(f"🔧 تنظيف داخل: {DSM_DIR}\n")
    for fn in sorted(os.listdir(DSM_DIR)):
        if not fn.endswith(".py"):
            continue
        total += 1
        path = os.path.join(DSM_DIR, fn)
        try:
            if clean_one(path):
                edited += 1
            import_test(path)
            print(f"✓ OK   {fn}")
        except Exception as e:
            failed.append((fn, str(e)))
            print(f"✗ FAIL {fn} -> {e}")

    print(f"\n📦 الملفات: {total} | ✍️ تم تعديل: {edited} | ❌ فشل: {len(failed)}")
    if failed:
        print("\nتفاصيل الأخطاء:")
        for fn, msg in failed:
            print(f"- {fn}: {msg}")
        sys.exit(2)

if __name__ == "__main__":
    main()
