"""
DSM-5 Index Loader (Arabic)
ملف: dsm_index.py
"""

import importlib.util
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DSM_DIR = os.path.join(BASE_DIR, "DSM5")

# الحزم (كل مجموعة ملفات DSM في باك واحد)
DSM_PACKAGES = [
    "DSM5.DSM_01",   # ملف 01_anxiety_disorders.py
    "DSM5.DSM_A",    # الملفات من 02 إلى 05
    "DSM5.DSM_B",    # الملفات من 06 إلى 09
    "DSM5.DSM_C",    # الملفات من 11 إلى 14
    "DSM5.DSM_D",    # الملفات من 15 إلى 19
]

# القاموس الرئيسي
ALL_DISORDERS = {}

def load_module_from_path(module_name, path):
    """تحميل ملف بايثون كـ module"""
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None:
        raise ImportError(f"تعذر إيجاد الملف {path}")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)  # type: ignore
    return mod

def load_all():
    """تحميل جميع الحزم المضافة في DSM_PACKAGES"""
    for package in DSM_PACKAGES:
        try:
            module = importlib.import_module(package)
            if hasattr(module, "DISORDERS"):
                ALL_DISORDERS.update(module.DISORDERS)
            else:
                print(f"⚠️ الحزمة {package} لا تحتوي DISORDERS")
        except Exception as e:
            print(f"❌ خطأ في تحميل {package}: {e}")

def get_disorder(name: str):
    """إرجاع اضطراب معين بالاسم"""
    return ALL_DISORDERS.get(name)

def list_disorders():
    """إرجاع قائمة بجميع الاضطرابات"""
    return list(ALL_DISORDERS.keys())
