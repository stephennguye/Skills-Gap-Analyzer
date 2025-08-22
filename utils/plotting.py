import plotly.graph_objects as go


def circular_gauge(skill: str, value: float) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=round(value * 100, 1),
            title={"text": skill.title()},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"thickness": 0.3},
                "steps": [
                    {"range": [0, 40]},
                    {"range": [40, 70]},
                    {"range": [70, 100]},
                ],
            },
            number={"suffix": "%"},
        )
    )
    fig.update_layout(height=240, margin=dict(l=10, r=10, t=50, b=10))
    return fig


def overall_gauge(value: float) -> go.Figure:
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=round(value * 100, 1),
            title={"text": "Overall Skill Match"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"thickness": 0.4},
                "steps": [
                    {"range": [0, 40]},
                    {"range": [40, 70]},
                    {"range": [70, 100]},
                ],
            },
            number={"suffix": "%"},
        )
    )
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig

