import numpy as np, pandas as pd, json, pathlib
np.random.seed(42)
root = pathlib.Path(__file__).parent
(root/"data").mkdir(exist_ok=True); (root/"results").mkdir(exist_ok=True)
cats = {"Electronics":(["Laptop","Headphones","Tablet"],[899,79,349]),"Home":(["Lamp","Chair","Kettle"],[49,129,39]),"Clothing":(["Jacket","Shoes","T-Shirt"],[89,69,25]),"Sports":(["Bike","Yoga Mat","Dumbbells"],[499,29,45]),"Beauty":(["Serum","Lipstick","Perfume"],[35,18,59])}
rows=[]
oid=1000
for i in range(1500):
    cat=np.random.choice(list(cats.keys()), p=[.25,.2,.25,.15,.15])
    idx=np.random.randint(0,3); prod=cats[cat][0][idx]; price=cats[cat][1][idx]
    qty=int(np.random.choice([1,2,3],p=[.7,.2,.1])); cid=int(np.random.randint(1,301))
    date=pd.Timestamp("2025-01-01")+pd.Timedelta(days=int(np.random.randint(0,365)))
    rows.append([oid,cid,str(date.date()),cat,prod,qty,price,round(price*qty,2)]); oid+=1
df=pd.DataFrame(rows, columns=["order_id","customer_id","order_date","category","product","quantity","unit_price","revenue"])
df.to_csv(root/"data/orders.csv", index=False)
total=float(df.revenue.sum()); aov=float(df.revenue.mean()); orders=len(df)
monthly=df.copy(); monthly["month"]=pd.to_datetime(monthly.order_date).dt.to_period("M").astype(str)
mt=monthly.groupby("month").revenue.sum()
rfm=df.groupby("customer_id").agg(recency_days=( "order_date", lambda s: (pd.Timestamp("2025-12-31")-pd.to_datetime(s)).dt.days.min()), frequency=("order_id","count"), monetary=("revenue","sum")).reset_index()
# simple quartile segmentation
rfm["segment"]=np.where(rfm.monetary>=rfm.monetary.quantile(.75),"Champions",np.where(rfm.frequency>=3,"Loyal",np.where(rfm.recency_days>180,"At Risk","Regular")))
top_prod=df.groupby("product").revenue.sum().sort_values(ascending=False)
top_cat=df.groupby("category").revenue.sum().sort_values(ascending=False)
summary={"total_revenue":round(total,2),"orders":orders,"aov":round(aov,2),"customers":int(df.customer_id.nunique()),"top_category":str(top_cat.index[0]),"top_category_revenue":round(float(top_cat.iloc[0]),2),"top_product":str(top_prod.index[0]),"top_product_revenue":round(float(top_prod.iloc[0]),2),"best_month":str(mt.idxmax()),"best_month_revenue":round(float(mt.max()),2),"segments":rfm.segment.value_counts().to_dict()}
(root/"results/summary.json").write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
