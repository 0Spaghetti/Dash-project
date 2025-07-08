import dash_cytoscape as cyto # <<< 1. استيراد المكتبة هنا
from app import app, server
from layout import layout
import callbacks

# <<< 2. إضافة السطر المهم لتحميل الإضافات
cyto.load_extra_layouts()

# تعيين الواجهة للتطبيق
app.layout = layout

# نقطة تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)