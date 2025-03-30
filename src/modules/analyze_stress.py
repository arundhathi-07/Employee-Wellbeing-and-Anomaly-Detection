import os
import pandas as pd
from datetime import datetime

def analyze_stress():
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    data_folder = "src/data"
    file_path = os.path.join(data_folder, f"{today}.csv")
    
    if not os.path.exists(file_path):
        print("No data available for today.")
        return
    
    # Load CSV data
    df = pd.read_csv(file_path)
    
    # Calculate stress indicators
    avg_blink_rate = df['Eye Blinks'].mean()
    bad_posture_count = df[df['Posture'] == 'Bad'].shape[0]
    disengaged_count = df[df['Engagement'] == 'Disengaged'].shape[0]
    
    print("\n[STRESS ANALYSIS REPORT]")
    print(f"Total Records: {len(df)}")
    print(f"Average Eye Blink Rate: {avg_blink_rate:.2f}")
    print(f"Instances of Bad Posture: {bad_posture_count}")
    print(f"Instances of Disengagement: {disengaged_count}")
    
    # Define stress levels based on collected data
    stress_level = "Low"
    if bad_posture_count > len(df) * 0.4 or disengaged_count > len(df) * 0.4:
        stress_level = "High"
    elif bad_posture_count > len(df) * 0.2 or disengaged_count > len(df) * 0.2:
        stress_level = "Moderate"
    
    print(f"Overall Stress Level: {stress_level}")
    
if __name__ == "__main__":
    analyze_stress()
