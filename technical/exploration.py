import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
from ydata_profiling import ProfileReport

#"🧑‍🍳"
#TODO date data handling ✅

#tidy data
#TODO apply basic tidy data concept (cleansing) ✅
#TODO handle mixed data type ✅ (by set low memeory to false when importing the data)
'''
mixed_type_columns = data.iloc[:, [4, 5, 12, 13]]
print(mixed_type_columns.applymap(type).nunique())
'''
#TODO check duplicated ✅
#TODO add comments/docstring
#TODO handle missing values 
#TODO apply some extended tidy data structure (if necessary) (pivot/melt) 🧑‍🍳
#TODO handle outliers
#TODO data transformation https://aeturrell.github.io/coding-for-economists/data-transformation.html
#TODO data analysis, stats work (variable analysis, correlation, hypothesis testing), & visualization 🧑‍🍳
#TODO OOP
#TODO deploy profiling to streamlit
#TODO minireport (keep it simple) & provide notebook for this (optional)




csv_file_path = 'technical/data/food/wfp_food_prices_idn.csv'
csv_file_path_two = 'technical/data/food/Jalan Tol Beroperasi di Indonesia Tahun 2015.csv'

data = pd.read_csv(csv_file_path, low_memory=False)
data_two = pd.read_csv(csv_file_path_two, delimiter=';')

#profiling
profile = ProfileReport(
    data, minimal=True, title="Profiling Report: Food Price"
)
profile.to_file("your_report.html")

data['price'] = pd.to_numeric(data['price'], errors='coerce')

data['date'] = pd.to_datetime(data['date'], errors='coerce', format='%Y-%m-%d')
data = data.assign(
    data_year=data['date'].dt.year,
    data_month=data['date'].dt.month,
    data_day=data['date'].dt.day
)


data = data.drop(['admin1', 'admin2', 'latitude', 'longitude', 'usdprice'], axis=1).copy()
data = data.drop(data.index[0])

data = data.rename(columns={'data_year': 'year', 'data_month': 'month', 'data_day': 'day'})

categorical_columns = ['market', 'category', 'commodity', 'unit', 'priceflag', 'pricetype', 'currency']
data[categorical_columns] = data[categorical_columns].astype('category')

data['priceflag'] = data['priceflag'].str.replace('#', '').astype('category')
data['pricetype'] = data['pricetype'].str.replace('#', '').astype('category')


data['priceflag'] = data['priceflag'].astype(str)
data_info = data.info()
data_duplicate= data.duplicated().sum()
data_mixed = data['priceflag'].isnull().sum()
data_mixed_info = data['priceflag'].dtypes()
print(f"Number of duplicated rows: {data_duplicate}")

data_info= data.columns
print(data_info)

# Clean special characters
print(data['priceflag'].unique())
print(data['pricetype'].unique())
print(data['currency'].unique())




# line plot 
# price trend

#TODO provide boxplot to present the outlier
#TODO do hypothesis testing for the median trend
data_trend = data.loc[(data['market'] == 'National Average')]
data_trend_median = data_trend.groupby(['date', 'category'], observed=False)['price'].median().reset_index()
data_trend_median['date'] = pd.to_datetime(data_trend_median['date'])
data_trend_median = data_trend_median.dropna(subset=['price'])
numeric_date = pd.to_numeric(data_trend_median['date'])
print(numeric_date.dtypes)

model = sm.OLS(data_trend_median['price'], sm.add_constant(numeric_date)).fit()

print(data_trend_median[['price', 'date']].isnull().sum())
print(model.summary())

# Check data types
print(data_trend_median[['price', 'date']].dtypes)


data_trend_median_scatter = px.scatter(
    data_frame=data_trend_median,
    x='date',
    y="price",
    color="category",
    #line_dash="category", add detail (commodity) to hover
)

data_trend_median_scatter.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Price",
    title_text="Trend of Average Prices by Category Over the Years",
    title_font_family="Plus Jakarta Sans",
    title_font_size=24,
    title_font_color="black",
)

# Add the linear regression line
data_trend_median_scatter.add_trace(
    go.Scatter(
        x=data_trend_median['date'],
        y=model.predict(sm.add_constant(numeric_date)),
        mode='lines',
        line=dict(color="black", width=2),
        name="Linear Regression",
    )
)



data_trend_median_scatter.update_layout(
    xaxis_title="Date",
    yaxis_title="Median Price (in IDR)",
    title=dict(text="Median Prices by Category Over Time", font=dict(color="black", size=24, family="Plus Jakarta Sans")),
)

#data_trend_median_scatter.update_traces(mode='lines+markers')
#data_trend_median_scatter.show()


#descriptive stats ✅

#TODO export this to latex table
data_trend = data.loc[(data['market'] == 'National Average')]
data_trend['price'] = pd.to_numeric(data_trend['price'], errors='coerce').dropna()

data_desc = data_trend['price'].agg([np.mean, np.std, np.median, np.max, np.min])
print(data_desc.to_string())
data_desc_fig = px.box(data_trend, x='category', y='price', color='category')

print(pd.unique(data_trend['category']))
print(pd.isna(data_trend['category']).sum())

#continuous var analysis
#price
#descriptive ✅
#outlier detection: boxplot ✅
#distribution: histogram ✅

data_trend_histo = px.histogram(data_trend, x='price', labels={'price': 'Price'}, title='Distribution of Prices (National Average)')
data_trend_histo.show()

#discrete var analysis 🧑‍🍳
# category analysis median ranking (with bar chart) ✅

# category/commodity analysis
data_trend_median_category = data_trend.groupby(['category', 'commodity'], observed=False)['price'].median().reset_index()
data_trend_median_category = data_trend_median_category.dropna(subset=['price'])
data_trend_median_category['commodity'] = data_trend_median_category['commodity'].str.replace("'", "")
data_trend_median_category_sorted = data_trend_median_category.sort_values(by='price', ascending=False)
data_trend_median_category_sorted = data_trend_median_category_sorted[~(data_trend_median_category_sorted['commodity'] == 'Fuel (kerosene)')]

print(data_trend_median_category.columns)
print(pd.isna(data_trend_median_category['commodity']).sum())
missing_values_count = data_trend_median_category['price'].isnull().groupby(data_trend_median_category['commodity']).sum()
print(missing_values_count)
print(data_trend_median_category['commodity'].value_counts())

unique_commodities = pd.unique(data_trend_median_category_sorted['commodity']).tolist()
print(unique_commodities)

#todo apply the visual custom to other plots
#todo eliminate non food
#todo sort from highest
data_trend_median_bar = px.bar(
    data_frame=data_trend_median_category_sorted,
    x='commodity',
    y='price',
    color='commodity',
    labels={'price': 'Median Price (IDR)', 'commodity': 'Commodity'},
    title='Median Prices by Category Over 2007-2020',
    color_discrete_sequence=px.colors.qualitative.Pastel,
    template='plotly_white',
)

data_trend_median_bar.update_layout(
    xaxis_title='Category',
    yaxis_title='Median Price (IDR)',
    title_font_family="Plus Jakarta Sans",
    title_font_size=24,
    title_font_color="black",
)

data_trend_median_bar.show()

#correlation (price of milk and dairy & meat, fish, eggs)
#regression ✅

data_trend['price'] = pd.to_numeric(data_trend['price'], errors='coerce').dropna()


# Create a Q-Q plot
stats.probplot(data_trend['price'], dist="norm", plot=plt)
plt.title('Q-Q Plot - Normality Check for Price')
plt.show()


#spearman
#subset_data = data_trend[data_trend['category'].isin(['meat, fish, and eggs', 'milk and dairy'])]

# Calculate correlation ✅
'''
data_trend_reset = data_trend.reset_index(drop=True)
subset_data_one = data_trend_reset.loc[(data_trend['market'] == 'National Average') & (data_trend['category'] == 'meat, fish, and eggs')]
subset_data_two = data_trend_reset.loc[(data_trend['market'] == 'National Average') & (data_trend['category'] == 'milk and dairy')]
'''

data_trend_reset = data_trend.reset_index(drop=True)
subset_data_one = data_trend_reset.loc[(data_trend_reset['category'] == 'vegetables and fruits')]
subset_data_two = data_trend_reset.loc[(data_trend_reset['category'] == 'milk and dairy')]


# Check for unique values to identify variability
unique_values_one = subset_data_one['price'].unique()
unique_values_two = subset_data_two['price'].unique()

print("Unique values in 'vegetables and fruits':", unique_values_one)
print("Unique values in 'milk and dairy':", unique_values_two)

# Check for missing values
missing_values_one = subset_data_one['price'].isnull().any()
missing_values_two = subset_data_two['price'].isnull().any()

print("Missing values in 'vegetables and fruits':", missing_values_one)
print("Missing values in 'milk and dairy':", missing_values_two)

# Data exploration
print("Summary statistics for 'vegetables and fruits':")
print(subset_data_one['price'].describe())

print("Summary statistics for 'milk and dairy':")
print(subset_data_two['price'].describe())

spearman_corr = subset_data_one['price'].corr(subset_data_two['price'], method='spearman')
print(f"Spearman correlation between vegetables and fruits and milk and dairy: {spearman_corr}")

#spearman_corr = pd.DataFrame(spearman_corr)
corr_df = pd.DataFrame({'Spearman Correlation': [spearman_corr]})
sns.heatmap(corr_df, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Spearman Correlation Matrix')
plt.show()

#Display the correlation matrix
#print(spearman_corr)


#hypothesis testing (price and date, price and market, category and price) ✅
unique_category = pd.unique(data_trend['category']).tolist()
print(unique_category)


#Price Difference between between meat,fish, & eggs prices and vegetable & fruits' prices
data_category_1 = data_trend[data_trend['category'] == 'meat, fish and eggs']['price']
data_category_2 = data_trend[data_trend['category'] == 'vegetables and fruits']['price']

# Perform a t-test assuming unequal variances
t_stat, p_value = stats.ttest_ind(data_category_1, data_category_2, equal_var=False)

# Set your significance level (alpha)
alpha = 0.05

# Check the p-value against the significance level
# Null Hypothesis (H0): There is no significant difference in prices between meat,fish, & eggs prices and vegetable & fruits prices.
# Alternative Hypothesis (H1): There is a significant difference in prices between meat,fish, & eggs prices and vegetable & fruits' prices.


if p_value < alpha:
    print(f"Reject the null hypothesis. There is a significant difference between meat,fish, & eggs prices and vegetable & fruits prices.")
else:
    print("Fail to reject the null hypothesis. There is no significant difference between meat,fish, & eggs prices and vegetable & fruits prices.")



# Price Difference between 'cereals and tubers' prices and 'milk and dairy' prices
data_category_3 = data_trend[data_trend['category'] == 'cereals and tubers']['price']
data_category_4 = data_trend[data_trend['category'] == 'milk and dairy']['price']

# Perform a t-test assuming unequal variances
t_stat, p_value = stats.ttest_ind(data_category_3, data_category_4, equal_var=False)

# Set your significance level (alpha)
alpha = 0.05

# Check the p-value against the significance level
# Null Hypothesis (H0): There is no significant difference in prices between 'cereals and tubers' prices and 'milk and dairy' prices.
# Alternative Hypothesis (H1): There is a significant difference in prices between 'cereals and tubers' prices and 'milk and dairy' prices.

if p_value < alpha:
    print(f"Reject the null hypothesis. There is a significant difference between 'cereals and tubers' prices and 'milk and dairy' prices.")
else:
    print("Fail to reject the null hypothesis. There is no significant difference between 'cereals and tubers' prices and 'milk and dairy' prices.")



# Price Difference between 'oil and fats' prices and 'miscellaneous food' prices
data_category_5 = data_trend[data_trend['category'] == 'oil and fats']['price']
data_category_6 = data_trend[data_trend['category'] == 'miscellaneous food']['price']

# Perform a t-test assuming unequal variances
t_stat, p_value = stats.ttest_ind(data_category_5, data_category_6, equal_var=False)

# Set your significance level (alpha)
alpha = 0.05

# Check the p-value against the significance level
# Null Hypothesis (H0): There is no significant difference in prices between 'oil and fats' prices and 'miscellaneous food' prices.
# Alternative Hypothesis (H1): There is a significant difference in prices between 'oil and fats' prices and 'miscellaneous food' prices.


if p_value < alpha:
    print(f"Reject the null hypothesis. There is a significant difference between 'oil and fats' prices and 'miscellaneous food' prices.")
else:
    print("Fail to reject the null hypothesis. There is no significant difference between 'oil and fats' prices and 'miscellaneous food' prices.")
