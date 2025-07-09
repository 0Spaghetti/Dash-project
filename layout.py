from dash import dcc, html
import dash_bootstrap_components as dbc
import dash_cytoscape as cyto
from data import course_options, cytoscape_elements

# تعريف متغير الواجهة
layout = dbc.Container([
    # --- وحدة التخزين لحفظ اختيارات المستخدم ---
    dcc.Store(id='local-storage', storage_type='local'),

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
                 html.Li("التظليل الخفيف (opacity): مادة مكتملة."),
                 html.Li("الإطار الأصفر: مادة متاحة للتسجيل."),
            ]),
        ]),
    ], id="about-modal", is_open=False),

    # --- الصف الأول: الرسوم البيانية ---
    dbc.Row([
        dbc.Col(dcc.Loading(type="circle", children=
            dbc.Card([
                dbc.CardHeader("نسبة إنجاز الخطة"),
                dcc.Graph(id='progress-pie-chart')
            ])
        ), width=12, md=6, className="mb-4"),
        
        dbc.Col(dcc.Loading(type="circle", children=[
            dbc.Card([
                dbc.CardHeader("ملخص الوحدات المعتمدة"),
                dbc.CardBody([
                    dcc.Graph(id='credits-bar-chart'),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col(dbc.Card(id='passed-hours-card', color="success", inverse=True, className="text-center p-2 mb-2")),
                        dbc.Col(dbc.Card(id='remaining-hours-card', color="warning", inverse=True, className="text-center p-2 mb-2")),
                        dbc.Col(dbc.Card(id='percentage-card', color="info", inverse=True, className="text-center p-2 mb-2")),
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
                    dbc.Tabs([
                        dbc.Tab(label="مواد عامة", tab_id="tab-general"),
                        dbc.Tab(label="مواد أساسية", tab_id="tab-core"),
                        dbc.Tab(label="مواد اختيارية", tab_id="tab-elective"),
                    ], id="course-tabs", active_tab="tab-general", className="mt-3"),
                    
                    html.Div(id='checklist-container', style={'maxHeight': '300px', 'overflowY': 'auto', 'marginTop': '10px'}),
                    
                    dbc.Row([
                        dbc.Col(dbc.Button('عرض المواد المتاحة لي', id='submit-button', color="primary", className="w-100"), width=8),
                        dbc.Col(dbc.Button('مسح', id='clear-button', color="secondary", outline=True, className="w-100"), width=4),
                    ], className="mt-3")
                ])
            ], style={'height': '100%'})
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
        dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Row([
                            dbc.Col(html.H4("خريطة الخطة الدراسية"), width=6),
                            dbc.Col(
                                dbc.RadioItems(
                                    id='layout-selector',
                                    options=[
                                        {'label': 'شجري (Dagre)', 'value': 'dagre'},
                                        {'label': 'عرضي (Breadthfirst)', 'value': 'breadthfirst'},
                                        {'label': 'دائري (Circle)', 'value': 'circle'},
                                        {'label': 'شبكي (Grid)', 'value': 'grid'},
                                    ],
                                    value='dagre',  # القيمة الافتراضية
                                    inline=True,
                                    labelClassName="p-2",
                                    inputClassName="mx-1",
                                ),
                                width=6,
                                className="d-flex justify-content-end align-items-center"
                            ),
                        ])
                    ),
                    dbc.CardBody(
                        dcc.Loading(type="circle", children=
                            cyto.Cytoscape(
                                id='cytoscape-graph',
                                elements=cytoscape_elements,
                                style={'width': '100%', 'height': '500px'},
                                # تم حذف خاصية 'layout' من هنا، ستتم إضافتها عبر الـ callback
                            )
                        )
                    )
                ])
            ], width=12, md=9),
        
            dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H5("تفاصيل المادة")),
                dbc.CardBody(id="course-details-output", style={'minHeight': '500px'})
            ])
        ], width=12, md=3)
    ])
], fluid=True)