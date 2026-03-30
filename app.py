import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# --- USER INPUT ---
weight = float(input("Enter your weight (kg): "))
height = float(input("Enter your height (cm): "))

# --- BMI ---
bmi = weight / ((height/100)**2)
print("Your BMI:", round(bmi, 2))

# --- DIET ---
if bmi > 25:
    print("Avoid: Fried Food, Sugar")
    print("Eat: Vegetables, Protein")
elif bmi < 18.5:
    print("Eat: Nuts, Milk, Rice")
else:
    print("Balanced diet")

# --- DATABASE ---
conn = sqlite3.connect("diet.db")
cursor = conn.cursor()

cursor.execute("SELECT MAX(day) FROM progress")
result = cursor.fetchone()[0]

day = 1 if result is None else result + 1

calories = float(input("Enter calories consumed today: "))

cursor.execute(
    "INSERT INTO progress (day, weight, calories) VALUES (?, ?, ?)",
    (day, weight, calories)
)

conn.commit()

# --- LOAD DATA ---
data = pd.read_sql_query("SELECT * FROM progress", conn)
conn.close()

# --- GRAPH ---
plt.plot(data["day"], data["weight"], marker='o')
plt.xlabel("Day")
plt.ylabel("Weight")
plt.title("Progress")
plt.show()

# --- EXCEL EXPORT ---
data.to_excel("progress.xlsx", index=False)

# --- MACHINE LEARNING ---
X = data[["calories"]]
y = data["weight"]

model = LinearRegression()
model.fit(X, y)

pred = model.predict([[2000]])
print("Predicted weight:", round(pred[0], 2))