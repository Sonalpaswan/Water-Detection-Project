# water_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Step 1: Load dataset
print("🔹 Loading dataset...")
df = pd.read_csv('water_potability.csv')

# Step 2: Handle missing values
print("🔹 Cleaning data (filling missing values)...")
df = df.fillna(df.mean())

# Step 3: Split data into features and labels
X = df.drop('Potability', axis=1)
y = df['Potability']

# Step 4: Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Step 5: Train model
print("🔹 Training model...")
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Step 6: Evaluate accuracy
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"✅ Model trained successfully!\nModel Accuracy: {acc*100:.2f}%")

# Step 7: Save model
joblib.dump(model, 'water_model.pkl')
print("💾 Model saved successfully as 'water_model.pkl'")
