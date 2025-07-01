import os
import pandas as pd
import matplotlib.pyplot as plt

# crear folders si no existen
os.makedirs("files/output", exist_ok=True)
os.makedirs("files/plots", exist_ok=True)

# leer archivos
drivers = pd.read_csv("files/input/drivers.csv")
timesheet = pd.read_csv("files/input/timesheet.csv")

# unir por driverId
df = pd.merge(drivers, timesheet, on="driverId")

# calcular pagos
def calcular_pago(row):
    if row["wage-plan"] == "hours":
        return row["hours-logged"] * 20
    else:
        return row["miles-logged"] * 0.5

df["pay"] = df.apply(calcular_pago, axis=1)

# agrupar por driver
summary = df.groupby(["driverId", "name"], as_index=False)[["hours-logged", "miles-logged", "pay"]].sum()

# guardar summary.csv
summary.to_csv("files/output/summary.csv", index=False)

# top 10 por salario
top10 = summary.sort_values(by="pay", ascending=False).head(10)

# plot
plt.figure(figsize=(10,6))
plt.bar(top10["name"], top10["pay"], color="orange")
plt.xticks(rotation=45)
plt.ylabel("Total Pay")
plt.title("Top 10 Drivers by Pay")
plt.tight_layout()
plt.savefig("files/plots/top10_drivers.png")

print("✅ summary.csv y top10_drivers.png generados correctamente")
