from pathlib import Path

import torch
import torch.nn as nn
import numpy as np
import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

OUTPUT_STEPS = 72

BASE_DIR = Path(__file__).resolve().parent.parent


class TransformerModel(nn.Module):
    def __init__(self, input_dim, model_dim=128, num_heads=4, num_layers=4, dropout=0.2):
        super().__init__()
        self.input_proj = nn.Linear(input_dim, model_dim)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=model_dim, nhead=num_heads, dropout=dropout, batch_first=True)
        self.encoder = nn.TransformerEncoder(
            encoder_layer, num_layers=num_layers)
        self.decoder = nn.Sequential(
            nn.Linear(model_dim, 128),
            nn.ReLU(),
            nn.Linear(128, input_dim * OUTPUT_STEPS)
        )
        self.input_dim = input_dim
        self.output_steps = OUTPUT_STEPS

    def forward(self, x):
        x = self.input_proj(x)  # [B, input_steps, model_dim]
        x = self.encoder(x)     # [B, input_steps, model_dim]
        x = x[:, -1, :]         # берем последний таймстемп [B, model_dim]
        x = self.decoder(x)     # [B, input_dim * output_steps]
        # [B, output_steps, input_dim]
        x = x.view(-1, self.output_steps, self.input_dim)
        return x


def analyze(path_csv):
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    features = ['Температура, °С', 'Давление, мм рт. ст.',
                'Влажность, %', 'Скорость ветра, м/с', 'Направление ветра, °']

    scaler = joblib.load(BASE_DIR / "ml" / "scaler.pkl")

    model = TransformerModel(input_dim=len(features))
    model.load_state_dict(torch.load(
        BASE_DIR / "ml" / "m2.pth", map_location=DEVICE))
    model.to(DEVICE)
    model.eval()

    # === Загрузка новых данных ===
    # путь к новому файлу
    new_data = pd.read_csv(path_csv)
    new_data['Период'] = pd.to_datetime(new_data['Период'])
    new_data = new_data.sort_values('Период').dropna()
    new_data['Пост мониторинга'] = LabelEncoder(
    ).fit_transform(new_data['Пост мониторинга'])
    new_data = new_data.drop(columns=['NO2', 'O3', 'H2S', 'CO', 'SO2'])

    new_data[features] = scaler.transform(new_data[features])

    INPUT_STEPS = 72
    X_input = new_data[features].values[-INPUT_STEPS:].astype(np.float32)
    X_input = torch.tensor(X_input).unsqueeze(0).to(DEVICE)  # [1, 72, 5]

    with torch.no_grad():
        y_pred_scaled = model(X_input).squeeze(0).cpu().numpy()  # [72, 5]
    # Обратное масштабирование
    predicted = scaler.inverse_transform(y_pred_scaled)

    # Создание датафрейма для сохранения
    future_periods = pd.date_range(
        start=new_data['Период'].iloc[-1] + pd.Timedelta(minutes=20),
        periods=OUTPUT_STEPS,
        freq='20min'
    )

    df_pred = pd.DataFrame(predicted, columns=features)
    df_pred.insert(0, 'Период', future_periods)

    # Сохранение прогноза
    df_pred.to_csv("prediction.csv", index=False)
