// scripts.js - عربي سايكو

document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ موقع عربي سايكو شغال بنجاح");

    // 📋 تأكيد قبل إرسال دراسة الحالة
    const caseForm = document.querySelector("#case-form");
    if (caseForm) {
        caseForm.addEventListener("submit", function (e) {
            if (!confirm("هل أنت متأكد من حفظ دراسة الحالة؟")) {
                e.preventDefault();
            }
        });
    }

    // 🔔 إخفاء رسائل التنبيه (Flash messages) بعد 5 ثوانٍ
    const flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = "0";
            setTimeout(() => msg.remove(), 600);
        }, 5000);
    });

    // 📝 تمييز السؤال الحالي في صفحة الاختبار
    const questions = document.querySelectorAll(".test-question");
    questions.forEach(q => {
        q.addEventListener("click", () => {
            questions.forEach(el => el.classList.remove("active"));
            q.classList.add("active");
        });
    });
});
