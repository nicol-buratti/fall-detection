from pathlib import Path

import numpy as np
import pandas as pd

dataset = Path("WEDA-FALL/dataset/50Hz")

falls_path = Path("WEDA-FALL/dataset/fall_timestamps.csv")
falls_df = pd.read_csv(falls_path)

p_accel = list(f for f in dataset.glob("F*/*_accel.csv") if "vertical" not in f.name)
p_gyro = list(f for f in dataset.glob("F*/*_gyro.csv"))

for acc, gyro in zip(p_accel, p_gyro):
    df1 = pd.read_csv(acc)
    df2 = pd.read_csv(gyro)
    df = pd.concat([df1, df2], axis=1)

    split = acc.stem.split("_")
    filename = str(acc.parent.name + "/" + split[0] + "_" + split[1])

    falls_df[falls_df["filename"] == filename]
    _, start, end = falls_df[falls_df["filename"] == filename].iloc[0]
    df["label"] = np.where(
        (df["accel_time_list"] > start)
        & (df["accel_time_list"] < end)
        & (df["gyro_time_list"] > start)
        & (df["gyro_time_list"] < end),
        "fall",
        "ADL",
    )

    df.drop(columns=["accel_time_list", "gyro_time_list"], inplace=True)
    # print(df.info())
    filename = filename.replace("/", "_")
    df.to_csv(Path(f"raw_data/{filename}_data.csv"), index=False)
