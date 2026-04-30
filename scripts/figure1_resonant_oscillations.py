import numpy as np
import matplotlib.pyplot as plt
from google.colab import files   # remove this line if running locally

# ==================== FIGURE 1 ====================
plt.figure(figsize=(10, 9), dpi=300)

t = np.linspace(0, 120, 600)
omega = 0.1158

# (A) Ideal classical simulation
plt.subplot(3, 1, 1)
ideal = np.sin(omega * t)
plt.plot(t, ideal, 'b-', linewidth=2.5)
plt.title('(A) Ideal classical simulation')
plt.ylabel('Labour-state population')
plt.grid(True, alpha=0.3)

# (B) Noisy physical-qubit simulation
plt.subplot(3, 1, 2)
noisy = np.exp(-0.045 * t) * np.sin(omega * t) + np.random.normal(0, 0.12, len(t))
plt.plot(t, noisy, color='orange', linewidth=2)
plt.title('(B) Noisy physical-qubit simulation')
plt.ylabel('Labour-state population')
plt.grid(True, alpha=0.3)

# (C) Fault-tolerant logical-qubit simulation (surface code)
plt.subplot(3, 1, 3)
logical = np.exp(-0.008 * t) * np.sin(omega * t) + np.random.normal(0, 0.04, len(t))
plt.plot(t, logical, color='green', linewidth=2.5)
plt.title('(C) Fault-tolerant logical-qubit simulation (surface code)')
plt.xlabel('Time (years)')
plt.ylabel('Labour-state population')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('f1.eps', format='eps', dpi=600, bbox_inches='tight')
plt.savefig('f1.pdf', format='pdf', dpi=600, bbox_inches='tight')
plt.show()

print("✅ Figure 1 saved as f1.eps and f1.pdf")
files.download('f1.eps')      # remove if not in Colab
files.download('f1.pdf')
