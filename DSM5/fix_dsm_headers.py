# -*- coding: utf-8 -*-
"""
Remove the first 'coding:' line from all DSM5/*.py to avoid syntax/annotation issues.
- يحذف سطر الترميز من بداية الملف إن وُجد (أي سطر يحتوي على 'coding')
- يزيل BOM إن وُجد
- يجرّب استيراد كل ملف للتأكد أن الأمور تمام
"""

import os, io, re, importlib.util, sys

ROOT = os.path.dirname(__file__)
DSM_DIR = os.path.join(ROOT, "DSM5")

coding_re = re.compile(r"^\s*#.*coding\s*:\s*utf-?8", re.I)

def clean_one(path: str) -> bool:
    """يحذف سطر الترميز الأول إن وُجد. يرجّع True إذا تعدّل الملف."""
    with io.open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        lines = f.readlines()

    if not lines:
        return False

    changed = False

    # إزالة BOM إن وُجد في أول سطر
    if lines[0].startswith("\ufeff"):
        lines[0] = lines[0].lstrip("\ufeff")
        changed = True

    # لو أول سطر تعليق فيه كلمة coding → احذفه
    if coding_re.match(lines[0]):
        lines.pop(0)
        changed = True

    if changed:
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(lines)

    return changed

def import_test(path: str):
    """تأكد أن الملف يُستورد بدون أخطاء بايثون."""
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

    print(f"🔧 تنظيف ملفات داخل: {DSM_DIR}\n")
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
