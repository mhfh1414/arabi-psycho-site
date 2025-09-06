<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <title>عربي سايكو | المركز العربي للصحة النفسية</title>
  <meta name="description" content="مركز عربي سايكو للصحة النفسية - نقدم خدمات التشخيص، العلاج السلوكي المعرفي، وعلاج الإدمان بأعلى معايير الجودة">
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    :root {
      --primary-blue: #0a3a75;
      --secondary-blue: #0a65b0;
      --dark-blue: #0a1330;
      --gold: #f4b400;
      --light-gold: #ffd86a;
      --light-blue: #cfe0ff;
      --white: #ffffff;
      --glass: rgba(255, 255, 255, 0.08);
      --glass-border: rgba(255, 255, 255, 0.12);
      --transition: all 0.3s ease;
    }
    
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: 'Tajawal', sans-serif;
      background: linear-gradient(135deg, var(--primary-blue), var(--secondary-blue));
      color: var(--white);
      line-height: 1.6;
      overflow-x: hidden;
      background-attachment: fixed;
    }
    
    .container {
      max-width: 1280px;
      margin: 0 auto;
      padding: 0 20px;
    }
    
    /* تحسين الهيدر */
    header {
      position: sticky;
      top: 0;
      z-index: 1000;
      backdrop-filter: blur(10px);
      background: rgba(7, 19, 56, 0.7);
      padding: 15px 0;
      border-bottom: 1px solid var(--glass-border);
    }
    
    .header-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .logo {
      display: flex;
      align-items: center;
      gap: 15px;
    }
    
    .logo-icon {
      width: 60px;
      height: 60px;
      border-radius: 15px;
      background: linear-gradient(145deg, var(--dark-blue), var(--primary-blue));
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 24px;
      color: var(--gold);
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
      border: 1px solid var(--glass-border);
    }
    
    .logo-text h1 {
      font-size: 28px;
      margin-bottom: 5px;
      background: linear-gradient(to right, var(--light-gold), var(--gold));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    
    .logo-text p {
      font-size: 14px;
      color: var(--light-blue);
      margin: 0;
    }
    
    /* تحسين قائمة التنقل */
    .nav-links {
      display: flex;
      gap: 10px;
    }
    
    .nav-link {
      display: flex;
      align-items: center;
      gap: 8px;
      text-decoration: none;
      color: var(--white);
      padding: 10px 18px;
      border-radius: 12px;
      background: var(--glass);
      border: 1px solid var(--glass-border);
      transition: var(--transition);
      font-weight: 500;
    }
    
    .nav-link:hover {
      background: rgba(255, 255, 255, 0.15);
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    .nav-link i {
      font-size: 18px;
    }
    
    /* تحسين قسم الهيرو */
    .hero {
      padding: 60px 0;
      text-align: center;
    }
    
    .hero-content {
      max-width: 800px;
      margin: 0 auto;
    }
    
    .hero h2 {
      font-size: 2.8rem;
      margin-bottom: 20px;
      line-height: 1.3;
    }
    
    .hero p {
      font-size: 1.2rem;
      color: var(--light-blue);
      margin-bottom: 40px;
      max-width: 600px;
      margin-left: auto;
      margin-right: auto;
    }
    
    .cta-buttons {
      display: flex;
      justify-content: center;
      gap: 20px;
      flex-wrap: wrap;
    }
    
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      font-weight: 700;
      padding: 16px 28px;
      border-radius: 14px;
      transition: var(--transition);
      font-size: 1.1rem;
    }
    
    .btn-primary {
      background: linear-gradient(145deg, var(--light-gold), var(--gold));
      color: #2b1b02;
      box-shadow: 0 6px 20px rgba(244, 180, 0, 0.3);
    }
    
    .btn-primary:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 25px rgba(244, 180, 0, 0.4);
    }
    
    .btn-secondary {
      background: linear-gradient(145deg, #9cc5ff, #63a4ff);
      color: #04122c;
      box-shadow: 0 6px 20px rgba(60, 130, 255, 0.3);
    }
    
    .btn-secondary:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 25px rgba(60, 130, 255, 0.4);
    }
    
    /* تحسين البطاقات */
    .features {
      padding: 60px 0;
    }
    
    .section-title {
      text-align: center;
      font-size: 2.2rem;
      margin-bottom: 50px;
      position: relative;
      padding-bottom: 15px;
    }
    
    .section-title:after {
      content: '';
      position: absolute;
      bottom: 0;
      right: 50%;
      transform: translateX(50%);
      width: 80px;
      height: 4px;
      background: linear-gradient(to right, var(--light-gold), var(--gold));
      border-radius: 2px;
    }
    
    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 25px;
    }
    
    .card {
      background: var(--glass);
      border: 1px solid var(--glass-border);
      border-radius: 18px;
      padding: 25px;
      backdrop-filter: blur(6px);
      transition: var(--transition);
      height: 100%;
      display: flex;
      flex-direction: column;
    }
    
    .card:hover {
      transform: translateY(-5px);
      box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
      border-color: rgba(255, 255, 255, 0.2);
    }
    
    .card-icon {
      font-size: 2.5rem;
      margin-bottom: 20px;
      color: var(--gold);
    }
    
    .card h3 {
      font-size: 1.5rem;
      margin-bottom: 15px;
    }
    
    .card p {
      color: var(--light-blue);
      margin-bottom: 20px;
      flex-grow: 1;
    }
    
    .card .btn {
      align-self: flex-start;
      margin-top: auto;
    }
    
    /* قسم الخدمات */
    .services {
      padding: 60px 0;
      background: rgba(0, 0, 0, 0.1);
      border-radius: 30px;
      margin: 40px 0;
    }
    
    /* الفوتر */
    footer {
      background: rgba(7, 19, 56, 0.8);
      padding: 40px 0 20px;
      margin-top: 60px;
      border-top: 1px solid var(--glass-border);
    }
    
    .footer-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;
    }
    
    .copyright {
      color: var(--light-blue);
    }
    
    .design-credit {
      color: var(--light-blue);
      font-size: 0.9rem;
    }
    
    /* تأثيرات للعناصر */
    .floating {
      animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
      0% { transform: translateY(0px); }
      50% { transform: translateY(-10px); }
      100% { transform: translateY(0px); }
    }
    
    /* responsiveness */
    @media (max-width: 768px) {
      .header-content {
        flex-direction: column;
        gap: 20px;
      }
      
      .nav-links {
        flex-wrap: wrap;
        justify-content: center;
      }
      
      .hero h2 {
        font-size: 2rem;
      }
      
      .hero p {
        font-size: 1rem;
      }
      
      .cta-buttons {
        flex-direction: column;
        align-items: center;
      }
      
      .footer-content {
        flex-direction: column;
        text-align: center;
      }
    }
  </style>
</head>
<body>
  <header>
    <div class="container">
      <div class="header-content">
        <div class="logo">
          <div class="logo-icon">AS</div>
          <div class="logo-text">
            <h1>عربي سايكو</h1>
            <p>المركز العربي للصحة النفسية</p>
          </div>
        </div>
        
        <nav class="nav-links">
          <a href="{{ url_for('contact_whatsapp') }}" class="nav-link">
            <i class="fab fa-whatsapp"></i>
            <span>واتساب</span>
          </a>
          <a href="{{ url_for('contact_telegram') }}" class="nav-link">
            <i class="fab fa-telegram"></i>
            <span>تلجرام</span>
          </a>
          <a href="{{ url_for('contact_email') }}" class="nav-link">
            <i class="far fa-envelope"></i>
            <span>إيميل</span>
          </a>
        </nav>
      </div>
    </div>
  </header>

  <main>
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <h2>رعاية نفسية متكاملة <br>بمعايير عالمية وبلغة عربية</h2>
          <p>نقدم خدمات التشخيص الدقيق، العلاج السلوكي المعرفي، وبرامج علاج الإدمان بأعلى معايير الجودة والسرية</p>
          
          <div class="cta-buttons">
            <a href="{{ url_for('dsm') }}" class="btn btn-primary">
              <i class="fas fa-book-medical"></i>
              ابدأ التشخيص الآن
            </a>
            <a href="{{ url_for('contact_whatsapp') }}" class="btn btn-secondary">
              <i class="fas fa-headset"></i>
              احجز استشارة
            </a>
          </div>
        </div>
      </div>
    </section>

    <section class="features">
      <div class="container">
        <h2 class="section-title">خدماتنا المتخصصة</h2>
        
        <div class="cards-grid">
          <div class="card floating">
            <div class="card-icon">📖</div>
            <h3>التشخيص وفق DSM-5</h3>
            <p>نظام متكامل للتشخيص الدقيق وفق الدليل التشخيصي والإحصائي للاضطرابات النفسية، مع تحليل شامل للحالة وتقديم تقرير مفصل.</p>
            <a href="{{ url_for('dsm') }}" class="btn btn-primary">ابدأ التشخيص</a>
          </div>
          
          <div class="card floating" style="animation-delay: 0.5s;">
            <div class="card-icon">🧠</div>
            <h3>العلاج السلوكي المعرفي</h3>
            <p>برامج علاجية متكاملة تشمل الاختبارات النفسية المعتمدة (PHQ-9, GAD-7, PCL-5) وتقنيات CBT المبنية على الأدلة العلمية.</p>
            <a href="{{ url_for('cbt') }}" class="btn btn-primary">اكتشف المزيد</a>
          </div>
          
          <div class="card floating" style="animation-delay: 1s;">
            <div class="card-icon">🚭</div>
            <h3>علاج الإدمان</h3>
            <p>برامج متخصصة للتقييم والعلاج والتأهيل من الإدمان، مع خطط فردية ومتابعة مستمرة لضمان التعافي المستدام.</p>
            <a href="{{ url_for('addiction') }}" class="btn btn-primary">ابدأ التقييم</a>
          </div>
        </div>
      </div>
    </section>

    <section class="services">
      <div class="container">
        <h2 class="section-title">لماذا تختار عربي سايكو؟</h2>
        
        <div class="cards-grid">
          <div class="card">
            <i class="fas fa-shield-alt card-icon"></i>
            <h3>سرية تامة</h3>
            <p>نضمن حماية كاملة لبياناتك وجلساتك بمعايير أمنية عالية المستوى.</p>
          </div>
          
          <div class="card">
            <i class="fas fa-certificate card-icon"></i>
            <h3>كفاءة علمية</h3>
            <p>فريق مختص من الأطباء والمعالجين النفسيين معتمد وذو خبرة واسعة.</p>
          </div>
          
          <div class="card">
            <i class="fas fa-globe card-icon"></i>
            <h3>خدمة عن بعد</h3>
            <p>احصل على خدماتنا من أي مكان في العالم عبر منصات التواصل الآمن.</p>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer>
    <div class="container">
      <div class="footer-content">
        <div class="copyright">© {{ year }} عربي سايكو — جميع الحقوق محفوظة</div>
        <div class="design-credit">تصميم يوحّد بين الأصالة العربية والحداثة — لرعاية نفسية بأعلى معايير الجودة</div>
      </div>
    </div>
  </footer>

  <script>
    // تأثيرات تفاعلية بسيطة
    document.addEventListener('DOMContentLoaded', function() {
      const cards = document.querySelectorAll('.card');
      
      cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
          this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
          this.style.transform = 'translateY(0)';
        });
      });
    });
  </script>
</body>
</html>
