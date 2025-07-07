import dash
import dash_bootstrap_components as dbc

# تهيئة التطبيق مع إضافة ثيم Bootstrap
# هذا هو المتغير المركزي 'app' الذي ستستخدمه كل الملفات الأخرى
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    # هذا السطر مهم عند فصل الكود لتجنب أخطاء الـ callback
    suppress_callback_exceptions=True 
)

server = app.server
