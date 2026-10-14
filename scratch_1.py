import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

revenues = pd.read_csv("company_quarterly_revenue_raw.csv")
print(f"\nrevenues: shape = {revenues.shape[0]} rows x {revenues.shape[1]} columns")
print(revenues.head())
print("\n")

orders = pd.read_csv("orders.csv")
print(f"\norders: shape = {orders.shape[0]} rows x {orders.shape[1]} columns")
print(orders.head())
print("\n")

shipments = pd.read_csv("shipments.csv")
print(f"\nshipments: shape = {shipments.shape[0]} rows x {shipments.shape[1]} columns")
print(shipments.head())
print("\n")

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(17, 4))

pd.Series(revenues.drop(columns="company").to_numpy().ravel()).plot(kind="hist", bins=10, edgecolor="black", ax=ax1)
ax1.set_title("revenues: all quarter columns")
ax1.set_xlabel("Revenue")

orders["amount"].plot(kind="hist", bins=8, edgecolor="black", ax=ax2)
ax2.set_title("orders: amount")
ax2.set_xlabel("Amount")

shipments["order_id"].value_counts().plot(kind="hist", bins=[0.5, 1.5, 2.5, 3.5], edgecolor="black", ax=ax3)
ax3.set_title("shipments: rows per order_id")
ax3.set_xlabel("Shipment rows per order_id")
ax3.set_xticks([1, 2, 3])

plt.tight_layout()
plt.savefig("Step 0")

# Revenues is wide because the 12 quarters are column headers. Each variable is not a column.  Revenue is a variable but it is in different spots along the 12 columns.
# Each observation is not a row so it fails rule 2. Each row holds 12 observations.
# Rule 3 is good because every cell has a revenue number.

rev_long = revenues.melt(id_vars="company", var_name="quarter", value_name="revenue")
print(f"rev_long: shape = {rev_long.shape[0]} rows x {rev_long.shape[1]} columns")
print(rev_long.head())

print("orders unique:", orders["order_id"].is_unique, "| duplicates:", orders["order_id"].duplicated().sum())
print("shipments unique:", shipments["order_id"].is_unique, "| duplicates:", shipments["order_id"].duplicated().sum())

# order_id is unique in orders.csv (20 rows, 20 distinct) but not unique in shipments.csv(35 rows, 20 distinct, 15 duplicates)
# Each order can have several shipments, so orders -> shipments is a one-to-many join.
# Every order's row will repeat once per shipment,
# so I expect the joined table to have 35 rows, not 20.

joined = orders.merge(shipments, on="order_id", how="left", validate="1:m")
print(f"joined: shape = {joined.shape[0]} rows x {joined.shape[1]} columns")
print("\n")

mean_joined = joined.groupby("customer_id")["amount"].mean()
print(mean_joined)

mean_orders = orders.groupby("customer_id")["amount"].mean()
print(mean_joined)

ships_per_order = shipments.groupby("order_id").size().rename("n_shipments").reset_index()
orders_ship = orders.merge(ships_per_order, on="order_id", how="left", validate="1:1")

orders_cq = orders_ship.groupby(["company", "quarter"], as_index=False).agg(
    n_orders=("order_id", "nunique"),
    order_amount_total=("amount", "sum"),
    n_shipments=("n_shipments", "sum"))

final = rev_long.merge(orders_cq, on=["company", "quarter"], how="left", validate="1:1")
cols = ["n_orders", "order_amount_total", "n_shipments"]
final[cols] = final[cols].fillna(0).astype(int)

final = final.sort_values(["company", "quarter"]).reset_index(drop=True)
print(f"final: shape = {final.shape[0]} rows x {final.shape[1]} columns")
print(final.head())


plt.figure(figsize=(13, 5))

plt.subplot(1, 2, 1)
all_revenue = revenues.drop(columns="company").values.flatten()
plt.hist(all_revenue, bins=10, edgecolor="black")
plt.title("All revenue values")
plt.xlabel("Revenue")
plt.ylabel("Count")

plt.subplot(1, 2, 2)
sns.lineplot(data=final, x="quarter", y="revenue", hue="company", marker="o")
plt.title("Revenue by company over time")
plt.xticks(rotation=60)

plt.tight_layout()
plt.savefig("Side-By-Side:Step 5")
