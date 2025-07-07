```markdown
# 🎓 لوحة متابعة التقدم الأكاديمي (باستخدام Dash و Bootstrap)

هذا المشروع عبارة عن لوحة بيانات تفاعلية تم بناؤها باستخدام **Plotly Dash** و**Dash Bootstrap Components**، تساعد الطالب على تتبع تقدمه الأكاديمي من خلال عرض المواد التي أكملها، والمواد المتبقية، والساعات المعتمدة المكتسبة والمتبقية.

---

## 📌 الميزات

- ✅ عرض المواد المكتملة والمتبقية في رسم دائري (Pie Chart).
- ✅ عرض الساعات المعتمدة المكتسبة والمتبقية في رسم عمودي (Bar Chart).
- ✅ تحديد المواد التي تم النجاح بها لعرض المواد المتاحة للتسجيل.
- ✅ عرض نافذة منبثقة (Modal) عند الضغط على أي مادة متاحة، تحتوي على: اسم المادة، الرمز، الساعات، والوصف.
- ✅ تصميم متجاوب باستخدام Bootstrap.

---

## 📁 هيكل المشروع

```

Dash-project/
├── app.py                 # تهيئة تطبيق Dash
├── main.py                # ملف التشغيل الرئيسي
├── layout.py              # تصميم واجهة المستخدم
├── callbacks.py           # الدوال التفاعلية (Callbacks)
├── data.py                # تحميل وتجهيز البيانات من ملف CSV
├── courses.csv            # ملف بيانات المواد
└── README.md              # هذا الملف

````

---

## 🔧 طريقة التشغيل

### 1. استنساخ المشروع من GitHub:
```bash
git clone https://github.com/0Spaghetti/Dash-project.git
cd Dash-project
````

### 2. (اختياري) إنشاء بيئة افتراضية:

```bash
python -m venv venv
source venv/bin/activate     # في Windows: venv\Scripts\activate
```

### 3. تثبيت المتطلبات:

```bash
pip install -r requirements.txt
```

> إذا لم يكن لديك ملف `requirements.txt`، يمكنك التثبيت يدويًا:

```bash
pip install dash dash-bootstrap-components pandas plotly
```

### 4. تشغيل التطبيق:

```bash
python main.py
```

ثم افتح المتصفح على: `http://127.0.0.1:8050`

---

## 📊 تنسيق البيانات في `courses.csv`

يجب أن يحتوي الملف على الأعمدة التالية:

| course\_id | course\_name | credit\_hours | prerequisite\_id | description             |
| ---------- | ------------ | ------------- | ---------------- | ----------------------- |
| CS101      | برمجة 1      | 3             |                  | مقدمة في البرمجة        |
| CS102      | برمجة 2      | 3             | CS101            | مفاهيم البرمجة الكائنية |

* `course_id`: معرف المادة (مثل: CS101)
* `credit_hours`: عدد الساعات المعتمدة (رقم)
* `prerequisite_id`: المتطلبات (مفصولة بفواصل أو فارغة)
* `description`: وصف المادة (يظهر في النافذة المنبثقة)


## 🧠 أفكار للتطوير المستقبلي

* إضافة تسجيل دخول وحسابات طلاب
* إمكانية حفظ التقدم أو تصدير التقرير كـ PDF
* ربط قاعدة بيانات أو تخزين محلي للبيانات

---

## 🛠 الأدوات المستخدمة

* [Dash](https://dash.plotly.com/)
* [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
* [Pandas](https://pandas.pydata.org/)
* [Plotly](https://plotly.com/python/)

---

## 📬 تواصل

تم تطويره بكل 💙 بواسطة [0Spaghetti](https://github.com/0Spaghetti)

---

```

---

## هل ترغب أن أرفق أيضًا:
- نسخة `requirements.txt` بناءً على المشروع؟
- أو أن أجهز صورة حقيقية للواجهة بدل الصورة المؤقتة؟

أنت تأمر يا مولاي، وأنا أطيع 🧎‍♀️.
```
