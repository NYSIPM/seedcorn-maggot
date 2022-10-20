# Seedcorn Maggot Models
Version 0.0.0 | Last updated 10/18/2022

[Specifications](#specifications) | [Alberta model](#alberta-model) | [Iowa model](#iowa-model) | [NEWA model](#newa-model) | [Ohio model](#ohio-model) | [Wisconsin model](#wisconsin-model)

## Specifications

This module is launched from the command line using Python 3.9 or later. Clone this module from Github, navigate to the local directory where you stored this module, and run `python3 script.py`. Enter the required information when prompted.

The seedcorn maggot (SCM) module queries an RCC-ACIS web service using latitude/longitude decimal degree coordinates to return interpolated daily maximum and minimum temperature at a resolution of 4km for 'NEWA' and 'Ohio' SCM models. _**'Alberta', 'Iowa', and 'Wisconsin' models are not included at this time.**_

A single CSV file is exported to the local `output` directory which summarizes the threshold date for first adult emergence at each location coordinate provided.

Location coordinates are provided by the user as a CSV with records containing a unique ID in the first column, latitude as positive decimal degree values in the second column, and North American longitude as negative decimal degree values in the third column. Column headers are required but the name does not matter.
<small>[back to top](#seedcorn-maggot-models)</small>



## 'Alberta' Model 

**Broatch, J. S., L. M. Dosdall, G. W. Clayton, K. N. Harker, and R.-C. Yang. 2006.** Using Degree-Day and Logistic Models to Predict Emergence Patterns and Seasonal Flights of the Cabbage Maggot and Seed Corn Maggot (Diptera: Anthomyiidae) in Canola. Environ. Entomol. 35: 12. https://doi.org/10.1093/ee/35.5.1166

| Constant      | Value |
| ----------- | ----------- |
MEASUREMENT_UNIT | C |
CALCULATION_SOURCE | soil |
BIOFIX | julianDay == 91 |
THRESHOLD_LOWER | 3.9 |
THRESHOLD_UPPER | - |
CALCULATION | HEAT_UNITS_SIMPLE |
HEAT_UNITS_EGG | - |
HEAT_UNITS_LARVAL | - |
HEAT_UNITS_PUPAL | - |
HEAT_UNITS_BIOFIX_TO_ADULT | - |
HEAT_UNITS_ADULT_TO_ADULT | - |
HEAT_UNITS_F0_ADULT_50PCT | 255 +/- 74.2 |
HEAT_UNITS_F0_PEAK_FLIGHT | 339.5 |
HEAT_UNITS_F1_ADULT_10PCT | 526.8 +/- 66.6 |
HEAT_UNITS_F1_ADULT_50PCT | 639.9 +/- 69.4 |
HEAT_UNITS_F1_ADULT_95PCT | 952.8 +/- 77.0 |
HEAT_UNITS_F1_PEAK_FLIGHT | 594.5 +/- 38.9 |
HEAT_UNITS_F2_ADULT_50PCT | - |
<small>[back to top](#seedcorn-maggot-models)</small>

***

## 'Iowa' Model

**Funderburk, J. E., L. G. Higley, and L. P. Pedigo. 1984.** Seedcorn Maggot (Diptera: Anthomyiidae) Phenology in Central Iowa and Examination of a Thermal-Unit System to Predict Development Under Field Conditions. Environ. Entomol. 13: 105–109. https://doi.org/10.1093/ee/13.1.105


| Constant      | Value |
| ----------- | ----------- |
MEASUREMENT_UNIT | C |
CALCULATION_SOURCE | air |
BIOFIX | julianDay == 1 |
THRESHOLD_LOWER | 3.9 |
THRESHOLD_UPPER | - |
CALCULATION | HEAT_UNITS_SIMPLE |
HEAT_UNITS_EGG | - |
HEAT_UNITS_LARVAL | - |
HEAT_UNITS_PUPAL | - |
HEAT_UNITS_BIOFIX_TO_ADULT | 376 |
HEAT_UNITS_ADULT_TO_ADULT | 392 |
HEAT_UNITS_F0_ADULT_50PCT | 190 |
HEAT_UNITS_F0_PEAK_FLIGHT | - |
HEAT_UNITS_F1_ADULT_10PCT | - |
HEAT_UNITS_F1_ADULT_50PCT | 492 |
HEAT_UNITS_F1_ADULT_95PCT | - |
HEAT_UNITS_F1_PEAK_FLIGHT | - |
HEAT_UNITS_F2_ADULT_50PCT | 499 |
<small>[back to top](#seedcorn-maggot-models)</small>

***

## 'NEWA' Model

Based on Broatch et al (2006) but starts from January 1. 

| Constant      | Value |
| ----------- | ----------- |
MEASUREMENT_UNIT | C |
CALCULATION_SOURCE | air |
BIOFIX | julianDay == 1 |
THRESHOLD_LOWER | 3.9 |
THRESHOLD_UPPER | - |
CALCULATION | HEAT_UNITS_SIMPLE |
HEAT_UNITS_EGG | - |
HEAT_UNITS_LARVAL | - |
HEAT_UNITS_PUPAL | - |
HEAT_UNITS_BIOFIX_TO_ADULT | 254 |
HEAT_UNITS_ADULT_TO_ADULT | - |
HEAT_UNITS_F0_ADULT_50PCT | - |
HEAT_UNITS_F0_PEAK_FLIGHT | - |
HEAT_UNITS_F1_ADULT_10PCT | 461 |
HEAT_UNITS_F1_ADULT_50PCT | - |
HEAT_UNITS_F1_ADULT_95PCT | - |
HEAT_UNITS_F1_PEAK_FLIGHT | - |
HEAT_UNITS_F2_ADULT_50PCT | - |
<small>[back to top](#seedcorn-maggot-models)</small>

***

## 'Ohio' Model

**Hammond, R. B. 1995.** Timing of plowing and planting: Effects on seedcorn maggot populations in soybean. Crop Protection. 14: 471–477. https://doi.org/10.1016/0261-2194(95)00004-6

**Hammond, R. B. 1984.** Effects of Rye Cover Crop Management on Seedcorn Maggot (Diptera: Anthomyiidae) Populations in Soybeans. Environmental Entomology. 13: 1302–1305. https://doi.org/10.1093/ee/13.5.1302



| Constant      | Value |
| ----------- | ----------- |
MEASUREMENT_UNIT | C |
CALCULATION_SOURCE | air |
BIOFIX | oviposition |
THRESHOLD_LOWER | 3.9 |
THRESHOLD_UPPER | - |
CALCULATION | HEAT_UNITS_SIMPLE |
HEAT_UNITS_EGG | - |
HEAT_UNITS_LARVAL | - |
HEAT_UNITS_PUPAL | - |
HEAT_UNITS_BIOFIX_TO_ADULT | range(400, 430) |
HEAT_UNITS_ADULT_TO_ADULT | - |
HEAT_UNITS_F0_ADULT_50PCT | - |
HEAT_UNITS_F0_PEAK_FLIGHT | - |
HEAT_UNITS_F1_ADULT_10PCT | - |
HEAT_UNITS_F1_ADULT_50PCT | - |
HEAT_UNITS_F1_ADULT_95PCT | - |
HEAT_UNITS_F1_PEAK_FLIGHT | - |
HEAT_UNITS_F2_ADULT_50PCT | - |
<small>[back to top](#seedcorn-maggot-models)</small>

***

## 'Wisconsin' Model

**Sanborn, S. M., J. A. Wyman, and R. K. Chapman. 1982.** Threshold Temperature and Heat Unit Summations for Seedcorn Maggot1 Development under Controlled Conditions2. Annals of the Entomological Society of America. 75: 103–106. https://doi.org/10.1093/aesa/75.1.103


| Constant      | Value |
| ----------- | ----------- |
MEASUREMENT_UNIT | C |
CALCULATION_SOURCE | air |
BIOFIX | julianDay == 1 |
THRESHOLD_LOWER | 3.9 |
THRESHOLD_UPPER | - |
CALCULATION | HEAT_UNITS_SIMPLE |
HEAT_UNITS_EGG | 30 |
HEAT_UNITS_LARVAL | 204 |
HEAT_UNITS_PUPAL | 142 |
HEAT_UNITS_BIOFIX_TO_ADULT | 376 |
HEAT_UNITS_ADULT_TO_ADULT | - |
HEAT_UNITS_F0_ADULT_50PCT | - |
HEAT_UNITS_F0_PEAK_FLIGHT | - |
HEAT_UNITS_F1_ADULT_10PCT | - |
HEAT_UNITS_F1_ADULT_50PCT | - |
HEAT_UNITS_F1_ADULT_95PCT | - |
HEAT_UNITS_F1_PEAK_FLIGHT | - |
HEAT_UNITS_F2_ADULT_50PCT | - |
<small>[back to top](#seedcorn-maggot-models)</small>
