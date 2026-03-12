import pandas as pd
from app.core.config import DATA_PATH

def load_dataset(path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df