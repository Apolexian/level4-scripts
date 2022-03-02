import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from math import pi

def show_values(axs, orient="v", space=.01):
    def _single(ax):
        if orient == "v":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() / 2
                _y = p.get_y() + p.get_height() + (p.get_height()*0.01)
                value = '{:.1f}'.format(p.get_height())
                ax.text(_x, _y, value, ha="center") 
        elif orient == "h":
            for p in ax.patches:
                _x = p.get_x() + p.get_width() + float(space)
                _y = p.get_y() + p.get_height() - (p.get_height()*0.5)
                value = '{:.1f}'.format(p.get_width())
                ax.text(_x, _y, value, ha="left")

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _single(ax)
    else:
        _single(axs)

impls = ["ngtcp2", "ngtcp2", "picoquic", "picoquic", "msquic","msquic", "quic-go", "quic-go", "Quinn", "Quinn", "Quiche","Quiche", "mvfst", "mvfst"]
footprint = [3.4, 4.3, 3.2, 3.9, 3.2, 4.1, 8.7, 9.9, 9.1, 9.5, 7.8, 7.0, 11.1, 12.0]
tag = ["Client", "Server"] * 7

data = list()
data.append(impls)
data.append(footprint)
data.append(tag)

df = pd.DataFrame(data).transpose()
df.columns = ["Implementations", "Footprint", "Type"]

sns.set_style('darkgrid')
sns.set_palette('Set2')

sns.barplot(data=df, x='Implementations', y='Footprint', hue='Type')

plt.title('Server and Client footprints for various QUIC implementations')
plt.xlabel('Implementation')
plt.ylabel('Size (MiB)')

sns.despine()
plt.savefig("quic_impls.png",dpi=500)

plt.clf()

components = ["std", "quinn", "regex", "rustls", "tokio", "ring", "url", "idna", "other"]
percents = [23, 17.8, 14.3, 12.6, 5.9, 5.8, 1.8, 1.5, 17.3]
data = list()
data.append(components)
data.append(percents)
df = pd.DataFrame(data).transpose()
df.columns = ["Crate", "Contribution"]
sns.set(style="darkgrid")
sns.set_palette('Set2')
ax = sns.barplot(data=df, x='Crate', y='Contribution')
plt.xlabel('Crate')
plt.ylabel('Contribution (%)')
plt.title("Crates by largest contribution to the client's binary size")
sns.despine()
show_values(ax)
plt.savefig("mquictt_binary_client.png",dpi=500)


plt.clf()

components = ["std", "quinn", "rustls", "regex", "h2", "tokio", "hyper", "aho\n_corasick", "other"]
percents = [16.9, 16.6, 16.3, 8.8, 7.3, 3.2, 3.0, 1.9, 26]
data = list()
data.append(components)
data.append(percents)
df = pd.DataFrame(data).transpose()
df.columns = ["Crate", "Contribution"]
sns.set(style="darkgrid")
sns.set_palette('Set2')
ax = sns.barplot(data=df, x='Crate', y='Contribution')
plt.xlabel('Crate')
plt.ylabel('Contribution (%)')
plt.title("Crates by largest contribution to the broker's binary size")
sns.despine()
show_values(ax)
plt.savefig("mquictt_binary_broker.png",dpi=500)


plt.clf()

stages = ["Base", "32-bit\nOnly", "No Std\nOut", "No Error\nHandling"]
size = [9183, 8649, 8327, 8211]
data = list()
data.append(stages)
data.append(size)
df = pd.DataFrame(data).transpose()
df.columns = ["Stage", "Binary Size (KiB)"]
sns.set(style="darkgrid")
sns.set_palette('Set2')
ax = sns.barplot(data=df, x='Stage', y='Binary Size (KiB)')
plt.xlabel('Stage')
plt.ylabel('Binary Size (KiB)')
plt.title("Reduction in broker's binary size based on stage of reduction")
sns.despine()
show_values(ax)
plt.savefig("quinn_binary_reduce_broker.png",dpi=500)

plt.clf()

stages = ["Base", "32-bit\nOnly", "No Std\nOut", "No Error\nHandling"]
size = [9838, 9002, 8527, 8501]
data = list()
data.append(stages)
data.append(size)
df = pd.DataFrame(data).transpose()
df.columns = ["Stage", "Binary Size (KiB)"]
sns.set(style="darkgrid")
sns.set_palette('Set2')
ax = sns.barplot(data=df, x='Stage', y='Binary Size (KiB)')
plt.xlabel('Stage')
plt.ylabel('Binary Size (KiB)')
plt.title("Reduction in client's binary size based on stage of reduction")
sns.despine()
show_values(ax)
plt.savefig("quinn_binary_reduce_client.png",dpi=500)

plt.clf()

df_mqtt_tcp = pd.read_csv("mqtt/rumqtt_base_filtered/results_connection_time.csv")
categories=set(df_mqtt_tcp["link"])
N = len(categories)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]
plt.figure(figsize=(8,8)) 
ax = plt.subplot(111, polar=True)
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)
plt.xticks(angles[:-1], categories)
ax.set_rlabel_position(0)
plt.yticks([0,0.001,0.02], ["0","0.01","0.02"], color="grey", size=7)
plt.ylim(0,0.03)
values_home = df_mqtt_tcp.loc[df_mqtt_tcp['scenario'] == "home"]
values_farm = df_mqtt_tcp.loc[df_mqtt_tcp['scenario'] == "farm"]
values_synth = df_mqtt_tcp.loc[df_mqtt_tcp['scenario'] == "synth"]

h = []
f = []
s = []

for c in categories:
    h.append(values_home.loc[values_home['link'] == c]['time'].values.tolist()[0])
    f.append(values_farm.loc[values_farm['link'] == c]['time'].values.tolist()[0])
    s.append(values_synth.loc[values_synth['link'] == c]['time'].values.tolist()[0])

h += h[:1]
f += f[:1]
s += s[:1]

print(h)
print(angles)
ax.plot(angles, h, linewidth=1, linestyle='solid', label="Home")
ax.fill(angles, h, 'b', alpha=0.1)
ax.plot(angles, f, linewidth=1, linestyle='solid', label="Farm")
ax.fill(angles, f, 'r', alpha=0.1)
ax.plot(angles, s, linewidth=1, linestyle='solid', label="Synth")
ax.fill(angles, s, 'g', alpha=0.1)
plt.legend(loc='upper right', bbox_to_anchor=(0.05, 0.05))
plt.title("Time for transport protocol\nto establish connection in base rumqtt.\n")
plt.savefig("rumqtt_base_connection_time.png",dpi=500)
