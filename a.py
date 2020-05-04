import numpy as np
from scipy import stats

# With lists
b = np.random.randn(10) + 2
a = np.random.randn(10)

t2, p2 = stats.ttest_ind(a,b)
print("t-test value: " + str(t2))
print("p-value for μ1 ≠ μ2: " + str(p2))
