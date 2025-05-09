import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("schedule8.csv")

# merge contiguous segments on the same (job,gpu)
merged = []
for (job, gpu), grp in df.groupby(["job","gpu"]):
    times = sorted(grp["start_s"])
    seg_start = times[0]
    seg_end   = seg_start + grp.iloc[0]["dur_s"]
    for t in times[1:]:
        if abs(t - seg_end) < 1e-6:
            seg_end += grp.iloc[0]["dur_s"]
        else:
            merged.append((job,gpu,seg_start, seg_end - seg_start))
            seg_start = t
            seg_end   = t + grp.iloc[0]["dur_s"]
    merged.append((job,gpu, seg_start, seg_end - seg_start))

# plot
fig, ax = plt.subplots(figsize=(10, 4))
colors = plt.get_cmap("tab10").colors

labeled = set()
for job, gpu, start, dur in merged:
    # label only the first time we see this job
    if job not in labeled:
        lbl = f"Job {job}"
        labeled.add(job)
    else:
        lbl = None

    ax.broken_barh(
        [(start, dur)],
        (gpu - 0.4, 0.8),
        facecolors=colors[job % len(colors)],
        edgecolor="black",
        linewidth=0.5,
        label=lbl
    )

ax.set_yticks(range(8))
ax.set_yticklabels([f"GPU {g}" for g in range(8)])
ax.set_xlabel("Time (s)")
ax.set_title("ILP Schedule for first 8 requests")

# build a legend showing each job once
handles, labels = ax.get_legend_handles_labels()
by_label = dict(zip(labels, handles))
ax.legend(by_label.values(), by_label.keys(), bbox_to_anchor=(1,1))

plt.tight_layout()
plt.savefig("schedule8.png", dpi=300)
plt.show()
