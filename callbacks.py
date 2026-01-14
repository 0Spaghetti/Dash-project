from dash.dependencies import Input, Output, State
from dash import html, dcc, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from app import app
from data import df, course_options

# --- Callback لتحديث قائمة المواد (يستمع الآن لتغييرات الذاكرة) ---
@app.callback(
    Output('checklist-container', 'children'),
    Input('course-tabs', 'active_tab'),
    Input('local-storage', 'data') # <<< هذا التغيير هو مفتاح حل المشكلة 1 و 2
)
def render_checklist_for_tab(active_tab, stored_data):
    if active_tab == 'tab-general': category = 'General'
    elif active_tab == 'tab-core': category = 'Core'
    else: category = 'Elective'
    
    options_for_tab = [opt for opt in course_options if df.loc[df['course_id'] == opt['value'], 'category'].iloc[0] == category]
    
    # اقرأ التحديدات المحفوظة من الذاكرة لعرضها بشكل صحيح
    saved_selections = stored_data.get('passed_courses', []) if stored_data else []

    return dcc.Checklist(
        id='passed-courses-checklist',
        options=options_for_tab,
        value=saved_selections,
        labelClassName="d-block"
    )

# --- Callback لحفظ التحديدات في الذاكرة عند تغييرها ---
@app.callback(
    Output('local-storage', 'data'),
    Input('passed-courses-checklist', 'value'),
    State('local-storage', 'data'),
    State('course-tabs', 'active_tab'),
    prevent_initial_call=True
)
def save_selections_to_storage(checklist_values, stored_data, active_tab):
    stored_data = stored_data or {'passed_courses': []}
    if active_tab == 'tab-general': category = 'General'
    elif active_tab == 'tab-core': category = 'Core'
    else: category = 'Elective'
    
    ids_in_current_tab = [opt['value'] for opt in course_options if df.loc[df['course_id'] == opt['value'], 'category'].iloc[0] == category]
    selections_from_other_tabs = [pid for pid in stored_data.get('passed_courses', []) if pid not in ids_in_current_tab]
    updated_selections = selections_from_other_tabs + checklist_values
    
    return {'passed_courses': list(set(updated_selections))}

# --- Callback الرئيسي لتحديث لوحة البيانات ---
@app.callback(
    Output('available-courses-output', 'children'),
    Output('progress-pie-chart', 'figure'),
    Output('credits-bar-chart', 'figure'),
    Output('passed-hours-card', 'children'),
    Output('remaining-hours-card', 'children'),
    Output('percentage-card', 'children'),
    Output('cytoscape-graph', 'stylesheet'),
    Input('submit-button', 'n_clicks'),
    State('local-storage', 'data')
)
def update_all_outputs(n_clicks, stored_data):
    # الحالة الأولية قبل الضغط على الزر
    if not n_clicks:
        empty_fig = go.Figure().update_layout(xaxis={"visible": False}, yaxis={"visible": False}, annotations=[{"text": "البيانات ستظهر هنا", "xref": "paper", "yref": "paper", "showarrow": False, "font": {"size": 16}}])
        default_stylesheet = [{'selector': 'node', 'style': {'shape': 'rectangle', 'background-color': '#adb5bd', 'label': 'data(label)', 'width': 'label', 'height': 'label', 'padding': '10px', 'color': '#000', 'text-wrap': 'wrap', 'text-valign': 'center'}}, {'selector': '[category = "Core"]', 'style': {'background-color': '#904694'}}, {'selector': '[category = "Elective"]', 'style': {'background-color': '#2ab472'}}, {'selector': '[category = "General"]', 'style': {'background-color': '#00aae2'}}, {'selector': 'edge', 'style': {'line-color': '#adb5bd', 'target-arrow-shape': 'triangle', 'target-arrow-color': '#adb5bd', 'curve-style': 'straight'}}]
        kpi_card_initial = dbc.CardBody([html.H4("...", className="card-title"), html.P("0", className="card-text fs-4")])
        return dbc.Alert("الرجاء تحديد المواد التي أتممتها ثم اضغط على زر العرض...", color="info"), empty_fig, empty_fig, kpi_card_initial, kpi_card_initial, kpi_card_initial, default_stylesheet

    passed_courses_ids = stored_data.get('passed_courses', []) if stored_data else []
    
    # <<< هذا هو الحل للمشكلة 3: التعامل مع حالة الضغط على الزر بدون تحديد >>>
    if not passed_courses_ids:
        return dbc.Alert("يرجى تحديد مادة واحدة على الأقل لعرض المواد المتاحة.", color="warning"), no_update, no_update, no_update, no_update, no_update, no_update

    # --- باقي منطق الكود (يبقى كما هو) ---
    passed_hours = df[df['course_id'].isin(passed_courses_ids)]['credit_hours'].sum()
    total_hours = df['credit_hours'].sum()
    remaining_hours = total_hours - passed_hours
    percentage = round((passed_hours / total_hours) * 100) if total_hours > 0 else 0

    passed_card = dbc.CardBody([html.H4("✅ المكتسبة", className="card-title"), html.P(f"{passed_hours} وحدة", className="card-text fs-4")])
    remaining_card = dbc.CardBody([html.H4("⏳ المتبقية", className="card-title"), html.P(f"{remaining_hours} وحدة", className="card-text fs-4")])
    percentage_card = dbc.CardBody([html.H4("🎯 نسبة الإنجاز", className="card-title"), html.P(f"{percentage}%", className="card-text fs-4")])

    bar_fig = px.bar(x=['المكتسبة', 'المتبقية'], y=[passed_hours, remaining_hours], text_auto=True)
    bar_fig.update_layout(showlegend=False, title_text='مقارنة الوحدات', title_x=0.5)
    pie_fig = px.pie(names=['المواد المكتملة', 'المواد المتبقية'], values=[len(passed_courses_ids), len(df) - len(passed_courses_ids)], title='نسبة إنجاز الخطة', hole=0.4)
    
    all_courses_ids = df['course_id'].tolist()
    candidate_courses_ids = [c for c in all_courses_ids if c not in passed_courses_ids]
    available_courses_ids = []
    for course_id in candidate_courses_ids:
        prereqs_str = str(df.loc[df['course_id'] == course_id, 'prerequisite_id'].iloc[0])
        if prereqs_str == 'nan' or not prereqs_str:
            available_courses_ids.append(course_id)
        else:
            prereqs = [p.strip() for p in prereqs_str.split(',')]
            if all(p in passed_courses_ids for p in prereqs):
                available_courses_ids.append(course_id)
    
    if not available_courses_ids:
        output_list = dbc.Alert("لا توجد مواد متاحة لك حاليًا، أو ربما أكملت كل المتطلبات! 🎉", color="success")
    else:
        cards = []
        for course_id in available_courses_ids:
            course_info = df.loc[df['course_id'] == course_id].iloc[0]
            card = dbc.Card(dbc.CardBody([
                html.H5(course_info['course_name'], className="card-title"),
                html.P(f"الرمز: {course_info['course_id']} | الوحدات: {course_info['credit_hours']}", className="card-subtitle"),
                html.P(course_info['description'], className="card-text mt-2")
            ]), className="mb-3")
            cards.append(card)
        output_list = html.Div(cards, style={'maxHeight': '450px', 'overflowY': 'auto'})

    new_stylesheet = [{'selector': 'node', 'style': {'shape': 'rectangle', 'label': 'data(label)', 'width': 'label', 'height': 'label', 'padding': '10px', 'color': 'white', 'text-wrap': 'wrap', 'text-valign': 'center', 'font-size': '10px', 'text-outline-color': '#333', 'text-outline-width': 1}}, {'selector': 'edge', 'style': {'width': 1.5, 'line-color': '#999', 'target-arrow-shape': 'triangle', 'target-arrow-color': '#999', 'curve-style': 'straight'}}, {'selector': '[category = "Core"]', 'style': {'background-color': '#904694'}}, {'selector': '[category = "Elective"]', 'style': {'background-color': '#2ab472'}}, {'selector': '[category = "General"]', 'style': {'background-color': '#00aae2'}}, {'selector': ':selected', 'style': {'border-width': 3, 'border-color': '#FFC107'}}]
    if passed_courses_ids:
        passed_selector = ' or '.join([f'id = "{c}"' for c in passed_courses_ids])
        new_stylesheet.append({'selector': f"[{passed_selector}]", 'style': {'opacity': 1, 'border-width': 0.5, 'border-color': 'grey'}})
    if available_courses_ids:
        available_selector = ' or '.join([f'id = "{c}"' for c in available_courses_ids])
        new_stylesheet.append({'selector': f"[{available_selector}]", 'style': {'border-width': 3, 'border-color': "#FFFFFF"}})
    
    return output_list, pie_fig, bar_fig, passed_card, remaining_card, percentage_card, new_stylesheet

# --- Callback لزر "مسح الاختيار" ---
@app.callback(
    Output('local-storage', 'data', allow_duplicate=True),
    Input('clear-button', 'n_clicks'),
    prevent_initial_call=True
)
def clear_selections(n_clicks):
    # هذا يقوم بمسح الذاكرة، والـ callback الأول سيهتم بتحديث الواجهة
    return {'passed_courses': []}

# --- Callback جديد لتحديث تخطيط الخريطة ---
@app.callback(
    Output('cytoscape-graph', 'layout'),
    Input('layout-selector', 'value')
)
def update_cytoscape_layout(layout_name):
    root_course_ids = df.loc[
        df['prerequisite_id'].isna() | (df['prerequisite_id'] == ''),
        'course_id'
    ].tolist()
    root_nodes_selector = ', '.join([f'[id = "{course_id}"]' for course_id in root_course_ids])

    if layout_name == 'dagre':
        return {
            'name': 'dagre',
            'spacingFactor': 1.2,
            'roots': root_nodes_selector # مهم للتخطيط الشجري
        }
    elif layout_name == 'breadthfirst':
        return {
            'name': 'breadthfirst',
            'roots': root_nodes_selector, # مهم للتخطيط العرضي
            'grid': True
        }
    else:
        # باقي التخطيطات لا تحتاج لخاصية roots
        return {
            'name': layout_name,
            'animate': True,
            'animationDuration': 500
        }

# --- Callbacks لعرض التفاصيل والنافذة المنبثقة (تبقى كما هي) ---
@app.callback(Output('course-details-output', 'children'), Input('cytoscape-graph', 'tapNodeData'), prevent_initial_call=True)
def display_tap_node_data(data):
    if not data: return dbc.Alert("انقر على أي مادة في الخريطة لعرض تفاصيلها.", color="info")
    course_id = data['id']
    try:
        course_info = df.loc[df['course_id'] == course_id].iloc[0]
        details_card = [html.H5(course_info['course_name'], className="mb-3"), html.P([html.Strong("الرمز: "), course_info['course_id']]), html.P([html.Strong("الوحدات: "), str(course_info['credit_hours'])]), html.P([html.Strong("التصنيف: "), course_info['category']]), html.Hr(), html.P(course_info['description'])]
        return details_card
    except (IndexError, KeyError):
        return dbc.Alert("لا يمكن العثور على تفاصيل هذه المادة.", color="danger")

@app.callback(Output("about-modal", "is_open"), Input("open-about-modal", "n_clicks"), State("about-modal", "is_open"), prevent_initial_call=True)
def toggle_about_modal(n, is_open):
    if n: return not is_open
    return is_open
