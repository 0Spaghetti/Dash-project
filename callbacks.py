from dash.dependencies import Input, Output, State
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from app import app
from data import df, course_options

# --- Callback لفلترة قائمة المواد ---
@app.callback(
    Output('passed-courses-checklist', 'options'),
    Input('course-search-input', 'value')
)
def filter_course_checklist(search_value):
    if not search_value:
        return course_options
    search_lower = search_value.lower()
    filtered_options = [
        option for option in course_options 
        if search_lower in option['label'].lower()
    ]
    return filtered_options


# --- Callback الرئيسي لتحديث لوحة البيانات والخريطة ---
@app.callback(
    [Output('available-courses-output', 'children'),
     Output('progress-pie-chart', 'figure'),
     Output('credits-bar-chart', 'figure'),
     Output('cytoscape-graph', 'stylesheet')],
    Input('submit-button', 'n_clicks'),
    State('passed-courses-checklist', 'value')
)
def update_all_outputs(n_clicks, passed_courses_ids):
    # --- الحالة الابتدائية ---
    if n_clicks == 0:
        empty_fig = go.Figure()
        empty_fig.update_layout(xaxis={"visible": False}, yaxis={"visible": False}, annotations=[{"text": "البيانات ستظهر هنا", "xref": "paper", "yref": "paper", "showarrow": False, "font": {"size": 16}}])
        # ورقة أنماط افتراضية محسنة
        default_stylesheet = [
            {'selector': 'node', 'style': {'background-color': '#adb5bd', 'label': 'data(label)', 'font-size': '12px', 'color': '#000'}},
            {'selector': 'edge', 'style': {'curve-style': 'bezier', 'target-arrow-shape': 'triangle', 'line-color': '#adb5bd', 'target-arrow-color': '#adb5bd'}}
        ]
        return dbc.Alert("الرجاء تحديد المواد التي أتممتها ثم اضغط على الزر.", color="info"), empty_fig, empty_fig, default_stylesheet

    # --- (باقي الحسابات كما هي) ---
    total_courses = len(df)
    passed_count = len(passed_courses_ids)
    remaining_count = total_courses - passed_count
    pie_fig = px.pie(names=['المواد المكتملة', 'المواد المتبقية'], values=[passed_count, remaining_count], title='نسبة إنجاز الخطة', hole=0.4, color_discrete_sequence=['#28a745', '#E9ECEF'])
    total_hours = df['credit_hours'].sum()
    passed_hours = df[df['course_id'].isin(passed_courses_ids)]['credit_hours'].sum()
    remaining_hours = total_hours - passed_hours
    bar_fig = px.bar(x=['المكتسبة', 'المتبقية'], y=[passed_hours, remaining_hours], title='الساعات المعتمدة', labels={'x': 'الحالة', 'y': 'عدد الساعات'}, color=['#28a745', '#E9ECEF'], text_auto=True)
    bar_fig.update_layout(showlegend=False)
    all_courses_ids = df['course_id'].tolist()
    candidate_courses_ids = [course for course in all_courses_ids if course not in passed_courses_ids]
    available_courses_ids = []
    for course_id in candidate_courses_ids:
        prereqs_str = str(df.loc[df['course_id'] == course_id, 'prerequisite_id'].iloc[0])
        if prereqs_str == 'nan' or not prereqs_str:
            available_courses_ids.append(course_id)
            continue
        required_ids = prereqs_str.split(',')
        if set(required_ids).issubset(set(passed_courses_ids)):
            available_courses_ids.append(course_id)
    if not available_courses_ids:
        output_list = [dbc.Alert("لا توجد مواد متاحة لك حاليًا.", color="warning")]
    else:
        available_courses_names = df[df['course_id'].isin(available_courses_ids)]['course_name'].tolist()
        output_list = html.Ul([html.Li(name) for name in available_courses_names])

    # --- ورقة الأنماط الديناميكية المحسنة ---
    new_stylesheet = [
        # القاعدة الافتراضية لكل العُقد
        {'selector': 'node', 'style': {
            'background-color': '#adb5bd', 
            'label': 'data(label)',
            'font-size': '12px', 
            'color': '#000',
            'text-outline-width': 1,
            'text-outline-color': '#fff'
        }},
        # القاعدة الافتراضية للروابط
        {'selector': 'edge', 'style': {
            'curve-style': 'bezier',
            'target-arrow-shape': 'triangle',
            'width': 1.5,
            'line-color': '#ced4da',
            'target-arrow-color': '#ced4da'
        }},
        # شكل العقدة عند تحديدها
        {'selector': ':selected', 'style': {
            'border-width': 3,
            'border-color': '#FFC107'
        }},
    ]
    
    # قواعد التلوين الديناميكية
    if passed_courses_ids:
        new_stylesheet.append({
            'selector': f"[{' or '.join([f'id = \"{course}\"' for course in passed_courses_ids])}]",
            'style': {'background-color': '#28a745', 'line-color': '#28a745'}
        })
    if available_courses_ids:
        new_stylesheet.append({
            'selector': f"[{' or '.join([f'id = \"{course}\"' for course in available_courses_ids])}]",
            'style': {'background-color': '#007bff', 'line-color': '#007bff'}
        })

    # --- إرجاع كل المخرجات ---
    return output_list, pie_fig, bar_fig, new_stylesheet