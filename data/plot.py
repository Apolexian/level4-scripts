import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
