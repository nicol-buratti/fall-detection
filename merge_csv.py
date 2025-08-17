import pandas as pd

df1 = pd.read_csv("U01_R01_accel.csv")
df2 = pd.read_csv("U01_R01_gyro.csv")

df1 = pd.concat([df1, df2], axis=1)


df1.to_csv("merged.csv", index=False)
