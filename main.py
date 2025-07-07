from app import app, server
from layout import layout
import callbacks # فقط قم باستيراد الملف ليتم تسجيل الـ callbacks

# تعيين الواجهة للتطبيق
app.layout = layout

# نقطة تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)