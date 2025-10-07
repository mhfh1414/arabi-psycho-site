# Addiction.py — خطة تعافٍ واضحة بخطوات: فحص سريع + اختيار المادة + خطة 14 يوم + منع الانتكاس + تنزيل JSON

def main():
    return """
    <div class='card'>
      <h1>🚭 برنامج الإدمان — خطوات واضحة</h1>
      <p class='small'>علاج نفسي افتراضي: خطتك مقسّمة إلى فحص سريع، تحديد المادة، خطة 14 يوم، ومنع الانتكاس.</p>

      <style>
        .tabs{display:flex;gap:8px;flex-wrap:wrap;margin:8px 0}
        .tab{padding:8px 12px;border-radius:10px;border:1px solid #ddd;cursor:pointer;font-weight:800}
        .tab.active{background:#4B0082;color:#fff;border-color:#4B0082}
        .sec{display:none;margin-top:10px}
        .sec.active{display:block}
        .grid{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
        label.chk{display:block;background:#fafafa;border:1px solid #eee;border-radius:10px;padding:8px}
        .tile{background:#fafafa;border:1px solid #eee;border-radius:12px;padding:10px}
        .row{display:flex;gap:10px;flex-wrap:wrap;margin-top:10px}
        .btn{display:inline-block;background:#4B0082;color:#fff;text-decoration:none;padding:10px 14px;border-radius:12px;font-weight:800}
        .btn.alt{background:#5b22a6} .btn.gold{background:#FFD700;color:#4B0082}
        table{width:100%;border-collapse:collapse} th,td{border:1px solid #eee;padding:8px;text-align:center}
        th{background:#f7f3ff}
      </style>

      <div class="tabs">
        <div class="tab active" data-target="#a1">🧪 فحص سريع</div>
        <div class="tab" data-target="#a2">🧾 اختيار المادة</div>
        <div class="tab" data-target="#a3">📅 خطة 14 يوم</div>
        <div class="tab" data-target="#a4">🛡️ منع الانتكاس</div>
      </div>

      <!-- a1 -->
      <div id="a1" class="sec active">
        <h2>CAGE-AID مبسّط</h2>
        <div id="cage" class="grid">
          <label class="chk"><input type="checkbox" data-q="Cut down"> فكّرت أن تُخفّف/تقلّل؟</label>
          <label class="chk"><input type="checkbox" data-q="Annoyed"> انزعجت من انتقاد الآخرين؟</label>
          <label class="chk"><input type="checkbox" data-q="Guilty"> شعرت بالذنب؟</label>
          <label class="chk"><input type="checkbox" data-q="Eye-opener"> احتجت مادة صباحًا لتبدأ اليوم؟</label>
        </div>
        <div class="tile">نتيجة إرشادية: إجابتان أو أكثر ⇒ احتمال مشكلة استخدام يستحق متابعة.</div>
        <div class="row"><a class="btn" href="#a2" onclick="openTab('#a2')">التالي: اختيار المادة</a></div>
      </div>

      <!-- a2 -->
      <div id="a2" class="sec">
        <h2>اختر المادة/النمط</h2>
        <div class="grid">
          <label class="chk"><input type="radio" name="substance" value="كحول"> كحول</label>
          <label class="chk"><input type="radio" name="substance" value="أفيونات"> أفيونات</label>
          <label class="chk"><input type="radio" name="substance" value="منبّهات"> منبّهات</label>
          <label class="chk"><input type="radio" name="substance" value="قنّب"> قنّب</label>
          <label class="chk"><input type="radio" name="substance" value="مهدئات/منوّمات"> مهدئات/منوّمات</label>
          <label class="chk"><input type="radio" name="substance" value="مختلط/غير محدد"> مختلط/غير محدد</label>
        </div>
        <div class="tile">ملاحظة: وجود انسحاب شديد/تاريخ نوبات/أدوية معيّنة ⇒ <b>يفضَّل إشراف طبي</b>.</div>
        <div class="row"><a class="btn" href="#a3" onclick="openTab('#a3')">التالي: خطة 14 يوم</a></div>
      </div>

      <!-- a3 -->
      <div id="a3" class="sec">
        <h2>خطة 14 يوم — واضحة ومقسّمة</h2>
        <table id="plan14">
          <thead><tr><th>اليوم</th><th>الهدف</th><th>مهمّة صباح</th><th>مهمّة مساء</th><th>مقياس رغبة (0–10)</th></tr></thead>
          <tbody></tbody>
        </table>
        <div class="tile" style="margin-top:10px">
          <h3>قائمة مهام قياسية</h3>
          <ul>
            <li><b>Detox خفيف/منزلي</b> (عند عدم وجود مخاطر): سوائل، نوم منتظم، بدائل صحية للمتعة.</li>
            <li><b>مهارات رفض + إدارة محفّزات</b>: مكافأة فورية عند الالتزام.</li>
            <li><b>CBT خاص بالإدمان</b>: تعرّف الأفكار المشتهية واستبدالها بأنشطة بديلة.</li>
          </ul>
        </div>
        <div class="row">
          <button class="btn" onclick="add14()">➕ ملء الجدول تلقائيًا</button>
          <button class="btn alt" onclick="saveAdd()">💾 تنزيل خطتي (JSON)</button>
          <button class="btn gold" onclick="window.print()">🖨️ طباعة</button>
        </div>
      </div>

      <!-- a4 -->
      <div id="a4" class="sec">
        <h2>منع الانتكاس — خطة طوارئ</h2>
        <div class="grid">
          <div class="tile"><label>محفّزاتي المتوقعة<textarea id="triggers" rows="4" placeholder="أماكن/أشخاص/مشاعر..."></textarea></label></div>
          <div class="tile"><label>استراتيجياتي البديلة<textarea id="alts" rows="4" placeholder="مشي سريع، اتصال داعم، استحمام دافئ، مهمّة منزلية..."></textarea></label></div>
          <div class="tile"><label>شبكة الدعم<textarea id="supports" rows="4" placeholder="أسماء داعمين/أرقام/مجموعات مساندة..."></textarea></label></div>
        </div>
        <div class="row" style="margin-top:10px">
          <a class="btn gold" href="/book">📅 احجز جلسة</a>
          <a class="btn" href="/cbt">🧠 أدوات CBT</a>
        </div>
      </div>

      <script>
        function openTab(sel){
          document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
          document.querySelectorAll('.sec').forEach(s=>s.classList.remove('active'));
          document.querySelector('.tab[data-target="'+sel+'"]').classList.add('active');
          document.querySelector(sel).classList.add('active');
          history.replaceState(null,'',sel);
        }
        document.querySelectorAll('.tab').forEach(t=>{
          t.addEventListener('click',()=>openTab(t.getAttribute('data-target')));
        });
        if(location.hash && document.querySelector(location.hash)) openTab(location.hash);

        function add14(){
          const tbody=document.querySelector('#plan14 tbody'); tbody.innerHTML='';
          const days=[...Array(14).keys()].map(i=>'اليوم '+(i+1));
          const goals=[
            'خفض الاستخدام 25% + شرب سوائل','خفض 50% + مهارات رفض',
            'امتناع يوم كامل','امتناع يومين','امتناع 3 أيام',
            'تثبيت الروتين + أنشطة بديلة','تقوية شبكة الدعم','مراجعة تقدّم الأسبوع',
            'امتناع متواصل','تعرّف مبكّر على الرغبة','تغيير مسار عند المحفّز',
            'تنشيط بدائل ممتعة','تقييم أسبوعين','خطة صيانة'
          ];
          days.forEach((d,i)=>{
            const r=document.createElement('tr');
            r.innerHTML='<td>'+d+'</td>'
              +'<td contenteditable>'+goals[i]+'</td>'
              +'<td contenteditable>مشي 20د/ماء/تنفّس</td>'
              +'<td contenteditable>اتصال داعم/روتين نوم</td>'
              +'<td contenteditable>0</td>';
            tbody.appendChild(r);
          });
        }

        function saveAdd(){
          const sub=(document.querySelector('input[name=substance]:checked')||{}).value||'غير محدد';
          const cage=[...document.querySelectorAll('#cage input[type=checkbox]:checked')].map(x=>x.getAttribute('data-q'));
          const rows=[...document.querySelectorAll('#plan14 tbody tr')].map(tr=>[...tr.children].map(td=>td.innerText));
          const payload={substance:sub,cage:cage,plan14:rows,
                         triggers:document.getElementById('triggers')?.value||'',
                         alternatives:document.getElementById('alts')?.value||'',
                         supports:document.getElementById('supports')?.value||'',
                         created_at:new Date().toISOString()};
          const a=document.createElement('a');
          a.href=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:'application/json'}));
          a.download='addiction_plan.json'; a.click(); URL.revokeObjectURL(a.href);
        }
      </script>

      <div class="tile" style="margin-top:12px">
        <b>عبارة تشجيع:</b> «الالتزام اليومي الصغير هو سرّ النتائج الكبيرة.»
      </div>
    </div>
    """
