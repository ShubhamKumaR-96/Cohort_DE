# scripts/generate_data.py

import pandas as pd
from faker import Faker
import random
import os
from datetime import datetime

# Faker object banao - Indian locale
fake = Faker('en_IN')

random.seed(42)
fake.seed_instance(42)

# =============================================
# CONSTANTS — Data options
# =============================================
PRODUCTS = [
    {"name": "Laptop",      "category": "Electronics", "price": 55000},
    {"name": "Mouse",       "category": "Electronics", "price": 499},
    {"name": "Keyboard",    "category": "Electronics", "price": 999},
    {"name": "Desk Chair",  "category": "Furniture",   "price": 8500},
    {"name": "Notebook",    "category": "Stationery",  "price": 120},
    {"name": "Pen Set",     "category": "Stationery",  "price": 250},
    {"name": "Monitor",     "category": "Electronics", "price": 18000},
    {"name": "Headphones",  "category": "Electronics", "price": 2999},
]

CITIES = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", 
          "Ludhiana", "Chennai", "Kolkata", "Pune"]

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]

STATUS = ["Completed", "Completed", "Completed", "Returned", "Pending"]

# =============================================
# MAIN FUNCTION — Data generate
# =============================================
def generate_sales_data(num_records=500):
    """
    500 fake sales records generate karta hai
    """
    print(f"[INFO] Generating {num_records} sales records...")
    
    records = []
    
    for i in range(1, num_records + 1):
        # Random product choose 
        product = random.choice(PRODUCTS)
        
        # Quantity aur discount
        quantity = random.randint(1, 5)
        discount_pct = random.choice([0, 0, 0, 5, 10, 15, 20])
        
        # Price calculation
        unit_price = product["price"]
        discount_amt = round(unit_price * discount_pct / 100, 2)
        total_price = round((unit_price - discount_amt) * quantity, 2)
        
        # Record 
        record = {
            "order_id":         f"ORD-{i:04d}",           # ORD-0001
            "order_date":       fake.date_between(          # Random date
                                    start_date="-1y", 
                                    end_date="today"
                                ),
            "customer_name":    fake.name(),
            "customer_email":   fake.email(),
            "city":             random.choice(CITIES),
            "product_name":     product["name"],
            "category":         product["category"],
            "quantity":         quantity,
            "unit_price":       unit_price,
            "discount_pct":     discount_pct,
            "discount_amount":  discount_amt,
            "total_price":      total_price,
            "payment_method":   random.choice(PAYMENT_METHODS),
            "status":           random.choice(STATUS),
        }
        
        records.append(record)
    
    return pd.DataFrame(records)


# =============================================
# DIRTY DATA — Intentionally problems add 
# =============================================
def add_dirty_data(df):
    """
    Real world jaisi problems add karta hai
    Taaki hum baad mein clean kar sakein
    """
    print("[INFO] Adding real-world data issues...")
    
    dirty_df = df.copy()
    total = len(dirty_df)
    
    # 1. Kuch emails NULL karo (~3%)
    null_email_idx = random.sample(range(total), int(total * 0.03))
    dirty_df.loc[null_email_idx, 'customer_email'] = None
    
    # 2. Kuch prices negative karo - data entry error (~2%)
    neg_price_idx = random.sample(range(total), int(total * 0.02))
    dirty_df.loc[neg_price_idx, 'unit_price'] = -999
    
    # 3. Kuch order dates future ki karo - impossible dates (~1%)
    future_idx = random.sample(range(total), int(total * 0.01))
    dirty_df.loc[future_idx, 'order_date'] = "2099-01-01"
    
    # 4. Duplicate rows add karo (~2%)
    dup_idx = random.sample(range(total), int(total * 0.02))
    duplicates = dirty_df.iloc[dup_idx]
    dirty_df = pd.concat([dirty_df, duplicates], ignore_index=True)
    
    # 5. City names inconsistent karo
    dirty_df['city'] = dirty_df['city'].apply(
        lambda x: x.upper() if random.random() < 0.1 else x
        # 10% cities UPPERCASE hongi — inconsistency!
    )
    
    print(f"[INFO] Dirty data stats:")
    print(f"       - Null emails:      {dirty_df['customer_email'].isna().sum()}")
    print(f"       - Negative prices:  {(dirty_df['unit_price'] < 0).sum()}")
    print(f"       - Duplicate rows:   {dirty_df.duplicated().sum()}")
    print(f"       - Total records:    {len(dirty_df)}")
    
    return dirty_df


# =============================================
# SAVE — CSV file mein save karo
# =============================================
def save_data(df, filename):
    # ✅ FIX — absolute path u
    script_dir = os.path.dirname(os.path.abspath(__file__))  # scripts/ folder
    project_root = os.path.dirname(script_dir)               # sales_pipeline/ folder
    output_path = os.path.join(project_root, "data", "raw", filename)
    
    # Folder na ho to automatically bana do
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Data saved to: {output_path}")
    print(f"[INFO] Shape: {df.shape[0]} rows × {df.shape[1]} columns")


# =============================================
# MAIN — Script 
# =============================================
if __name__ == "__main__":
    print("=" * 50)
    print("   SALES DATA GENERATOR")
    print("=" * 50)
    
    # Step 1: Clean data generate
    clean_df = generate_sales_data(num_records=500)
    
    # Step 2: Dirty data add 
    dirty_df = add_dirty_data(clean_df)
    
    # Step 3: Save 
    save_data(dirty_df, "sales_raw.csv")
    
    print("=" * 50)
    print("[DONE] Raw data generation complete!")
    print("=" * 50)