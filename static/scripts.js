document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ موقع عربي سايكو شغال");

    // تأكيد قبل إرسال دراسة الحالة
    const caseForm = document.querySelector("#case-form");
    if (caseForm) {
        caseForm.addEventListener("submit", function (e) {
            if (!confirm("هل أنت متأكد من حفظ دراسة الحالة؟")) {
                e.preventDefault();
            }
        });
    }
});
