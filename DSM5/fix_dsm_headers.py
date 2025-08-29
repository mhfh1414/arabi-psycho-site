# -*- coding: utf-8 -*-
"""
يصلّح السطر الأول في جميع ملفات DSM5/*.py
- يضمن أن أول سطر يساوي:  # -*- coding: utf-8 -*-
- يزيل أي محارف غريبة (BOM) أو صيغ خاطئة (-- coding: utf-8 --، أو بدون #)
- يعطيك تقرير بالملفات المعدّلة، ويحاول يستورد كل ملف للتأكد أنه صار سليم
"""

import os, io, re, importlib.util, sys

ROOT = os.path.dirname(__file__)
DSM_DIR = os.path.join(ROOT, "DSM5")
HEADER = "# -*- coding: utf-8 -*-\n"

bad_header_re = re.compile(
    r"""^\s*(#\s*)?[-–—]*\s*\*?-?\*\s*coding\s*:\s*utf-?8\s*\*?-?\*\s*[-–—]*\s*$""",
    re.IGNORECASE,
)

def fix_one(path: str) -> bool:
    """يعيد كتابة أول سطر لو كان خاطئ أو مفقود. يرجّع True إذا تم تعديل الملف."""
    with io.open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        lines = f.readlines()

    if not lines:
        return False

    changed = False
    first = lines[0].rstrip("\r\n")

    # 1) لو أول سطر يشبه تعليمة الترميز لكن بصيغة غلط → نستبدله بالشكل الصحيح
    if bad_header_re.match(first):
        if first != HEADER.strip():
            lines[0] = HEADER
            changed = True
    # 2) لو أول سطر يبدأ بـ "-*-" أو "coding" بدون "#" → حوّله لتعليق صحيح
    elif first.strip().lower().startswith(("-*-", "coding", "–", "—", "--")):
        lines[0] = HEADER
        changed = True
    # 3) لو مافيه تعليمة ترميز في أول سطر → أضفها أعلى الملف
    elif "coding" not in first.lower():
        lines.insert(0, HEADER)
        changed = True

    # إزالة أي BOM متبقّي
    if lines[0].startswith("\ufeff"):
        lines[0] = lines[0].lstrip("\ufeff")
        changed = True

    if changed:
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(lines)

    return changed

def import_test(path: str):
    """يتأكد أن الملف صار يتستورد بدون SyntaxError."""
    name = os.path.splitext(os.path.basename(path))[0]
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore
    spec.loader.exec_module(mod)  # type: ignore

def main():
    if not os.path.isdir(DSM_DIR):
        print("⚠️ لم يتم العثور على مجلد DSM5/ بجانب هذا السكربت.", file=sys.stderr)
        sys.exit(1)

    total = 0
    modified = 0
    failed = []

    print(f"🔧 بدء الإصلاح داخل: {DSM_DIR}\n")
    for fn in sorted(os.listdir(DSM_DIR)):
        if not fn.endswith(".py"):
            continue
        total += 1
        path = os.path.join(DSM_DIR, fn)
        changed = fix_one(path)
        try:
            import_test(path)
            status = "✓ OK"
        except Exception as e:
            status = "✗ FAIL"
            failed.append((fn, str(e)))
        mod_flag = " (edited)" if changed else ""
        print(f"{status}  {fn}{mod_flag}")

    print(f"\n📦 الملفات: {total}  | ✍️ تم تعديل: {modified}  | ❌ فشل: {len(failed)}")
    if failed:
        print("\nتفاصيل الأخطاء:")
        for fn, msg in failed:
            print(f"- {fn}: {msg}")
        sys.exit(2)

if __name__ == "__main__":
    main()
