import pandas as pd
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

RAW_PATH =  os.path.join(project_root,"data","raw","sales_raw.csv")
CLEANED_PATH = os.path.join(project_root,"data","cleaned","sales_cleaned.csv")


# =============================================
# STEP 1 — Load data
# =============================================

def load_data(path):
    print("[INFO] Loading raw data")
    df = pd.read_csv(path)
    print(f"[INFO] Loaded shape: {df.shape[0]} rows × {df.shape[1]}columns")
    return df