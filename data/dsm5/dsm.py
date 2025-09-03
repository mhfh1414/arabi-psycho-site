# data/dsm5/dsm.py
# وحدة مبسطة تحتوي على قائمة اضطرابات DSM-5 ودوال مساعدة

DSM5_DISORDERS = [
    {"id": 1, "name": "الاكتئاب", "desc": "اضطراب مزاجي يتميز بالحزن المستمر وفقدان الاهتمام."},
    {"id": 2, "name": "القلق العام", "desc": "قلق مفرط وصعوبة في التحكم في التوتر."},
    {"id": 3, "name": "اضطراب ثنائي القطب", "desc": "نوبات متناوبة من الهوس والاكتئاب."},
]

def list_disorders():
    """إرجاع قائمة الاضطرابات النفسية"""
    return DSM5_DISORDERS

def get_disorder(disorder_id: int):
    """إرجاع اضطراب واحد حسب الرقم"""
    for disorder in DSM5_DISORDERS:
        if disorder["id"] == disorder_id:
            return disorder
    return None
