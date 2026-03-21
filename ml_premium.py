"""
Collective Alibi — Dynamic Premium ML Model
Trains an XGBoost model to predict personalised weekly premiums
Run: python ml_premium.py
"""
import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import json, pickle, os

# ── Generate synthetic training data ─────────────────────────
np.random.seed(42)
N = 5000

zone_risks = {
    "Kurla":8, "Dharavi":9, "Andheri":5, "Bandra":3,
    "Koramangala":2, "Connaught":4, "Jubilee":2, "Whitefield":1
}

def generate_data(n):
    zones = np.random.choice(list(zone_risks.keys()), n)
    zone_risk = np.array([zone_risks[z] for z in zones])
    avg_daily  = np.random.uniform(500, 1500, n)
    monsoon    = np.random.randint(0, 2, n)
    claim_hist = np.random.randint(0, 20, n)
    account_age_weeks = np.random.randint(1, 200, n)

    base = np.where(avg_daily > 1000, 79, np.where(avg_daily > 700, 49, 29))
    premium = (base + zone_risk * .8 + monsoon * 6
               - np.minimum(claim_hist // 5, 10)
               - np.minimum(account_age_weeks // 52, 5)
               + np.random.normal(0, 2, n))
    premium = np.clip(premium, 19, 99)

    return pd.DataFrame({
        "zone_risk": zone_risk, "avg_daily_earning": avg_daily,
        "is_monsoon": monsoon, "claim_history": claim_hist,
        "account_age_weeks": account_age_weeks, "premium": premium,
    })

df = generate_data(N)
X = df.drop("premium", axis=1)
y = df["premium"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBRegressor(n_estimators=200, max_depth=4, learning_rate=0.05, random_state=42)
model.fit(X_train, y_train)

preds = model.predict(X_test)
mae = mean_absolute_error(y_test, preds)
print(f"Model trained — MAE: ₹{mae:.2f}/week")

os.makedirs("models", exist_ok=True)
with open("models/premium_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved to models/premium_model.pkl")

# ── Prediction function ──────────────────────────────────────
def predict_premium(zone_risk: int, avg_daily: float, is_monsoon: bool,
                    claim_history: int, account_age_weeks: int) -> dict:
    with open("models/premium_model.pkl", "rb") as f:
        m = pickle.load(f)
    features = pd.DataFrame([{
        "zone_risk": zone_risk, "avg_daily_earning": avg_daily,
        "is_monsoon": int(is_monsoon), "claim_history": claim_history,
        "account_age_weeks": account_age_weeks,
    }])
    raw = float(m.predict(features)[0])
    rounded = round(raw / 5) * 5
    return {"recommended_premium": max(19, min(99, rounded)), "raw_score": round(raw, 2)}

if __name__ == "__main__":
    examples = [
        (8, 900, True, 0, 4, "New rider, Kurla, monsoon"),
        (5, 900, True, 10, 52, "1yr rider, Andheri, monsoon"),
        (2, 1200, False, 5, 104, "2yr rider, Koramangala, dry season"),
    ]
    print("\nSample predictions:")
    for zone_r, earn, monsoon, claims, age, desc in examples:
        result = predict_premium(zone_r, earn, monsoon, claims, age)
        print(f"  {desc}: ₹{result['recommended_premium']}/week")
