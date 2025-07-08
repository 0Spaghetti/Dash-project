import pandas as pd

def load_data():
    """
    تقوم هذه الدالة بقراءة ملف البيانات وتجهيزه للعرض في التطبيق.
    """
    try:
        # هنا قمنا بإضافة الترميز الصحيح
        df = pd.read_csv('courses.csv', encoding='windows-1256')
        
        # التعامل مع القيم الفارغة في عمود المتطلبات لضمان أنه نصي
        df['prerequisite_id'] = df['prerequisite_id'].astype(str)
        
        # تجهيز قائمة الخيارات لمكون الـ Checklist
        course_options = [{'label': f"{row['course_name']} ({row['credit_hours']} وحدات)", 'value': row['course_id']}
                          for index, row in df.iterrows()]
        
        return df, course_options
        
    except FileNotFoundError:
        print("خطأ فادح: لم يتم العثور على ملف 'courses.csv'. تأكد من وجوده في المجلد الصحيح.")
        return pd.DataFrame(), []

def create_cytoscape_elements(dataframe):
    """
    تقوم هذه الدالة بتحويل بيانات الخطة الدراسية إلى تنسيق يفهمه Cytoscape
    (قائمة من العُقد والروابط).
    """
    nodes = []
    edges = []

    for index, row in dataframe.iterrows():
        # --- 1. إنشاء العُقد (Nodes) ---
        nodes.append({
            'data': {
                'id': row['course_id'],
                'label': row['course_name'],
                'category': row['category']
            }
        })

        # --- 2. إنشاء الروابط (Edges) ---
        if row['prerequisite_id'] != 'nan':
            # التعامل مع حالة وجود أكثر من متطلب واحد
            prerequisites = row['prerequisite_id'].split(',')
            for prereq in prerequisites:
                edges.append({
                    'data': {
                        # معرّف فريد للرابط (اختياري لكنه ممارسة جيدة)
                        'id': f"{prereq}-{row['course_id']}",
                        # مصدر السهم
                        'source': prereq,
                        # وجهة السهم
                        'target': row['course_id']
                    }
                })

    # دمج العُقد والروابط في قائمة واحدة
    return nodes + edges

# --- الجزء الرئيسي الذي يتم تشغيله عند استيراد الملف ---

# قم بتحميل البيانات الأساسية
df, course_options = load_data()

# قم بإنشاء عناصر الرسم البياني إذا تم تحميل البيانات بنجاح
if not df.empty:
    cytoscape_elements = create_cytoscape_elements(df)
else:
    cytoscape_elements = []