from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from data import course_options, cytoscape_elements

# تعريف متغير الواجهة
layout = dbc.Container([
    # <<< الجزء الجديد الذي تمت إضافته
    # --- شريط التنقل العلوي ---
    dbc.NavbarSimple(
        brand="مخطط المسار الدراسي 🎓",
        color="primary",
        dark=True,
        className="mb-4", # لإضافة هامش سفلي
    ),
    # >>> نهاية الجزء الجديد

    # --- الصف الأول: العنوان الرئيسي (يمكن إزالته الآن لأن العنوان في الشريط) ---
    dbc.Row([
        dbc.Col(html.H1("لوحة بيانات المسار الدراسي", className="text-center my-4"), width=12)
    ]),

    # --- الصف الثاني: الرسوم البيانية ---
    dbc.Row([
        dbc.Col(dcc.Loading(type="circle", children=dbc.Card(dcc.Graph(id='progress-pie-chart'))), width=12, md=6),
        dbc.Col(dcc.Loading(type="circle", children=dbc.Card(dcc.Graph(id='credits-bar-chart'))), width=12, md=6)
    ], className="mb-4"),

    # --- الصف الثالث: الإدخال والنتائج ---
    dbc.Row([
        # --- العمود الأيسر: المدخلات (مع مربع البحث) ---
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("الخطوة 1: حدد المواد التي نجحت فيها")),
                dbc.CardBody([
                    dbc.Input(
                        id="course-search-input",
                        placeholder="ابحث عن مادة...",
                        type="text",
                        className="mb-3"
                    ),
                    dcc.Checklist(
                        id='passed-courses-checklist',
                        options=course_options,
                        value=[],
                        labelClassName="d-block"
                    ),
                    dbc.Button('عرض المواد المتاحة لي', id='submit-button', n_clicks=0, color="primary", className="mt-3")
                ])
            ])
        ], width=12, md=5),

        # --- العمود الأيمن: المخرجات ---
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("الخطوة 2: المواد التي يمكنك تسجيلها")),
                dbc.CardBody(
                    dcc.Loading(type="circle", children=html.Div(id='available-courses-output'))
                )
            ])
        ], width=12, md=7)
    ], className="mb-4"),

    # --- الصف الرابع: خريطة المواد التفاعلية ---
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("خريطة الخطة الدراسية")),
                dbc.CardBody(
                    dcc.Loading(type="circle", children=
                        cyto.Cytoscape(
                            id='cytoscape-graph',
                            elements=cytoscape_elements,
                            style={'width': '100%', 'height': '450px'},
                            layout={
                                'name': 'cose',
                                'idealEdgeLength': 100,
                                'nodeRepulsion': 400000,
                            }
                        )
                    )
                )
            ])
        ], width=12)
    ])
], fluid=True)