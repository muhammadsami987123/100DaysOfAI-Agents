import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio
import os
from pathlib import Path
from typing import Dict, Any, Optional

from backend.config import Config

class ChartGenerator:
    def __init__(self):
        self.charts_dir = Path(Config.CHARTS_DIR)
        self.charts_dir.mkdir(parents=True, exist_ok=True)

    def generate_chart(self, df: pd.DataFrame, chart_suggestion: Dict[str, Any]) -> Optional[str]:
        chart_type = chart_suggestion.get('type', '').lower()
        x_col = chart_suggestion.get('x')
        y_col = chart_suggestion.get('y')
        color_col = chart_suggestion.get('color')

        if not x_col or not y_col:
            print("Chart generation failed: Missing X or Y column.")
            return None

        # Basic validation of columns
        if x_col not in df.columns or y_col not in df.columns:
            print(f"Chart generation failed: One or more columns (X:{x_col}, Y:{y_col}) not found in DataFrame.")
            return None
        if color_col and color_col not in df.columns:
            print(f"Chart generation failed: Color column ({color_col}) not found in DataFrame.")
            return None

        fig = None
        if chart_type == 'bar chart':
            fig = px.bar(df, x=x_col, y=y_col, color=color_col, title=f'{y_col} by {x_col}')
        elif chart_type == 'line chart':
            fig = px.line(df, x=x_col, y=y_col, color=color_col, title=f'{y_col} over {x_col}')
        elif chart_type == 'scatter plot':
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f'{y_col} vs {x_col}')
        elif chart_type == 'histogram':
            fig = px.histogram(df, x=x_col, color=color_col, title=f'Distribution of {x_col}')
        elif chart_type == 'pie chart':
            fig = px.pie(df, names=x_col, values=y_col, title=f'Proportion of {y_col} by {x_col}')
        
        if fig:
            chart_filename = f"chart_{x_col}_{y_col}_{chart_type}_{os.urandom(4).hex()}.html" # HTML for interactivity
            chart_path = self.charts_dir / chart_filename
            pio.write_html(fig, file=str(chart_path), auto_open=False)
            return chart_filename
        
        print(f"Chart generation failed: Unsupported chart type {chart_type}")
        return None

    def save_matplotlib_chart(self, fig: plt.Figure, filename: str) -> str:
        filepath = self.charts_dir / filename
        fig.savefig(filepath)
        plt.close(fig) # Close the figure to free memory
        return str(filepath)
