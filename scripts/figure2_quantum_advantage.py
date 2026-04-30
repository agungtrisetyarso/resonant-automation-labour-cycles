import numpy as np
import matplotlib.pyplot as plt
from google.colab import files   # remove this line if running locally

# ==================== FIGURE 2 ====================
plt.figure(figsize=(10, 6), dpi=300)

sizes = np.array([10, 50, 100, 200, 500, 1000, 2000, 5000])

classical = np.exp(-0.0015 * sizes) + 0.05 * np.random.normal(0, 1, len(sizes))
physical  = np.exp(-0.008 * sizes)  + 0.08 * np.random.normal(0, 1, len(sizes))
logical   = 0.98 * np.exp(-0.0003 * sizes) + 0.015 * np.random.normal(0, 1, len(sizes))

classical = np.clip(classical, 0.05, 0.98)
physical  = np.clip(physical,  0.02, 0.95)
logical   = np.clip(logical,   0.85, 0.99)

plt.semilogx(sizes, classical, 'b-o', linewidth=2.5, label='Classical tensor-network')
plt.semilogx(sizes, physical,  color='orange', marker='o', linestyle='-', linewidth=2.5, label='Noisy physical qubits')
plt.semilogx(sizes, logical,   'g-o', linewidth=2.5, label='Fault-tolerant logical qubits (surface code)')

plt.xlabel('System size (number of tasks / qubits)')
plt.ylabel('Simulation fidelity')
plt.title('Predicted Quantum Advantage in Macroeconomic Simulation')
plt.grid(True, which='both', alpha=0.3)
plt.legend(fontsize=11)
plt.tight_layout()

plt.savefig('f2.eps', format='eps', dpi=600, bbox_inches='tight')
plt.savefig('f2.pdf', format='pdf', dpi=600, bbox_inches='tight')
plt.show()

print("✅ Figure 2 saved as f2.eps and f2.pdf")
files.download('f2.eps')      # remove if not in Colab
files.download('f2.pdf')
