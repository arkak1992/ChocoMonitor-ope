import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt

def ensure_directory(output_folder):
    today_folder = datetime.date.today().strftime("%Y-%m-%d")
    full_path = os.path.join(output_folder, today_folder)
    os.makedirs(full_path, exist_ok=True)
    return full_path

def calculate_temper_index(df):
    """حساب مؤشر الحرارة كقيمة من 0 إلى 10"""
    avg_temp = df['Temperature (°C)'].mean()
    return round(max(0, min(10, (avg_temp - 15) / 3.5)), 1)  # تأكد أن المؤشر بين 0 و 10

def analyze_and_save(csv_file, output_folder="results"):
    if not os.path.exists(csv_file):
        print(f"[ERROR] File {csv_file} not found.")
        return

    df = pd.read_csv(csv_file)
    if 'Time (s)' not in df.columns or 'Temperature (°C)' not in df.columns:
        print("[ERROR] CSV file does not contain required columns: 'Time (s)', 'Temperature (°C)'")
        return

    if df.empty:
        print("[ERROR] CSV file is empty.")
        return

    temper_index = calculate_temper_index(df)
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    start_temp = df['Temperature (°C)'].iloc[0]
    break_points = df[df['Temperature (°C)'].diff().abs() > 2]

    plt.figure(figsize=(3.35, 4.72), dpi=300)  # 85mm x 120mm

    plt.subplot(2, 1, 1)
    plt.plot(df['Time (s)'], df['Temperature (°C)'], label='Temperature', color='blue')
    plt.scatter(break_points['Time (s)'], break_points['Temperature (°C)'], color='red', label='Break Points')
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.text(0.1, 0.8, f"Start Temp: {start_temp}°C", fontsize=10)
    plt.text(0.1, 0.6, f"Date: {today}", fontsize=10)

    for i, row in break_points.iterrows():
        plt.text(0.1, max(0.1, 0.4 - (i * 0.1)), f"Break {i+1}: {row['Temperature (°C)']}°C at {row['Time (s)']}s", fontsize=8)

    plt.text(0.1, 0.05, f"Temper Index: {temper_index}/10", fontsize=12, fontweight='bold')
    plt.axis('off')

    save_path = os.path.join(ensure_directory(output_folder), f"result_{datetime.datetime.now().strftime('%H-%M-%S')}.png")
    plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"[SUCCESS] Analysis saved as PNG at: {save_path}")

if __name__ == "__main__":
    sample_csv = "data/2025-01-27/temperature_sample.csv"
    analyze_and_save(sample_csv)
