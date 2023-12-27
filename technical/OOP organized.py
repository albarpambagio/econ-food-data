import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
from ydata_profiling import ProfileReport

#TODO add comments and docstring
#TODO add exception handling
#TODO handle variable names
#TODO handle plotly layout 

def load_data(CSV_FILE_PATH):
    try:
        data = pd.read_csv(CSV_FILE_PATH, low_memory=False)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {CSV_FILE_PATH}")
    
def tidy_operations(data):
    mixed_type_columns = data.iloc[:, [4, 5, 12, 13]]
    print(mixed_type_columns.applymap(type).nunique())
    return data

def preprocess_data(data):
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
    data_duplicate = data.duplicated().sum()
    print(f"Number of duplicated rows: {data_duplicate}")
    data_info = data.columns
    print(data_info)
    return data

def generate_profiling_report(data):
    profile = ProfileReport(data, minimal=True, title="Profiling Report: Food Price")
    profile.to_file("your_report.html")

def analyze_price_trend(data):
    data_trend = data.loc[(data['market'] == 'National Average')]
    data_trend_median = data_trend.groupby(['date', 'category'], observed=False)['price'].median().reset_index()
    numeric_date = pd.to_numeric(data_trend_median['date'])
    model = sm.OLS(data_trend_median['price'], sm.add_constant(numeric_date)).fit()
    print(data_trend_median[['price', 'date']].isnull().sum())
    print(model.summary())

    data_trend_median_scatter = px.scatter(
        data_frame=data_trend_median,
        x='date',
        y="price",
        color="category",
    )

    data_trend_median_scatter.update_layout(
        xaxis_title="Year",
        yaxis_title="Average Price",
        title_text="Trend of Average Prices by Category Over the Years",
    )

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
        title=dict(text="Median Prices by Category Over Time"),
    )

    #data_trend_median_scatter.show()

def descriptive_statistics(data):
    data_trend = data.loc[(data['market'] == 'National Average')]
    data_trend['price'] = pd.to_numeric(data_trend['price'], errors='coerce').dropna()
    data_desc = data_trend['price'].agg([np.mean, np.std, np.median, np.max, np.min])
    print(data_desc.to_string())
    data_desc_fig = px.box(data_trend, x='category', y='price', color='category')
    print(pd.unique(data_trend['category']))
    print(pd.isna(data_trend['category']).sum())
    data_trend_histo = px.histogram(data_trend, x='price', labels={'price': 'Price'}, title='Distribution of Prices (National Average)')
    #data_trend_histo.show()


def category_analysis(data):
    data_trend = data.loc[(data['market'] == 'National Average')]
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
    #data_trend_median_bar.show()

def correlation_analysis(data):
    data_trend = data.loc[(data['market'] == 'National Average')]
    data_trend['price'] = pd.to_numeric(data_trend['price'], errors='coerce').dropna()
    stats.probplot(data_trend['price'], dist="norm", plot=plt)
    plt.title('Q-Q Plot - Normality Check for Price')
    plt.show()
    data_trend_reset = data_trend.reset_index(drop=True)
    subset_data_one = data_trend_reset.loc[(data_trend_reset['category'] == 'vegetables and fruits')]
    subset_data_two = data_trend_reset.loc[(data_trend_reset['category'] == 'milk and dairy')]
    unique_values_one = subset_data_one['price'].unique()
    unique_values_two = subset_data_two['price'].unique()
    print("Unique values in 'vegetables and fruits':", unique_values_one)
    print("Unique values in 'milk and dairy':", unique_values_two)
    missing_values_one = subset_data_one['price'].isnull().any()
    missing_values_two = subset_data_two['price'].isnull().any()
    print("Missing values in 'vegetables and fruits':", missing_values_one)
    print("Missing values in 'milk and dairy':", missing_values_two)
    print("Summary statistics for 'vegetables and fruits':")
    print(subset_data_one['price'].describe())
    print("Summary statistics for 'milk and dairy':")
    print(subset_data_two['price'].describe())
    spearman_corr = subset_data_one['price'].corr(subset_data_two['price'], method='spearman')
    print(f"Spearman correlation between vegetables and fruits and milk and dairy: {spearman_corr}")
    corr_df = pd.DataFrame({'Spearman Correlation': [spearman_corr]})
    sns.heatmap(corr_df, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Spearman Correlation Matrix')
    #plt.show()

def hypothesis_testing(data):
    unique_category = pd.unique(data['category']).tolist()
    print(unique_category)

    data_category_1 = data[data['category'] == 'meat, fish and eggs']['price']
    data_category_2 = data[data['category'] == 'vegetables and fruits']['price']

    t_stat, p_value = stats.ttest_ind(data_category_1, data_category_2, equal_var=False)
    alpha = 0.05

    if p_value < alpha:
        print(f"Reject the null hypothesis. There is a significant difference between meat, fish, & eggs prices and vegetable & fruits prices.")
    else:
        print("Fail to reject the null hypothesis. There is no significant difference between meat, fish, & eggs prices and vegetable & fruits prices.")

    data_category_3 = data[data['category'] == 'cereals and tubers']['price']
    data_category_4 = data[data['category'] == 'milk and dairy']['price']

    t_stat, p_value = stats.ttest_ind(data_category_3, data_category_4, equal_var=False)
    alpha = 0.05

    if p_value < alpha:
        print(f"Reject the null hypothesis. There is a significant difference between 'cereals and tubers' prices and 'milk and dairy' prices.")
    else:
        print("Fail to reject the null hypothesis. There is no significant difference between 'cereals and tubers' prices and 'milk and dairy' prices.")

    data_category_5 = data[data['category'] == 'oil and fats']['price']
    data_category_6 = data[data['category'] == 'miscellaneous food']['price']

    t_stat, p_value = stats.ttest_ind(data_category_5, data_category_6, equal_var=False)
    alpha = 0.05

    if p_value < alpha:
        print(f"Reject the null hypothesis. There is a significant difference between 'oil and fats' prices and 'miscellaneous food' prices.")
    else:
        print("Fail to reject the null hypothesis. There is no significant difference between 'oil and fats' prices and 'miscellaneous food' prices.")

if __name__ == "__main__":
    CSV_FILE_PATH = 'technical/data/food/wfp_food_prices_idn.csv'

    data = load_data(CSV_FILE_PATH)

    tidy_data = tidy_operations(data)

    preprocessed_data = preprocess_data(tidy_data)

    generate_profiling_report(preprocessed_data)

    analyze_price_trend(preprocessed_data)

    descriptive_statistics(preprocessed_data)

    category_analysis(preprocessed_data)

    correlation_analysis(preprocessed_data)

    hypothesis_testing(preprocessed_data)
