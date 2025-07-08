from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from data import course_options, cytoscape_elements

# تعريف متغير الواجهة
layout = dbc.Container([
    # --- شريط التنقل العلوي ---
    dbc.NavbarSimple(
        brand="مخطط المسار الدراسي 🎓",
        children=[dbc.Button("دليل الاستخدام", id="open-about-modal", color="light", outline=True)],
        color="primary",
        dark=True,
        className="mb-4",
    ),
    
    # --- النافذة المنبثقة المخفية ---
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("دليل استخدام المخطط")),
        dbc.ModalBody([
            html.H5("مفتاح ألوان الخريطة:"),
            html.Ul([
                html.Li([html.Span("■", style={'color': '#904694'}), " مادة أساسية"]),
                html.Li([html.Span("■", style={'color': '#2ab472'}), " مادة اختيارية"]),
                html.Li([html.Span("■", style={'color': '#00aae2'}), " مادة عامة"]),
            ]),
            html.Hr(),
            html.H5("حالة المواد:"),
            html.Ul([
                 html.Li("التظليل الخفيف (opacity): مادة مكتملة حاليًا."),
            ]),
        ]),
    ], id="about-modal", is_open=False),

    # --- الصف الأول: الرسوم البيانية ---
    dbc.Row([
        dbc.Col(dcc.Loading(type="circle", children=dbc.Card(dcc.Graph(id='progress-pie-chart'))), width=12, md=6, className="mb-4"),
        dbc.Col(dcc.Loading(type="circle", children=[
                dbc.Card([
                    dbc.CardHeader("ملخص الساعات المعتمدة"),
                    dbc.CardBody([
                        dcc.Graph(id='credits-bar-chart'),
                        html.Hr(),
                        dbc.Row([
                            dbc.Col(dbc.Card(id='passed-hours-card', className="text-center p-2")),
                            dbc.Col(dbc.Card(id='remaining-hours-card', className="text-center p-2")),
                            dbc.Col(dbc.Card(id='percentage-card', className="text-center p-2")),
                        ]),
                    ])
                ])
            ]), width=12, md=6, className="mb-4")
    ]),

    # --- الصف الثاني: الإدخال والنتائج ---
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("الخطوة 1: حدد المواد التي نجحت فيها")),
                dbc.CardBody([
                    dbc.Input(id="course-search-input", placeholder="ابحث عن مادة...", type="text", className="mb-3"),
                    html.Div([
                        dcc.Checklist(
                            id='passed-courses-checklist',
                            options=course_options,
                            value=[],
                            labelClassName="d-block"
                        )
                    ], style={'maxHeight': '300px', 'overflowY': 'auto'}),
                    dbc.Button('عرض المواد المتاحة لي', id='submit-button', n_clicks=0, color="primary", className="mt-3 w-100")
                ])
            ], style={'height': '100%'}) # لضمان تناسق الارتفاع
        ], width=12, md=5),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("الخطوة 2: المواد التي يمكنك تسجيلها")),
                dbc.CardBody(dcc.Loading(type="circle", children=html.Div(id='available-courses-output')), style={'minHeight': '450px'})
            ])
        ], width=12, md=7)
    ], className="mb-4"),

    # --- الصف الثالث: خريطة المواد وتفاصيلها ---
    dbc.Row([
        # --- عمود الخريطة ---
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4("خريطة الخطة الدراسية")),
                dbc.CardBody(
                    dcc.Loading(type="circle", children=
                        cyto.Cytoscape(
                            id='cytoscape-graph',
                            elements=cytoscape_elements,
                            style={'width': '100%', 'height': '500px'},
                            layout={'name': 'dagre', 'spacingFactor': 1.2, 'roots': '[id = "ITGS211"], [id = "ITGS223"], [id = "ITGS215"], [id = "ITGS224"], [id = "ITGS226"], [id = "ITGS228"]'}
                        )
                    )
                )
            ])
        ], width=12, md=9),
        
        # --- عمود تفاصيل المادة ---
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("تفاصيل المادة")),
                dbc.CardBody(id="course-details-output", style={'minHeight': '500px'})
            ])
        ], width=12, md=3)
    ])
], fluid=True)