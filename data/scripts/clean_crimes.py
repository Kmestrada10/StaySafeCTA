import pandas as pd
from datetime import datetime, timedelta

def clean_crime_data(input_path, output_path):
    """
    Processes raw crime data to focus on violent crimes near CTA routes.
    
    Args:
        input_path (str): Path to raw crime data CSV
        output_path (str): Path to save cleaned data
    """
    # Load raw data
    crimes = pd.read_csv(input_path)
    
    # 1. Filter by date (last 30 days)
    crimes['date'] = pd.to_datetime(crimes['date'])
    recent_crimes = crimes[crimes['date'] >= (datetime.now() - timedelta(days=30))]
    
    # 2. Filter violent crime types
    violent_types = ['BATTERY', 'ASSAULT', 'ROBBERY', 'HOMICIDE']
    violent_crimes = recent_crimes[recent_crimes['primary_type'].isin(violent_types)]
    
    # 3. Select relevant columns
    cols_to_keep = [
        'date',
        'primary_type',
        'description',
        'location_description',
        'arrest',
        'latitude',
        'longitude',
        'block',
        'beat',
        'district'
    ]
    cleaned = violent_crimes[cols_to_keep].copy()
    
    # 4. Add danger score (simple version)
    # Weight more severe crimes higher
    crime_weights = {
        'HOMICIDE': 4,
        'ROBBERY': 3, 
        'ASSAULT': 2,
        'BATTERY': 1
    }
    cleaned['danger_score'] = cleaned['primary_type'].map(crime_weights)
    
    # 5. Handle missing data
    cleaned = cleaned.dropna(subset=['latitude', 'longitude'])
    
    # Save cleaned data
    cleaned.to_csv(output_path, index=False)
    print(f"Saved cleaned data to {output_path}")
    print(f"Total violent crimes: {len(cleaned)}")

if __name__ == "__main__":
    # Example usage (update paths as needed)
    input_file = "../data/raw/crimes_raw_20240315_1420.csv"  # Update with your file
    output_file = "../data/processed/violent_crimes_cleaned.csv"
    
    clean_crime_data(input_file, output_file)