'''
Download the built-in R dataset called ChickWeight either from within an R session or from here.
This is about observed growth of chickens living on different diets.

Based on the sample data, determine whether diet 1 gives a significantly different growth than diet 2. 

For this you can use R, excel, python, or any other programming language or tool.
Prepare a short presentation with your findings. You will be asked to present this on your next interview.
'''


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


df = pd.read_csv(
    '/Users/matteotorba/Library/CloudStorage/OneDrive-PolitecnicodiMilano/2026 APPLICATIONS/MS_QuantCreditRiksAnalyst_Budapest/Homework/ChickWeight.csv'
)


print(df.head())

print(df.info())

print(df.to_string(max_rows=None))

# Filter the data for diet 1 and diet 2
df = df.loc[df['Diet'].isin([1, 2])]

##################################################################################
# 1. EXPLORATORY DATA ANALYSIS (EDA)
#################################################################################

# Compute how many unique chickens are in each diet group
chickens_diet1 = df[df['Diet'] == 1]['Chick'].nunique()
chickens_diet2 = df[df['Diet'] == 2]['Chick'].nunique()
print(f'Number of unique chickens in diet 1: {chickens_diet1}')
print(f'Number of unique chickens in diet 2: {chickens_diet2}')

# Check the presence of early time points for each chicken in each diet group
for chicken in df['Chick'].unique():
    df_chicken = df[df['Chick'] == chicken]
    diet = df_chicken['Diet'].iloc[0]
    time_points = df_chicken['Time'].unique()
    print(f'Chick {chicken} (Diet {diet}) has time points: {time_points}')

# Check the distribution of weights at time 0 (or the first time point) for each diet group
for diet in df['Diet'].unique():
    df_diet = df[df['Diet'] == diet]
    first_time_point = df_diet['Time'].min()
    weights_at_first_time = df_diet[df_diet['Time'] == first_time_point]['weight']
    print(f'Diet {diet} - Weights at time {first_time_point}:')
    print(weights_at_first_time.describe())
# Do a boxplot to check the baseline weight distribution by diet at time 0 (or the first time point)
df_first_time = df[df['Time'] == df['Time'].min()]
plt.figure(figsize=(6, 4))
# highlight the 2nd quartile weight for each diet group with a different color
sns.boxplot(x='Diet', y='weight', data=df_first_time, hue='Diet', palette=['orange', 'blue'], showfliers=False)
plt.title('Baseline Weight Distribution by Diet')
# plt.show()

# Observe that there is not a big difference, however diet 1 has Q1==Q2, and a lower variance. In general the chickens in diet 1 
# seem to be more homogeneous in terms of weight at the first time point, while diet 2 has a wider distribution of weights. 
# This could potentially impact the growth trajectories and should be taken into account when analyzing the growth patterns over time.


# Check the distribution of weights at the last time point for each diet group
for diet in df['Diet'].unique():
    df_diet = df[df['Diet'] == diet]
    last_time_point = df_diet['Time'].max()
    weights_at_last_time = df_diet[df_diet['Time'] == last_time_point]['weight']
    print(f'Diet {diet} - Weights at time {last_time_point}:')
    print(weights_at_last_time.describe())
# Do a boxplot to check the weight distribution by diet at the last time point
df_last_time = df[df['Time'] == df['Time'].max()]
plt.figure(figsize=(6, 4))
sns.boxplot(x='Diet', y='weight', data=df_last_time, hue='Diet', palette=['orange', 'blue'], showfliers=False)
plt.title('Weight Distribution by Diet at Last Time Point')
# plt.show()



# Plotting the growth of each chick over time, colored by diet
plt.figure(figsize=(10, 6))
for chicken in df['Chick'].unique():
    df_chicken = df[df['Chick'] == chicken]
    color = 'orange' if int(df_chicken.loc[df['Chick'] == chicken, 'Diet'].min()) % 2 else 'blue'
    plt.plot(df_chicken['Time'], df_chicken['weight'], label=f'Chick {chicken}', color=color, marker='o')
plt.xlabel('Time')
plt.ylabel('Weight')
plt.title('Growth of Chickens Over Time by Diet')
handles = [plt.Line2D([0], [0], color='orange', label='Diet 1'),
           plt.Line2D([0], [0], color='blue', label='Diet 2')]
plt.legend(handles=handles)
# plt.show()

# Compute the weight gain for each chick at the last time point compared to the first time point and plot it as a bar chart, colored by diet
df['weight_gain'] = df.groupby('Chick')['weight'].transform(lambda x: x.iloc[-1] - x.iloc[0])
plt.figure(figsize=(10, 6))
sns.barplot(x='Chick', y='weight_gain', hue='Diet', data=df.drop_duplicates(subset=['Chick']), palette=['orange', 'blue'])
plt.xlabel('Chick')
plt.ylabel('Weight Gain')
plt.title('Weight Gain of Chickens by Diet')
# plt.show()



# Plot the mean trajectory by diet over time (with error bars / CI)
plt.figure(figsize=(10, 6))
sns.lineplot(x='Time', y='weight', hue='Diet', data=df, errorbar='sd', palette=['orange', 'blue'])
plt.xlabel('Time')
plt.ylabel('Weight')
plt.title('Mean Growth of Chickens Over Time by Diet')
# plt.show()



# Compute the growth rate for each chick
df['growth_rate'] = df.groupby('Chick')['weight'].diff() / df.groupby('Chick')['Time'].diff()

# Plot the growth rate of each chick over time, colored by diet
plt.figure(figsize=(10, 6))
for chicken in df['Chick'].unique():
    df_chicken = df[df['Chick'] == chicken]
    color = 'orange' if int(df_chicken.loc[df['Chick'] == chicken, 'Diet'].min()) % 2 else 'blue'
    plt.plot(df_chicken['Time'], df_chicken['growth_rate'], label=f'Chick {chicken}', color=color, marker='o')
plt.xlabel('Time')
plt.ylabel('Growth Rate')
plt.title('Growth Rate of Chickens Over Time by Diet')
handles = [plt.Line2D([0], [0], color='orange', label='Diet 1'),
           plt.Line2D([0], [0], color='blue', label='Diet 2')]
plt.legend(handles=handles)
# plt.show()



# Plot the mean growth rate by diet over time (with error bars / CI)
plt.figure(figsize=(10, 6))
sns.lineplot(x='Time', y='growth_rate', hue='Diet', data=df, errorbar='sd', palette=['orange', 'blue'])
plt.xlabel('Time')
plt.ylabel('Growth Rate')
plt.title('Mean Growth Rate of Chickens Over Time by Diet')
# plt.show()

# # Plot the mean growth rate by diet over time (with error bars / CI) by excluding the chickens that died before the end of the observation period
# # Identify chickens that died before the end of the observation period (i.e., those that do not have data for the last time point)
# last_time_point = df['Time'].max()
# chickens_with_full_data = df[df['Time'] == last_time_point]['Chick'].unique()
# df_full_data = df[df['Chick'].isin(chickens_with_full_data)]
# plt.figure(figsize=(10, 6))
# sns.lineplot(x='Time', y='growth_rate', hue='Diet', data=df_full_data, errorbar='sd', palette=['orange', 'blue'])
# plt.xlabel('Time')
# plt.ylabel('Growth Rate')
# plt.title('Mean Growth Rate of Chickens Over Time by Diet (Excluding Chickens that Died Early)')
# # plt.show()



# Plotting the histogram of the growth rate of each chick using subplots, colored by diet
pltgen = plt.figure(figsize=(6, 5))
for chicken in df['Chick'].unique():
    subplot_index = int(chicken)  # Assuming Chick numbers are 1-indexed
    plt.subplot(6, 5, subplot_index)  # Create a 2x4 grid of subplots
    df_chicken = df[df['Chick'] == chicken]
    color = 'orange' if int(df_chicken.loc[df['Chick'] == chicken, 'Diet'].min()) % 2 else 'blue'
    plt.hist(df_chicken['growth_rate'], label=f'Chick {chicken}', color=color)
    plt.xlabel('Time')
    plt.ylabel('Growth Rate')
pltgen.suptitle('Growth Rate of Chickens Over Time by Diet')
handles = [plt.Line2D([0], [0], color='orange', label='Diet 1'),
           plt.Line2D([0], [0], color='blue', label='Diet 2')]
pltgen.legend(handles=handles, loc='center right', prop={'size': 20})
pltgen.show()





##################################################################################
# 2. CORE ANALYSIS - LINEAR MIXED EFFECTS MODEL
#################################################################################

import numpy as np
import statsmodels.formula.api as smf
from scipy.stats import chi2

# 2.1 Prepare analysis dataset (important for mixed models)
# Keep only the columns we need and drop missing values
df_main = df[['weight', 'Time', 'Diet', 'Chick']].dropna().copy()

# Ensure proper sorting within chick (useful for sanity)
df_main = df_main.sort_values(['Chick', 'Time']).reset_index(drop=True)

# Make sure Chick is treated as a grouping variable (string/categorical is safer)
df_main['Chick'] = df_main['Chick'].astype(str)

# Create a binary indicator for diet 2 (diet 1 is the reference group)
# This avoids ambiguity with categorical coding and makes coefficient interpretation explicit.
df_main['diet2'] = (df_main['Diet'] == 2).astype(int)

# Center time for interpretability/stability
# (If centered, the 'diet2' coefficient is the estimated difference at average time)
df_main['Time_c'] = df_main['Time'] - df_main['Time'].mean()

print("\n=== MAIN ANALYSIS DATA OVERVIEW ===")
print(df_main.head())
print(df_main.groupby('Diet')['Chick'].nunique().rename('n_unique_chicks'))
print(df_main.groupby('Diet').size().rename('n_observations'))

# How many observations per chick
obs_per_chick = df_main.groupby('Chick').size()
print("\nObservations per chick (summary):")
print(obs_per_chick.describe())


# 2.2 Fit primary mixed-effects model (random intercept per chick)
# Model:
# weight ~ Time_c + diet2 + Time_c:diet2
# random intercept by Chick
#
# Interpretation:
# - Time_c      : slope for Diet 1 (reference)
# - diet2       : vertical shift for Diet 2 vs Diet 1 at centered time
# - Time_c:diet2: difference in slope (Diet 2 minus Diet 1) --> KEY TEST

print("\n=== FITTING PRIMARY MIXED MODEL (RANDOM INTERCEPT) ===")

model_full = smf.mixedlm(
    "weight ~ Time_c + diet2 + Time_c:diet2",
    data=df_main,
    groups=df_main["Chick"],
    re_formula="1"
)

result_full = model_full.fit(reml=False, method="lbfgs")
print(result_full.summary())

# Extract key interaction result (main hypothesis test)
interaction_name = "Time_c:diet2"
beta_inter = result_full.params.get(interaction_name, np.nan)
se_inter = result_full.bse.get(interaction_name, np.nan)
p_inter = result_full.pvalues.get(interaction_name, np.nan)

# Confidence intervals
ci_full = result_full.conf_int()
if interaction_name in ci_full.index:
    ci_low, ci_high = ci_full.loc[interaction_name]
else:
    ci_low, ci_high = np.nan, np.nan

print("\n=== MAIN HYPOTHESIS TEST: DIFFERENT GROWTH TREND? ===")
print(f"Interaction coefficient ({interaction_name}) = {beta_inter:.4f} g/day")
print(f"SE = {se_inter:.4f}")
print(f"95% CI = [{ci_low:.4f}, {ci_high:.4f}]")
print(f"p-value = {p_inter:.6f}")

if pd.notna(p_inter):
    if p_inter < 0.05:
        direction = "higher" if beta_inter > 0 else "lower"
        print(
            f"Conclusion (5% level): Significant difference in growth trend. "
            f"Diet 2 has a {direction} growth slope than Diet 1 by about {abs(beta_inter):.2f} g/day."
        )
    else:
        print(
            "Conclusion (5% level): No statistically significant evidence of a different growth trend "
            "between Diet 1 and Diet 2 in this sample."
        )


#  2.3 Reduced vs Full model comparison (LRT)
# Reduced model excludes the interaction term, i.e. assumes same growth trend across diets
print("\n=== LIKELIHOOD-RATIO TEST: REDUCED vs FULL MODEL ===")

model_reduced = smf.mixedlm(
    "weight ~ Time_c + diet2",
    data=df_main,
    groups=df_main["Chick"],
    re_formula="1"
)

result_reduced = model_reduced.fit(reml=False, method="lbfgs")
print(result_reduced.summary())

# Likelihood-ratio statistic
ll_full = result_full.llf
ll_red = result_reduced.llf
lr_stat = 2 * (ll_full - ll_red)
df_diff = int(result_full.df_modelwc - result_reduced.df_modelwc)
p_lr = chi2.sf(lr_stat, df=df_diff) if df_diff > 0 else np.nan

print(f"\nLRT statistic = {lr_stat:.4f}")
print(f"df difference = {df_diff}")
print(f"LRT p-value = {p_lr:.6f}")

if pd.notna(p_lr):
    if p_lr < 0.05:
        print("The interaction improves model fit significantly (supports different growth trends).")
    else:
        print("The interaction does not improve model fit significantly (no strong evidence of different growth trends).")


# 2.4 Model-based predicted trajectories (fixed effects only) for visualization
# Build a small prediction grid over the observed time range
time_grid = np.sort(df_main['Time'].unique())
time_mean = df_main['Time'].mean()

pred_grid = pd.DataFrame({
    'Time': np.concatenate([time_grid, time_grid]),
    'Diet': [1] * len(time_grid) + [2] * len(time_grid)
})
pred_grid['diet2'] = (pred_grid['Diet'] == 2).astype(int)
pred_grid['Time_c'] = pred_grid['Time'] - time_mean

# Predict using fixed effects part
pred_grid['pred_weight'] = result_full.predict(pred_grid)

plt.figure(figsize=(10, 6))

# Plot raw mean trajectories as context (from your data)
sns.lineplot(
    data=df_main,
    x='Time',
    y='weight',
    hue='Diet',
    estimator='mean',
    errorbar='sd',
    palette=['orange', 'blue'],
    alpha=0.35,
    legend=False
)

# Plot model-implied trajectories
for diet_val, color in [(1, 'orange'), (2, 'blue')]:
    tmp = pred_grid[pred_grid['Diet'] == diet_val]
    plt.plot(tmp['Time'], tmp['pred_weight'], color=color, linewidth=2.5, label=f'Mixed model fit - Diet {diet_val}')

plt.xlabel('Time')
plt.ylabel('Weight')
plt.title('Diet 1 vs Diet 2: Mixed-Model Estimated Growth Trajectories')
plt.legend()
# plt.show()


# 2.5 Light diagnostics
# Residuals vs fitted and QQ-like histogram
df_main['fitted'] = result_full.fittedvalues
df_main['resid'] = df_main['weight'] - df_main['fitted']

plt.figure(figsize=(8, 5))
plt.scatter(df_main['fitted'], df_main['resid'], alpha=0.7)
plt.axhline(0, linestyle='--')
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.title('Residuals vs Fitted (Mixed Model)')
# plt.show()

plt.figure(figsize=(8, 5))
plt.hist(df_main['resid'], bins=20, edgecolor='black')
plt.xlabel('Residual')
plt.ylabel('Frequency')
plt.title('Residual Distribution (Mixed Model)')
# plt.show()


##################################################################################
# 3. BACKUP ANALYSIS - PER-CHICK WEIGHT GAIN (ROBUSTNESS CHECK)
##################################################################################

# Build one row per chick: first and last observed weight/time
df_chick_summary = (
    df_main.sort_values(['Chick', 'Time'])
           .groupby('Chick', as_index=False)
           .agg(
               Diet=('Diet', 'first'),
               time_first=('Time', 'first'),
               time_last=('Time', 'last'),
               weight_first=('weight', 'first'),
               weight_last=('weight', 'last'),
               n_obs=('weight', 'size')
           )
)

df_chick_summary['duration'] = df_chick_summary['time_last'] - df_chick_summary['time_first']
df_chick_summary['weight_gain'] = df_chick_summary['weight_last'] - df_chick_summary['weight_first']

# Avoid division by zero if any chick has only one time point
df_chick_summary['gain_per_day'] = np.where(
    df_chick_summary['duration'] > 0,
    df_chick_summary['weight_gain'] / df_chick_summary['duration'],
    np.nan
)

print("\n=== PER-CHICK SUMMARY (BACKUP ANALYSIS DATA) ===")
print(df_chick_summary.head())
print(df_chick_summary.groupby('Diet')[['weight_gain', 'gain_per_day', 'duration', 'n_obs']].describe())

# Compare gain_per_day between diets (all chicks with duration > 0)
gain1 = df_chick_summary.loc[(df_chick_summary['Diet'] == 1) & (df_chick_summary['gain_per_day'].notna()), 'gain_per_day']
gain2 = df_chick_summary.loc[(df_chick_summary['Diet'] == 2) & (df_chick_summary['gain_per_day'].notna()), 'gain_per_day']

# Welch t-test (does not assume equal variances)
ttest_res = stats.ttest_ind(gain1, gain2, equal_var=False, nan_policy='omit')

print("\n=== BACKUP TEST: GAIN PER DAY (WELCH T-TEST) ===")
print(f"Diet 1 mean gain/day: {gain1.mean():.4f}")
print(f"Diet 2 mean gain/day: {gain2.mean():.4f}")
print(f"Difference (Diet 2 - Diet 1): {(gain2.mean() - gain1.mean()):.4f}")
print(f"t-statistic = {ttest_res.statistic:.4f}")
print(f"p-value     = {ttest_res.pvalue:.6f}")

# Optional nonparametric backup
mw_res = stats.mannwhitneyu(gain1, gain2, alternative='two-sided')
print("\n=== NONPARAMETRIC BACKUP: MANN-WHITNEY U (GAIN PER DAY) ===")
print(f"U statistic = {mw_res.statistic:.4f}")
print(f"p-value     = {mw_res.pvalue:.6f}")

# Visualize backup metric
plt.figure(figsize=(8, 5))
sns.boxplot(data=df_chick_summary, x='Diet', y='gain_per_day', hue='Diet', palette=['orange', 'blue'], showfliers=False)
sns.stripplot(data=df_chick_summary, x='Diet', y='gain_per_day', color='black', alpha=0.6, jitter=True)
plt.title('Per-Chick Average Gain per Day by Diet (Backup Analysis)')
plt.ylabel('Average Gain per Day')
# plt.show()

plt.show()