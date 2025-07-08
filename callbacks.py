from dash.dependencies import Input, Output, State
from dash import html, no_update
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
    if not search_value: return course_options
    search_lower = search_value.lower()
    return [opt for opt in course_options if search_lower in opt['label'].lower()]

# --- Callback الرئيسي لتحديث لوحة البيانات والخريطة ---
@app.callback(
    [Output('available-courses-output', 'children'),
     Output('progress-pie-chart', 'figure'),
     Output('credits-bar-chart', 'figure'),
     Output('passed-hours-card', 'children'),
     Output('remaining-hours-card', 'children'),
     Output('percentage-card', 'children'),
     Output('cytoscape-graph', 'stylesheet')],
    Input('submit-button', 'n_clicks'),
    State('passed-courses-checklist', 'value')
)
def update_all_outputs(n_clicks, passed_courses_ids):
    if n_clicks == 0:
        empty_fig = go.Figure().update_layout(xaxis={"visible": False}, yaxis={"visible": False}, annotations=[{"text": "البيانات ستظهر هنا", "xref": "paper", "yref": "paper", "showarrow": False, "font": {"size": 16}}])
        default_stylesheet = [
            {'selector': 'node', 'style': {'shape': 'rectangle', 'background-color': '#adb5bd', 'label': 'data(label)', 'width': 'label', 'height': 'label', 'padding': '10px', 'color': '#000', 'text-wrap': 'wrap', 'text-valign': 'center'}},
            {'selector': '[category = "Core"]', 'style': {'background-color': '#904694'}},
            {'selector': '[category = "Elective"]', 'style': {'background-color': '#2ab472'}},
            {'selector': '[category = "General"]', 'style': {'background-color': '#00aae2'}},
            {'selector': 'edge', 'style': {'line-color': '#adb5bd', 'target-arrow-shape': 'triangle', 'target-arrow-color': '#adb5bd', 'curve-style': 'straight'}}
        ]
        kpi_card_initial = [html.H3("0"), html.P("...")]
        return dbc.Alert("الرجاء تحديد المواد التي أتممتها...", color="info"), empty_fig, empty_fig, kpi_card_initial, kpi_card_initial, kpi_card_initial, default_stylesheet

    passed_hours = df[df['course_id'].isin(passed_courses_ids)]['credit_hours'].sum()
    total_hours = df['credit_hours'].sum()
    remaining_hours = total_hours - passed_hours
    percentage = round((passed_hours / total_hours) * 100) if total_hours > 0 else 0
    passed_card = [html.H3(f"{passed_hours}"), html.P("ساعة مكتسبة")]
    remaining_card = [html.H3(f"{remaining_hours}"), html.P("ساعة متبقية")]
    percentage_card = [html.H3(f"{percentage}%"), html.P("الإنجاز")]
    bar_fig = px.bar(x=['المكتسبة', 'المتبقية'], y=[passed_hours, remaining_hours], text_auto=True)
    bar_fig.update_layout(showlegend=False, title_text='مقارنة الساعات', title_x=0.5)
    pie_fig = px.pie(names=['المواد المكتملة', 'المواد المتبقية'], values=[len(passed_courses_ids), len(df) - len(passed_courses_ids)], title='نسبة إنجاز الخطة', hole=0.4)
    
    all_courses_ids = df['course_id'].tolist()
    candidate_courses_ids = [c for c in all_courses_ids if c not in passed_courses_ids]
    available_courses_ids = []
    for course_id in candidate_courses_ids:
        prereqs_str = str(df.loc[df['course_id'] == course_id, 'prerequisite_id'].iloc[0])
        if prereqs_str == 'nan' or not prereqs_str: available_courses_ids.append(course_id)
        else:
            if set(prereqs_str.split(',')).issubset(set(passed_courses_ids)): available_courses_ids.append(course_id)
    if not available_courses_ids: output_list = [dbc.Alert("لا توجد مواد متاحة لك حاليًا.", color="warning")]
    else: output_list = html.Ul([html.Li(df.loc[df['course_id'] == cid, 'course_name'].iloc[0]) for cid in available_courses_ids])
    
    new_stylesheet = [
        {'selector': 'node', 'style': {'shape': 'rectangle', 'label': 'data(label)', 'width': 'label', 'height': 'label', 'padding': '10px', 'color': 'white', 'text-wrap': 'wrap', 'text-valign': 'center', 'font-size': '10px', 'text-outline-color': '#333', 'text-outline-width': 1}},
        {'selector': 'edge', 'style': {'width': 1.5, 'line-color': '#999', 'target-arrow-shape': 'triangle', 'target-arrow-color': '#999', 'curve-style': 'straight'}},
        {'selector': '[category = "Core"]', 'style': {'background-color': '#904694'}},
        {'selector': '[category = "Elective"]', 'style': {'background-color': '#2ab472'}},
        {'selector': '[category = "General"]', 'style': {'background-color': '#00aae2'}},
        {'selector': ':selected', 'style': {'border-width': 3, 'border-color': '#FFC107'}},
    ]
    if passed_courses_ids:
        new_stylesheet.append({'selector': f"[{' or '.join([f'id = \"{c}\"' for c in passed_courses_ids])}]", 'style': {'opacity': 1.0}})
    
    return output_list, pie_fig, bar_fig, passed_card, remaining_card, percentage_card, new_stylesheet

# --- Callback لفتح نافذة "حول" ---
@app.callback(
    Output("about-modal", "is_open"),
    Input("open-about-modal", "n_clicks"),
    State("about-modal", "is_open"),
    prevent_initial_call=True,
)
def toggle_about_modal(n, is_open):
    if n:
        return not is_open
    return is_open

# --- Callback لعرض تفاصيل المادة ---
@app.callback(
    Output('course-details-output', 'children'),
    Input('cytoscape-graph', 'tapNodeData'),
    prevent_initial_call=True
)
def display_tap_node_data(data):
    if not data:
        return dbc.Alert("انقر على أي مادة في الخريطة لعرض تفاصيلها.", color="info")

    course_id = data['id']
    try:
        course_info = df.loc[df['course_id'] == course_id].iloc[0]
        details_card = [
            html.H5(course_info['course_name'], className="mb-3"),
            html.P([html.Strong("الرمز: "), course_info['course_id']]),
            html.P([html.Strong("الساعات: "), str(course_info['credit_hours'])]),
            html.P([html.Strong("التصنيف: "), course_info['category']]),
            html.Hr(),
            html.P(course_info['description'])
        ]
        return details_card
    except (IndexError, KeyError):
        return dbc.Alert("لا يمكن العثور على تفاصيل هذه المادة.", color="danger")