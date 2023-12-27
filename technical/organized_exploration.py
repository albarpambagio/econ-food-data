import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
from ydata_profiling import ProfileReport

# Set CSV file paths
csv_file_path = 'technical/data/food/wfp_food_prices_idn.csv'
csv_file_path_two = 'technical/data/food/Jalan Tol Beroperasi di Indonesia Tahun 2015.csv'

# Load data from CSV files
data = pd.read_csv(csv_file_path, low_memory=False)
data_two = pd.read_csv(csv_file_path_two, delimiter=';')

# Profile the data
profile = ProfileReport(data, minimal=True, title="Profiling Report: Food Price")
profile.to_file("your_report.html")

# Data preprocessing
data['price'] = pd.to_numeric(data['price'], errors='coerce')
data['date'] = pd.to_datetime(data['date'], errors='coerce', format='%Y-%m-%d')
data = data.assign(data_year=data['date'].dt.year, data_month=data['date'].dt.month, data_day=data['date'].dt.day)
data = data.drop(['admin1', 'admin2', 'latitude', 'longitude', 'usdprice'], axis=1).copy()
data = data.drop(data.index[0])
data = data.rename(columns={'data_year': 'year', 'data_month': 'month', 'data_day': 'day'})
categorical_columns = ['market', 'category', 'commodity', 'unit', 'priceflag', 'pricetype', 'currency']
data[categorical_columns] = data[categorical_columns].astype('category')
data['priceflag'] = data['priceflag'].str.replace('#', '').astype('category')
data['pricetype'] = data['pricetype'].str.replace('#', '').astype('category')

# Data visualization
data_trend = data.loc[(data['market'] == 'National Average')]
data_trend_median = data_trend.groupby(['date', 'category'], observed=False)['price'].median().reset_index()
data_trend_median['date'] = pd.to_datetime(data_trend_median['date'])
data_trend_median = data_trend_median.dropna(subset=['price'])
numeric_date = pd.to_numeric(data_trend_median['date'])
model = sm.OLS(data_trend_median['price'], sm.add_constant(numeric_date)).fit()

# Descriptive statistics
data_trend = data.loc[(data['market'] == 'National Average')]
data_trend['price'] = pd.to_numeric(data_trend['price'], errors='coerce').dropna()
data_desc = data_trend['price'].agg([np.mean, np.std, np.median, np.max, np.min])
data_desc_fig = px.box(data_trend, x='category', y='price', color='category')

# Continuous variable analysis - Price
data_trend_histo = px.histogram(data_trend, x='price', labels={'price': 'Price'}, title='Distribution of Prices (National Average)')

# Category/commodity analysis
data_trend_median_category = data_trend.groupby(['category', 'commodity'], observed=False)['price'].median().reset_index()
data_trend_median_category = data_trend_median_category.dropna(subset=['price'])
data_trend_median_category['commodity'] = data_trend_median_category['commodity'].str.replace("'", "")
data_trend_median_category_sorted = data_trend_median_category.sort_values(by='price', ascending=False)
data_trend_median_category_sorted = data_trend_median_category_sorted[~(data_trend_median_category_sorted['commodity'] == 'Fuel (kerosene)')]

# Bar chart for median prices by category
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

# Spearman correlation
data_trend_reset = data_trend.reset_index(drop=True)
subset_data_one = data_trend_reset.loc[(data_trend_reset['category'] == 'vegetables and fruits')]
subset_data_two = data_trend_reset.loc[(data_trend_reset['category'] == 'milk and dairy')]
spearman_corr = subset_data_one['price'].corr(subset_data_two['price'], method='spearman')
corr_df = pd.DataFrame({'Spearman Correlation': [spearman_corr]})
sns.heatmap(corr_df, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Spearman Correlation Matrix')

# Hypothesis testing
data_category_5 = data_trend[data_trend['category'] == 'oil and fats']['price']
data_category_6 = data_trend[data_trend['category'] == 'miscellaneous food']['price']
t_stat, p_value = stats.ttest_ind(data_category_5, data_category_6, equal_var=False)
alpha = 0.05

if p_value < alpha:
    print(f"Reject the null hypothesis. There is a significant difference between 'oil and fats' prices and 'miscellaneous food' prices.")
else:
    print("Fail to reject the null hypothesis. There is no significant difference between 'oil and fats' prices and 'miscellaneous food' prices.")
