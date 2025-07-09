import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px
from app import app

# Load and process data
df = pd.read_csv("student.csv")

# Custom grade ranges function
def get_grade(score):
    if score >= 85:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 55:
        return "C"
    elif score >= 40:
        return "D"
    else:
        return "F"

df["Grade"] = df["Score"].apply(get_grade)

# App setup

# Grading scale table component
grade_scale = html.Div([
    html.H3("📏 Grading Scale", style={"marginTop": "40px", "color": "#333"}),
    html.Table([
        html.Tbody([
            html.Tr([html.Td("A", style={"padding": "8px", "fontWeight": "bold"}), html.Td("85 and above", style={"padding": "8px"})]),
            html.Tr([html.Td("B", style={"padding": "8px", "fontWeight": "bold"}), html.Td("70 - 84", style={"padding": "8px"})]),
            html.Tr([html.Td("C", style={"padding": "8px", "fontWeight": "bold"}), html.Td("55 - 69", style={"padding": "8px"})]),
            html.Tr([html.Td("D", style={"padding": "8px", "fontWeight": "bold"}), html.Td("40 - 54", style={"padding": "8px"})]),
            html.Tr([html.Td("F", style={"padding": "8px", "fontWeight": "bold"}), html.Td("Below 40", style={"padding": "8px"})]),
        ])
    ], style={
        "width": "250px",
        "border": "1px solid #444",
        "borderCollapse": "collapse",
        "textAlign": "center",
        "marginTop": "10px",
        "marginLeft": "auto",
        "marginRight": "auto",
        "backgroundColor": "#fafafa",
        "boxShadow": "0 2px 6px rgba(0,0,0,0.1)"
    }),
])

# App layout
layout_app2 = html.Div(style={"fontFamily": "Arial, sans-serif", "padding": "30px", "backgroundColor": "#f5f5f5"}, children=[
    html.H1("🎓 Personal Student Dashboard", style={"textAlign": "center", "color": "#333"}),

    html.Label("👤 Select Student:", style={"fontSize": "18px", "marginTop": "20px"}),
    dcc.Dropdown(
        id="student-dropdown",
        options=[{"label": name, "value": name} for name in df["Name"].unique()],
        placeholder="Choose a student",
        style={"width": "60%", "margin": "auto", "marginBottom": "30px"}
    ),

    html.Div(id="student-charts"),

    grade_scale,
])

@app.callback(
    Output("student-charts", "children"),
    Input("student-dropdown", "value")
)
def display_student_data(selected_student):
    if not selected_student:
        return html.P("Please select a student to see their performance.", style={"fontSize": "18px", "textAlign": "center"})

    student_df = df[df["Name"] == selected_student]

    # Line chart for SemiFinal scores (out of 40)
    semi_fig = px.line(
        student_df, x="Subject", y="SemiFinal", markers=True,
        title=f"{selected_student}'s Semi-Final Scores (out of 40)",
        line_shape="linear", color_discrete_sequence=["#1f77b4"]
    )
    semi_fig.update_yaxes(range=[0, 40])

    # Line chart for Final scores (out of 60)
    final_fig = px.line(
        student_df, x="Subject", y="Final", markers=True,
        title=f"{selected_student}'s Final Exam Scores (out of 60)",
        line_shape="linear", color_discrete_sequence=["#ff7f0e"]
    )
    final_fig.update_yaxes(range=[0, 60])

    # Line chart for Total scores (out of 100)
    total_fig = px.line(
        student_df, x="Subject", y="Score", markers=True,
        title=f"{selected_student}'s Total Scores (out of 100)",
        line_shape="linear", color_discrete_sequence=["#2ca02c"]
    )
    total_fig.update_yaxes(range=[0, 100])

    # Pie chart for Grade Breakdown
    grade_colors = {
        "F": "red",
        "D": "orange",
        "C": "yellow",
        "B": "blue",
        "A": "green"
    }
    pie_fig = px.pie(
        student_df, names="Grade", title="Grade Breakdown",
        color="Grade",
        color_discrete_map=grade_colors
    )

    # Data Table for student details
    table = html.Table([
        html.Thead(html.Tr([html.Th(col, style={"backgroundColor": "#007acc", "color": "white", "padding": "8px"}) for col in student_df.columns])),
        html.Tbody([
            html.Tr([html.Td(student_df.iloc[i][col], style={"padding": "8px", "borderBottom": "1px solid #ddd"}) for col in student_df.columns])
            for i in range(len(student_df))
        ])
    ], style={"width": "100%", "marginTop": "20px", "borderCollapse": "collapse"})

    return html.Div(children=[
        dcc.Graph(figure=semi_fig),
        dcc.Graph(figure=final_fig),
        dcc.Graph(figure=total_fig),
        dcc.Graph(figure=pie_fig),
        html.H3("📋 Student Data Table", style={"marginTop": "20px"}),
        table
    ])

