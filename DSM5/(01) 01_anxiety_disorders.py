import os, importlib.util, types

DSM_DIR = os.path.join(os.path.dirname(__file__), "DSM5")
REGISTRY = {}
CATEGORIES_META = {}

def _load_module_from_path(path: str) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(os.path.basename(path), path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)  # type: ignore
    return mod

def _expected_name_from_filename(fn: str) -> str:
    """يرجع اسم المتغيّر القديم المتوقع من اسم الملف: 01_anxiety_disorders.py -> ANXIETY_DISORDERS"""
    name_no_ext = os.path.splitext(fn)[0]
    # احذف الرقم والبروفكس (01_) إن وجد
    parts = name_no_ext.split("_", 1)
    base = parts[1] if parts and parts[0].isdigit() and len(parts[0]) <= 3 else name_no_ext
    # مثال: anxiety_disorders -> ANXIETY_DISORDERS
    return base.upper()

def load_all() -> None:
    REGISTRY.clear(); CATEGORIES_META.clear()

    for fn in sorted(os.listdir(DSM_DIR)):
        if not fn.endswith(".py") or fn == "__init__.py":
            continue
        path = os.path.join(DSM_DIR, fn)
        mod = _load_module_from_path(path)

        # 1) جرّب الواجهة الجديدة (CATEGORY / LABEL_AR / DATA)
        category = getattr(mod, "CATEGORY", None)
        data = getattr(mod, "DATA", None)
        label = getattr(mod, "LABEL_AR", None)

        # 2) لو غير موجودة، جرّب الواجهة القديمة: <NAME>_DISORDERS
        if data is None:
            expected = _expected_name_from_filename(fn)  # e.g. ANXIETY_DISORDERS
            # بعض الملفات القديمة كانت تضيف لاحقة _DISORDERS
            for cand in (expected + "_DISORDERS", expected):
                if hasattr(mod, cand):
                    data = getattr(mod, cand)
                    # اشتق التصنيف من الاسم الأساسي
                    category = expected.lower()
                    if category.endswith("_disorders"):
                        category = category[:-10]  # احذف _disorders من النهاية
                    label = label or category
                    break

        if not isinstance(data, dict) and not isinstance(data, list):
            raise AttributeError(f"({fn}) لا يحتوي بنية بيانات معروفة (DATA أو *_DISORDERS)")

        # توحيد الشكل: إذا كانت قائمة قديمة، لفّها داخل dict بمفتاح 'items'
        if isinstance(data, list):
            data = {"items": data}

        # تأكيد category/label
        if not category:
            category = _expected_name_from_filename(fn).lower().replace("_disorders", "")
        if not label:
            label = category

        REGISTRY[category] = data
        CATEGORIES_META[category] = {"label_ar": label, "file": fn}

def categories():
    return [(k, CATEGORIES_META[k]["label_ar"], len(REGISTRY[k])) for k in REGISTRY]

def get_category(cat):
    return REGISTRY.get(cat, {})

def get_disorder(cat, key):
    block = REGISTRY.get(cat, {})
    # يدعم الصيغتين: dict بالمفاتيح أو dict فيه 'items' قائمة
    if "items" in block and isinstance(block["items"], list):
        for it in block["items"]:
            if it.get("id") == key:
                return it
        return None
    return block.get(key)
