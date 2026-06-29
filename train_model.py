import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score
)
from sklearn.ensemble import RandomForestClassifier

# ---------------- LOAD DATA ---------------- #

df = pd.read_csv("upi_fraud_dataset.csv")

print("\nDataset Loaded Successfully\n")

# ---------------- ENCODE CATEGORICAL FEATURES ---------------- #

categorical_columns = [

    "sender_bank",

    "receiver_bank",

    "location",

    "device",

    "transaction_type"

]

encoders = {}

for column in categorical_columns:

    encoder = LabelEncoder()

    df[column] = encoder.fit_transform(df[column])

    encoders[column] = encoder

# ---------------- FEATURES ---------------- #

X = df.drop("fraud", axis=1)

y = df["fraud"]

# ---------------- TRAIN TEST SPLIT ---------------- #

X_train, X_test, y_train, y_test = train_test_split(

    X,

    y,

    test_size=0.20,

    random_state=42,

    stratify=y

)

# ---------------- MODEL ---------------- #

model = RandomForestClassifier(

    n_estimators=250,

    max_depth=12,

    random_state=42,

    class_weight="balanced"

)

model.fit(X_train, y_train)

# ---------------- PREDICTION ---------------- #

prediction = model.predict(X_test)

probability = model.predict_proba(X_test)[:,1]

# ---------------- METRICS ---------------- #

accuracy = accuracy_score(y_test,prediction)

precision = precision_score(y_test,prediction)

recall = recall_score(y_test,prediction)

f1 = f1_score(y_test,prediction)

roc = roc_auc_score(y_test,probability)

print("\n------------------------------")

print("MODEL PERFORMANCE")

print("------------------------------\n")

print(f"Accuracy : {accuracy:.4f}")

print(f"Precision : {precision:.4f}")

print(f"Recall : {recall:.4f}")

print(f"F1 Score : {f1:.4f}")

print(f"ROC AUC : {roc:.4f}")

print("\nClassification Report\n")

print(classification_report(

    y_test,

    prediction

))

print("\nConfusion Matrix\n")

print(confusion_matrix(

    y_test,

    prediction

))

# ---------------- FEATURE IMPORTANCE ---------------- #

importance = pd.DataFrame({

    "Feature":X.columns,

    "Importance":model.feature_importances_

})

importance = importance.sort_values(

    by="Importance",

    ascending=False

)

print("\nTop Important Features\n")

print(importance)

# ---------------- SAVE MODEL ---------------- #

os.makedirs(

    "models",

    exist_ok=True

)

joblib.dump(

    model,

    "models/fraud_model.pkl"

)

joblib.dump(

    encoders,

    "models/label_encoders.pkl"

)

print("\nModel Saved Successfully")

print("models/fraud_model.pkl")

print("models/label_encoders.pkl")