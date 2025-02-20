import pandas as pd
from datetime import datetime
import os
from typing import Dict, Any
from constants import DATABASE_FILE

def save_lead_data(lead_data: Dict[str, Any], analysis_result: str) -> None:
    """Save lead data and analysis to CSV"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df = pd.DataFrame([{
        'timestamp': now,
        **lead_data,
        'analysis': analysis_result
    }])

    if os.path.exists(DATABASE_FILE):
        df.to_csv(DATABASE_FILE, mode='a', header=False, index=False)
    else:
        df.to_csv(DATABASE_FILE, index=False)

def load_lead_history() -> pd.DataFrame:
    """Load lead history from CSV"""
    if os.path.exists(DATABASE_FILE):
        return pd.read_csv(DATABASE_FILE)
    return pd.DataFrame()