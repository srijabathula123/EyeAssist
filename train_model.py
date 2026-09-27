import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


DATA_FILE = "eye_gesture_data.csv"
MODEL_FILE = "eye_gesture_model.pkl"


data = pd.read_csv(DATA_FILE)

print("Dataset loaded")
print("Total samples:", len(data))
print()

print("Gesture distribution:")
print(data["label"].value_counts())
print()


features = [
    "left_ear",
    "right_ear",
    "iris_x",
    "iris_y",
    "gaze_x",
    "gaze_y",
    "left_ratio_x",
    "right_ratio_x",
    "left_ratio_y",
    "right_ratio_y"
]

X = data[features]
y = data["label"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


print("Training Random Forest...")

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    max_depth=15
)

model.fit(X_train, y_train)


predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)


print()
print("================================")
print("RANDOM FOREST TRAINING COMPLETE")
print("================================")
print()

print(f"Accuracy: {accuracy * 100:.2f}%")

print()
print("Classification Report:")
print(
    classification_report(
        y_test,
        predictions
    )
)


with open(MODEL_FILE, "wb") as file:
    pickle.dump(model, file)


print()
print("Model saved successfully!")
print("File:", MODEL_FILE)