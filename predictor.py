import os
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

DATA_PATH = "data/historical_Hanoi_weather.csv"
MODEL_DIR = "models"
REG_MODEL_PATH = os.path.join(MODEL_DIR, "multioutput_regression_model.pkl")
CLS_MODEL_PATH = os.path.join(MODEL_DIR, "weather_condition_classifier.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "label_encoder.pkl")

def load_models():
    if not (os.path.exists(REG_MODEL_PATH) and os.path.exists(CLS_MODEL_PATH) and os.path.exists(ENCODER_PATH)):
        raise FileNotFoundError("Models or encoder not found. Please train models first.")
    reg_model = joblib.load(REG_MODEL_PATH)
    cls_model = joblib.load(CLS_MODEL_PATH)
    label_encoder = joblib.load(ENCODER_PATH)
    return reg_model, cls_model, label_encoder

def predict_weather(day_of_year):
    reg_model, cls_model, label_encoder = load_models()
    
    X_pred = pd.DataFrame([[day_of_year]], columns=['dayofyear'])
    
    # Dự đoán giá trị liên tục
    reg_preds = reg_model.predict(X_pred)[0]
    temp, humidity, pressure, windspeed = reg_preds
    
    # Dự đoán nhãn phân loại
    cls_pred = cls_model.predict(X_pred)[0]
    
    print("Class predicted (encoded):", cls_pred)
    print("Label classes:", label_encoder.classes_)
    
    try:
        condition = label_encoder.inverse_transform([cls_pred])[0]
    except Exception as e:
        print("Error decoding condition:", e)
        condition = "Unknown"
    
    return {
        "tavg": temp,
        "humidity": humidity,
        "pressure": pressure,
        "windspeed": windspeed,
        "condition": condition
    }


def train_models():
    df = pd.read_csv(DATA_PATH)
    print("Columns in CSV:", df.columns.tolist())
    df['date'] = pd.to_datetime(df['datetime'], errors='coerce')
    df['dayofyear'] = df['date'].dt.dayofyear

    # Loại bỏ hàng thiếu dữ liệu quan trọng
    df = df.dropna(subset=['dayofyear', 'temp', 'humidity', 'sealevelpressure', 'windspeed', 'conditions'])

    # Feature
    X = df[['dayofyear']]

    # Targets cho hồi quy
    y_reg = df[['temp', 'humidity', 'sealevelpressure', 'windspeed']]

    # Target phân loại
    y_cls = df['conditions']

    # Mã hóa nhãn phân loại
    le = LabelEncoder()
    y_cls_encoded = le.fit_transform(y_cls)

    # Train multi-output regression
    X_train_reg, X_test_reg, y_train_reg, y_test_reg = train_test_split(X, y_reg, test_size=0.2, random_state=42)
    reg_model = MultiOutputRegressor(LinearRegression())
    reg_model.fit(X_train_reg, y_train_reg)
    print("Regression model trained.")

    # Train classification
    X_train_cls, X_test_cls, y_train_cls, y_test_cls = train_test_split(X, y_cls_encoded, test_size=0.2, random_state=42)
    cls_model = LogisticRegression(max_iter=200)
    cls_model.fit(X_train_cls, y_train_cls)
    print("Classification model trained.")

    # Tạo thư mục lưu model nếu chưa có
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Lưu model và encoder
    joblib.dump(reg_model, REG_MODEL_PATH)
    joblib.dump(cls_model, CLS_MODEL_PATH)
    joblib.dump(le, ENCODER_PATH)

    print(f"Models and encoder saved to {MODEL_DIR}")

if __name__ == "__main__":
    train_models()
