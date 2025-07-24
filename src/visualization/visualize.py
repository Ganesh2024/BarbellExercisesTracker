import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
 

df = pd.read_pickle("../../data/interim/01_data_processed.pkl")

# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------

set_df = df[df["set"] == 1]  # df data w.r.t set column

plt.plot(set_df["acc_y"].reset_index(drop=True))  
# sns.lineplot(x=set_df.index, y=set_df["acc_y"])
# sns.lineplot(x=range(1,len(set_df)+1), y=set_df["acc_y"])



# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------

for label in df["label"].unique():
  subset = df[df["label"] == label]
  fig, ax = plt.subplots()
  plt.plot(subset[:100]["acc_y"].reset_index(drop=True),label = label)
  plt.legend()
  plt.show()

# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------

sns.set_theme(style="darkgrid") 
mpl.rcParams["figure.dpi"] = 100
mpl.rcParams["figure.figsize"] = (20,5)

# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------

category_df = df[ (df["label"]=="ohp") & (df["participant"]=="B") ]
sns.lineplot(
  data=category_df,
  x=range(0,len(category_df)),
  y="acc_x",
  hue="category"
)
plt.xlabel("sample")
plt.ylabel("acc_y")
plt.legend()

# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------

participant_df = df[df["label"] == 'row'].sort_values("participant") #bench , row, ohp, squat

sns.lineplot(
  data=participant_df,
  x=range(0,len(participant_df)),
  y="acc_x",
  hue="participant"
)

# fig, ax = plt.subplots()
# participant_df.groupby(["participant"])["acc_y"].plot()
# ax.set_ylabel("acc_y")
# ax.set_xlabel("samples")
# plt.legend()

# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------

# label = "squat"
# participant = "A"
# all_axis_df = df.query(f"label == '{label}' ").query(f"participant == '{participant}' ").reset_index()
# fig, ax = plt.subplots()
# all_axis_df[["acc_x","acc_y","acc_z"]].plot(ax=ax)
# ax.set_ylabel("acc_y")
# ax.set_xlabel("samples")
# plt.legend()

all_axis_df = df[ (df["label"] == "squat") & (df["participant"] == "A")]

melted_df = all_axis_df.melt(
  # id_vars = ["index"]
  value_vars = ["acc_x","acc_y","acc_z"],
  var_name = "axis",
  value_name = "all_axis_acc"
)

# melted_df = melted_df.sort_values("axis")
plt.figure(figsize=(40, 5)) 
sns.lineplot(
  data=melted_df,
  x = range(0,len(melted_df)),
  y = "all_axis_acc",
  hue = "axis"
)

# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------

labels = df["label"].unique()
participants = df["participant"].unique()

for label in labels:
  for participant in participants:
    all_axis_df = (
      df[(df["label"]==label) & (df["participant"]==participant)].reset_index()
    )

    if len(all_axis_df) > 0 :
      fig, ax = plt.subplots(figsize=(20, 5))
      all_axis_df[["acc_x","acc_y","acc_z"]].plot(ax=ax)
      ax.set_xlabel("samples")
      plt.title(f"{label} ({participant})".title())
      plt.legend()

for label in labels:
  for participant in participants:
    all_axis_df = (
      df[(df["label"]==label) & (df["participant"]==participant)].reset_index()
    )

    if len(all_axis_df) > 0 :
      fig, ax = plt.subplots(figsize=(20, 5))
      all_axis_df[["gyr_x","gyr_y","gyr_z"]].plot(ax=ax)
      ax.set_xlabel("samples")
      plt.title(f"{label} ({participant})".title())
      plt.legend()

# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------


# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------
 
labels = df["label"].unique()
participants = df["participant"].unique()

for label in labels:
  for participant in participants:
    combined_plot_df = df[(df["label"]==label) & (df["participant"]==participant)].reset_index()

    if len(combined_plot_df)>0 :
      fig,ax = plt.subplots(nrows=2,sharex=True ,figsize=(20,10))
      combined_plot_df[["acc_x","acc_y","acc_z"]].plot(ax=ax[0])
      combined_plot_df[["gyr_x","gyr_y","gyr_z"]].plot(ax=ax[1])
      fig.suptitle(f"{label}_{participant}")
      ax[0].set_ylabel("Accelerometer")
      ax[1].set_ylabel("Gyroscope")
      ax[1].set_xlabel("samples")
      plt.savefig(f"../../reports/figures/{label}_{participant}.png")
      plt.close(fig)  # Close the figure to free memory





