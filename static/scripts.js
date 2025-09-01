// scripts.js
// أكواد بسيطة لدعم الواجهة والتعامل مع الفورمات

// تأكيد قبل إرسال دراسة الحالة
document.addEventListener("DOMContentLoaded", () => {
  const caseForm = document.querySelector("form#caseForm");
  if (caseForm) {
    caseForm.addEventListener("submit", (e) => {
      const confirmSend = confirm("هل أنت متأكد من إرسال دراسة الحالة؟");
      if (!confirmSend) {
        e.preventDefault();
      }
    });
  }

  // تحسين تجربة أزرار الاختبارات
  const testForms = document.querySelectorAll("form.testForm");
  testForms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      const unanswered = form.querySelectorAll("input[type='radio']:not(:checked)");
      if (unanswered.length > 0) {
        const ok = confirm("بعض الأسئلة لم تُجب عليها، هل تريد المتابعة؟");
        if (!ok) e.preventDefault();
      }
    });
  });

  // إشعار بسيط عند تحميل الصفحة
  console.log("✅ تم تحميل الواجهة - عربي سايكو يعمل الآن");
});
