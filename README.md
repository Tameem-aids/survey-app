# 📋 استبيان دور العلاقات العامة في تعزيز السمعة المؤسسية

## وصف المشروع
موقع ويب لاستبيان طلابي حول "دور العلاقات العامة في تعزيز السمعة المؤسسية لكلية الآداب بجامعة تعز".

## هيكل المشروع
```
survey-app/
├── app.py                 # الخادم الرئيسي (Flask)
├── requirements.txt       # المكتبات المطلوبة
├── survey.db             # قاعدة البيانات (تُنشأ تلقائياً)
├── static/
│   └── style.css         # تنسيق الموقع
├── templates/
│   ├── survey.html       # صفحة الاستبيان
│   ├── thank_you.html    # صفحة الشكر
│   ├── admin_login.html  # تسجيل دخول المشرف
│   └── admin_dashboard.html  # لوحة التحكم
└── README.md             # هذا الملف
```

## 🚀 التشغيل محلياً

### 1. تثبيت المتطلبات
```bash
pip install -r requirements.txt
```

### 2. تشغيل الموقع
```bash
python app.py
```

### 3. فتح الموقع
- **الاستبيان**: http://localhost:5000
- **لوحة التحكم**: http://localhost:5000/admin

### بيانات لوحة التحكم
- **كلمة المرور**: `admin123` (غيّرها في app.py)

---

## 🌐 النشر على الإنترنت (مجاناً)

### الخيار 1: Render.com (مُوصى به - مجاني)

1. **أنشئ حساب** على [render.com](https://render.com)
2. **ارفع المشروع** إلى GitHub:
   ```bash
   git init
   git add .
   git commit -m "first commit"
   git remote add origin https://github.com/username/survey-app.git
   git push -u origin main
   ```
3. **على Render**:
   - اختر "New Web Service"
   - اربطه بمستودع GitHub
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - اضغط "Create Web Service"
4. ستحصل على رابط مثل: `https://your-survey.onrender.com`

### الخيار 2: PythonAnywhere (مجاني)

1. أنشئ حساب على [pythonanywhere.com](https://www.pythonanywhere.com)
2. ارفع الملفات عبر لوحة التحكم
3. أنشئ Web App جديد واختر Flask
4. عدّل المسار ليشير إلى app.py
5. ستحصل على رابط مثل: `https://username.pythonanywhere.com`

### الخيار 3: Railway.app (مجاني مع حدود)

1. أنشئ حساب على [railway.app](https://railway.app)
2. اربط مستودع GitHub
3. سيتم النشر تلقائياً

---

## 📊 الميزات

- ✅ استبيان كامل بـ 45 عبارة + بيانات عامة
- ✅ مقياس ليكرت الخماسي
- ✅ تصميم عربي متجاوب (يعمل على الجوال)
- ✅ حفظ تلقائي في قاعدة بيانات SQLite
- ✅ لوحة تحكم لعرض النتائج
- ✅ تصدير النتائج كملف CSV
- ✅ شريط تقدم أثناء ملء الاستبيان
- ✅ التحقق من ملء جميع الحقول
- ✅ حماية لوحة التحكم بكلمة مرور

---

## ⚙️ إعدادات مهمة (غيّرها قبل النشر)

في ملف `app.py`:
```python
app.secret_key = 'your-secret-key-change-this'  # غيّر لمفتاح عشوائي طويل
ADMIN_PASSWORD = 'admin123'  # غيّر كلمة المرور
```

---

## 📧 الدعم
للأسئلة أو المساعدة، تواصل مع مطور المشروع.
