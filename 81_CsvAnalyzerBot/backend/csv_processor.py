import pandas as pd
from typing import Optional, Dict, Any
import io

class CSVProcessor:
    def __init__(self):
        self.df: Optional[pd.DataFrame] = None
        self.file_path: Optional[str] = None

    def load_csv(self, file_path: str) -> bool:
        try:
            self.df = pd.read_csv(file_path)
            self.file_path = file_path
            return True
        except Exception as e:
            print(f"Error loading CSV: {e}")
            self.df = None
            self.file_path = None
            return False

    def get_dataframe(self) -> Optional[pd.DataFrame]:
        return self.df

    def get_column_names(self) -> list[str]:
        return self.df.columns.tolist() if self.df is not None else []

    def get_summary_statistics(self) -> Dict[str, Any]:
        if self.df is None:
            return {}
        return self.df.describe(include='all').to_dict()

    def get_head(self, n: int = 5) -> Dict[str, Any]:
        if self.df is None:
            return {}
        return self.df.head(n).to_dict()

    def get_info(self) -> str:
        if self.df is None:
            return "No DataFrame loaded."
        buffer = io.StringIO()
        self.df.info(buf=buffer)
        return buffer.getvalue()

    def run_query(self, query_code: str) -> Optional[pd.DataFrame]:
        if self.df is None:
            return None
        try:
            # Use a dictionary to provide context for `eval`
            local_vars = {'df': self.df, 'pd': pd}
            result = eval(query_code, {"__builtins__": {}}, local_vars)
            if isinstance(result, pd.DataFrame):
                return result
            elif isinstance(result, pd.Series):
                return result.to_frame()
            else:
                return pd.DataFrame({'result': [result]})
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
