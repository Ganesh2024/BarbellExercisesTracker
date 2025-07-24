import pandas as pd
from glob import glob

# --------------------------------------------------------------
# List all data in data/raw/MetaMotion
# --------------------------------------------------------------

files = glob("../../data/raw/MetaMotion/*.csv")
len(files)

# --------------------------------------------------------------
# Extract features from filename
# --------------------------------------------------------------

# --------------------------------------------------------------
# Read all files
# --------------------------------------------------------------
 
# --------------------------------------------------------------
# Working with datetimes
# --------------------------------------------------------------

# --------------------------------------------------------------
# Turn into function
# --------------------------------------------------------------

def read_data_from_files(files):
    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    acc_set = 1
    gyr_set = 1

    for i in range(0, len(files)):
        path = "../../data/raw/MetaMotion\\"
        f = files[i].replace(path, "").split("_")[0].split("-")

        participant = f[0]
        label = f[1]
        category = f[2].rstrip("123")

        temp_df = pd.read_csv(files[i])
        temp_df["participant"] = participant
        temp_df["label"] = label
        temp_df["category"] = category

        if "Accelerometer" in files[i]:
            temp_df["set"] = acc_set
            acc_set += 1
            acc_df = pd.concat([acc_df,temp_df])
        else:
            temp_df["set"] = gyr_set
            gyr_set += 1
            gyr_df = pd.concat([gyr_df,temp_df])
    
    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"],unit="ms") 
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"],unit="ms")

    acc_df.drop(columns=["elapsed (s)","time (01:00)","epoch (ms)"],inplace=True)
    gyr_df.drop(columns=["elapsed (s)","time (01:00)","epoch (ms)"],inplace=True)

    return acc_df,gyr_df

acc_df, gyr_df = read_data_from_files(files)


# --------------------------------------------------------------
# Merging datasets
# --------------------------------------------------------------

data_merged = pd.concat([acc_df.iloc[:,:3],gyr_df],axis=1)

data_merged.columns = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyr_x",
    "gyr_y",
    "gyr_z",
    "participant",
    "label",
    "category",
    "set"
]

# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz

sampling = {
    "acc_x": "mean",
    "acc_y": "mean",
    "acc_z": "mean",
    "gyr_x": "mean",
    "gyr_y": "mean",
    "gyr_z": "mean",
    "participant": "last",
    "label":       "last",
    "category":    "last",
    "set" :        "last"
}

days = [g for n, g in data_merged.groupby(pd.Grouper(freq="D"))]

data_resampled = pd.concat([df.resample(rule="200ms").apply(sampling).dropna() for df in days])

data_resampled["set"] = data_resampled["set"].astype("int")

data_resampled.info()

# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------

data_resampled.to_pickle("../../data/interim/01_data_processed.pkl")
