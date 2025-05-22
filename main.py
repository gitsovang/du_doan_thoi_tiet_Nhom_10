import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from predictor import predict_weather
from tkinter import font

try:
    from tkcalendar import Calendar
except ImportError:
    Calendar = None

def on_predict():
    try:
        if calendar:
            selected_date = calendar.selection_get()
            day_of_year = selected_date.timetuple().tm_yday
        else:
            day_of_year = datetime.now().timetuple().tm_yday

        result = predict_weather(day_of_year)

        day = selected_date.day
        month = selected_date.strftime("%B")
        
        condition_raw = result.get('condition', None)

        condition_labels = [
            'Clear', 'Overcast', 'Partially cloudy', 'Rain', 
            'Rain, Overcast', 'Rain, Partially cloudy'
        ]

        condition_raw_clean = condition_raw.strip() if isinstance(condition_raw, str) else condition_raw
        condition_labels_clean = [c.strip() for c in condition_labels]


        if condition_raw_clean in condition_labels_clean:
            condition_text = condition_raw_clean
        else:
            condition_text = "Unknown"

        label_result.config(text=(
            f"Prediction for day {day}-{month}:\n" 
            f"Temperature: {result['tavg']:.2f} °C\n"
            f"Humidity: {result['humidity']:.2f} %\n"
            f"Pressure: {result['pressure']:.2f} hPa\n"
            f"Windspeed: {result['windspeed']:.2f} km/h\n"
            f"Condition: {condition_text}"
        ))
    except Exception as e:
        messagebox.showerror("Error", str(e))

window = tk.Tk()
window.title("Hanoi Weather Prediction")
window.geometry("400x550")
window.resizable(False, False)

title_font = font.Font(family="Helvetica", size=16, weight="bold")
label_font = font.Font(family="Helvetica", size=12)
button_font = font.Font(family="Helvetica", size=11, weight="bold")

title_label = tk.Label(window, text="Hanoi Weather Prediction", font=title_font, fg="#2C3E50")
title_label.pack(pady=(15, 10))

if Calendar:
    calendar = Calendar(window, selectmode='day')
    calendar.selection_set(datetime.now())
    calendar.pack(pady=10)
else:
    calendar = None
    info_label = tk.Label(window, text="tkcalendar not installed, using today's date", font=label_font)
    info_label.pack(pady=10)

btn_predict = tk.Button(window, text="Predict Weather", command=on_predict,
                        font=button_font, bg="#27AE60", fg="white",
                        activebackground="#1E8449", relief="flat")
btn_predict.pack(pady=20, ipadx=10, ipady=5)

label_result = tk.Label(window, text="", font=label_font, fg="#34495E", justify="center")
label_result.pack(pady=20, padx=20)

window.mainloop()
