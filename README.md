طاعةً لك يا مولاي 👑، إليك ملف `README.md` متكامل وجاهز للاستخدام، باللغة الإنجليزية، ليتماشى مع أسلوب GitHub الاحترافي، مع شرح وافي عن المشروع، طريقة التشغيل، الملفات، وبيانات الداتا.

---

### 📄 `README.md`

```markdown
# 🎓 Academic Progress Dashboard (Dash + Bootstrap)

This project is a dynamic interactive dashboard built using **Plotly Dash** and **Bootstrap Components**, designed to help students visualize their academic progress, including completed courses, available courses, and credit hour statistics.

---

## 📌 Features

- ✅ View passed and remaining courses in a pie chart.
- ✅ View total and earned credit hours in a bar chart.
- ✅ Select completed courses to see eligible (available) ones.
- ✅ Click on any available course to view a **popup (modal)** with full details: course code, credit hours, and description.
- ✅ Responsive layout using **Dash Bootstrap Components**.

---

## 📁 Project Structure

```

Dash-project/
├── app.py                 # Initializes Dash app
├── main.py                # Entry point of the app
├── layout.py              # UI Layout (components, cards, charts, modal)
├── callbacks.py           # All Dash callbacks
├── data.py                # Loads and processes course data from CSV
├── courses.csv            # Your data source
└── README.md              # You’re here!

````

---

## 🔧 Installation & Running the App

### 1. Clone the repo:
```bash
git clone https://github.com/0Spaghetti/Dash-project.git
cd Dash-project
````

### 2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install required packages:

```bash
pip install -r requirements.txt
```

> If you don't have a `requirements.txt`, here's what you need:

```bash
pip install dash dash-bootstrap-components pandas plotly
```

### 4. Run the app:

```bash
python main.py
```

Then visit: `http://127.0.0.1:8050` in your browser.

---

## 📊 Data Format (`courses.csv`)

The `courses.csv` file must contain the following columns:

| course\_id | course\_name   | credit\_hours | prerequisite\_id | description          |
| ---------- | -------------- | ------------- | ---------------- | -------------------- |
| CS101      | Programming I  | 3             |                  | Intro to programming |
| CS102      | Programming II | 3             | CS101            | OOP concepts         |

* `course_id`: Unique identifier (e.g., CS101)
* `credit_hours`: Numeric value
* `prerequisite_id`: Comma-separated list (e.g., CS101,CS102) or empty
* `description`: Text shown inside the modal


## 🧠 Future Improvements

* Add login system and student profiles
* Export progress report as PDF
* Save progress using local storage or database

---

## 🛠 Built With

* [Dash](https://dash.plotly.com/)
* [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
* [Pandas](https://pandas.pydata.org/)
* [Plotly](https://plotly.com/python/)

---

## 📬 Contact

Made with 💙 by مهند نوح


