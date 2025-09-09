# MIRI-Color-Diagnostics
The MIRI Color classification obtained by Kilerci et al. (2025) can be easily applied to any dataset using the provided region files. 
The x and y colors should be in log units. 
For example: 
x_col= np.log10(F12 / F07)
y_val= np.log10(F18/ F10)
x_err = np.abs((1 / np.log(10)) * np.sqrt((F12_err/F12)**2 + (F07_err/F07)**2))
y_err= np.abs((1 / np.log(10)) * np.sqrt((F18_err/F18)**2 + (F10_err/F10)**2))

# Ellipse parameters 
Ellipse parameters are: center_x, center_y, width, height, angle in degrees
# Reproduction of ellipses
Ellipses can be reproduced using matplotlib.patches.Ellipse(xy=(x, y), width=w, height=h, angle=a)
# Classification
We suggest Mahalanobis Method for source classification. An example code is shown in GMM-Mahalanobis classification file.
