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

xy=(x, y) → ellipse center (mean)

width=w, height=h → the 2σ ellipse axes lengths

angle=a → rotation of the ellipse in degrees

# Reproduction of ellipses
Ellipses can be reproduced using matplotlib.patches.Ellipse(xy=(x, y), width=w, height=h, angle=a)

# Classification
We suggest Mahalanobis Method for source classification. An example code is classify_mahalanobis.py

It can be applied as: python classify_mahalanobis.py <sources_file> <ellipse_file> <output_file>

python classify_mahalanobis.py sources.txt ellipse_12over07_03_12over10_03.txt output_example.txt

source.txt:

ID   F07   F07_err   F10   F10_err   F12   F12_err

F07, F10, F12 → fluxes in the relevant IR bands in log units. 
_err → 1σ flux errors
ID → unique source ID

output_example.txt:

ID   Mahalanobis_Distance   Class   Uncertain

1    0.95   AGN   No

2    1.20   AGN   No

3    2.85   AGN   No

4    3.25   SFG   Yes

5    1.75   AGN   No

Mahalanobis_Distance → distance from ellipse center
Class → AGN or SFG
Uncertain → Yes if distance > threshold  (this means ID 4's SFG classification is not certain)

# Plotting script
The plotting script can be used to check if the sources fall into the GMM ellipses visually. 

python plot_mahalanobis.py


# Citation
If you use this code or ellipse definitions, please cite: Kilerci et al. 2025, A&A, 704, A71. https://doi.org/10.1051/0004-6361/202554884
# Citation
Kilerci et al. 2025, A&A, 704, A71. https://doi.org/10.1051/0004-6361/202554884


