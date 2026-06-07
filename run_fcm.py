import pandas as pd
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv('synthetic_patients.csv')

# Feature Selection: eGFR and Creatinine
# Transpose to get shape (2, 300) for skfuzzy.cluster.cmeans
alldata = np.vstack((df['eGFR'], df['Creatinine']))

# Set FCM Parameters
c = 4
m = 2.0
error = 0.005
maxiter = 1000

# Run cmeans
cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
    alldata, c=c, m=m, error=error, maxiter=maxiter, init=None
)

print("Cluster Centers for eGFR and Creatinine:")
for i, center in enumerate(cntr):
    print(f"Cluster {i}: eGFR = {center[0]:.2f}, Creatinine = {center[1]:.2f}")

# Optional: Plotting
cluster_membership = np.argmax(u, axis=0)

plt.figure(figsize=(10, 7))
colors = ['b', 'g', 'r', 'c']
labels = ['Cluster 0', 'Cluster 1', 'Cluster 2', 'Cluster 3']

for j in range(c):
    plt.scatter(alldata[0, cluster_membership == j],
                alldata[1, cluster_membership == j],
                c=colors[j],
                label=labels[j],
                alpha=0.6,
                edgecolors='w',
                s=50)

# Plot centers
for i, pt in enumerate(cntr):
    plt.plot(pt[0], pt[1], 'ks', markersize=10) # black squares for centers

plt.title('Fuzzy C-Means Clustering (eGFR vs Creatinine)')
plt.xlabel('eGFR (mL/min)')
plt.ylabel('Creatinine (umol/L)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)

plt.savefig('fcm_clusters.png', dpi=300, bbox_inches='tight')
print("\nSaved scatter plot to fcm_clusters.png")
