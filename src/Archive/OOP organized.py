import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import statsmodels.api as sm
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
import seaborn as sns
from ydata_profiling import ProfileReport

# TODO: Add comments and docstring ✅
# TODO: Add exception handling ✅
# TODO: Handle variable names ✅
# TODO: Handle plotly layout ✅
# TODO: debugging ✅
# TODO: make modular code ✅
# TODO check the output

def load_data(csv_file_path):
    """
    Load data from a CSV file.

    Parameters:
    - csv_file_path (str): Path to the CSV file.

    Returns:
    - pd.DataFrame: Loaded data.

    Raises:
    - FileNotFoundError: If the specified file is not found.
    """
    
    try:
        data = pd.read_csv(csv_file_path, low_memory=False)
        return data
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {csv_file_path}") from e
    except Exception as e:
        raise Exception(f"Error loading data from {csv_file_path}: {str(e)}") from e

def tidy_operations(data):
    """
    Perform tidy operations on the data.

    This function extracts a subset of columns with mixed data types and prints the count of unique data types for each column.

    Parameters:
    - data (pd.DataFrame): Input data.

    Returns:
    - pd.DataFrame: Tidied data.
    """
    try:
        mixed_type_columns = data.iloc[:, [4, 5, 12, 13]]
        print(mixed_type_columns.applymap(type).nunique())
        return data
    except Exception as e:
        raise Exception(f"Error during tidy operations: {str(e)}") from e

def preprocess_data(data):
    """
    Preprocess the data.

    This function handles data cleaning tasks such as converting columns to appropriate data types, extracting date components,
    dropping unnecessary columns, handling missing values, and updating column names.

    Parameters:
    - data (pd.DataFrame): Input data.

    Returns:
    - pd.DataFrame: Preprocessed data.
    """
    try:
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
    except Exception as e:
        raise Exception(f"Error during data preprocessing: {str(e)}") from e

def generate_profiling_report(data):
    """
    Generate a profiling report for the data.

    This function generates a profiling report using the ydata_profiling library and saves it as an HTML file.

    Parameters:
    - data (pd.DataFrame): Input data.
    """
    
    try:
        profile = ProfileReport(data, minimal=True, title="Profiling Report: Food Price")
        profile.to_file("your_report.html")
    except Exception as e:
        raise Exception(f"Error generating profiling report: {str(e)}") from e

def set_common_plotly_layout(fig, x_title, y_title, title_text, legend_title=None):
    """
    Set common Plotly layout options.

    Parameters:
    - fig (plotly.graph_objects.Figure): Plotly figure object.
    - x_title (str): X-axis title.
    - y_title (str): Y-axis title.
    - title_text (str): Title text for the plot.
    - legend_title (str, optional): Legend title.
    """
    fig.update_layout(
        xaxis_title=x_title,
        yaxis_title=y_title,
        title_text=title_text,
    )

    if legend_title:
        fig.update_layout(
            legend=dict(title=dict(text=legend_title)),
        )
        
def analyze_price_trend(data):
    """
    Analyze the price trend over time.

    This function fits a linear regression model to analyze the trend of average prices by category over the years.

    Parameters:
    - data (pd.DataFrame): Input data.
    """
    
    try:
        #TODO consider to using non median data
        data_trend = data.loc[(data['market'] == 'National Average')]
        data_trend['price'] = pd.to_numeric(data_trend['price'], errors='coerce').dropna()
        data_trend_median = data_trend.groupby(['date', 'category'], observed=False)['price'].median().reset_index()
        data_trend_median['date'] = pd.to_datetime(data_trend_median['date'])
        data_trend_median = data_trend_median.dropna(subset=['price'])
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

        set_common_plotly_layout(
            data_trend_median_scatter,
            x_title="Date",
            y_title="Median Price (in IDR)",
            title_text="Median Prices by Category Over Time",
            legend_title="Category",
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
        
        data_trend_median_scatter.show()
    
    except Exception as e:
        raise Exception(f"Error analyzing price trend: {str(e)}") from e

def descriptive_statistics(data):
    """
    Perform descriptive statistics on the data.

    This function calculates descriptive statistics, creates a box plot, and a histogram to visualize the distribution of prices.

    Parameters:
    - data (pd.DataFrame): Input data.
    """

    try:
        data_trend = data.loc[(data['market'] == 'National Average')]
        data_trend['price'] = pd.to_numeric(data_trend['price'], errors='coerce').dropna()
        data_desc = data_trend['price'].agg([np.mean, np.std, np.median, np.max, np.min])
        print(data_desc.to_string())
        
        data_desc_fig = px.box(data_trend, x='category', y='price', color='category')
        set_common_plotly_layout(
            data_desc_fig,
            x_title="Category",
            y_title="Price",
            title_text="Distribution of Prices (National Average)",
            legend_title="Category",
        )
        data_desc_fig.show()
        
        print(pd.unique(data_trend['category']))
        print(pd.isna(data_trend['category']).sum())
        data_trend_histo = px.histogram(data_trend, x='price', labels={'price': 'Price'}, title='Distribution of Prices (National Average)')
        set_common_plotly_layout(
            data_trend_histo,
            x_title="Price",
            y_title="Count",
            title_text="Distribution of Prices (National Average)",
        )
        data_trend_histo.show()
    except Exception as e:
        raise Exception(f"Error calculating descriptive statistics: {str(e)}") from e

def category_analysis(data):
    """
    Analyze prices by category.

    This function analyzes median prices by category over a specified time range and creates a bar chart.

    Parameters:
    - data (pd.DataFrame): Input data.
    """

    try:    
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
        
        set_common_plotly_layout(
            data_trend_median_bar,
            x_title='Category',
            y_title='Median Price (IDR)',
            title_text='Median Prices by Category Over 2007-2020',
            legend_title='Commodity',
        )
        
        data_trend_median_bar.update_layout(
            title_font_family="Plus Jakarta Sans",
            title_font_size=24,
            title_font_color="black",
        )
        
        data_trend_median_bar.show()
    except Exception as e:
        raise Exception(f"Error during category analysis: {str(e)}") from e
    
def correlation_analysis(data):
    """
    Perform correlation analysis.

    This function performs a normality check, compares unique values, handles missing values,
    calculates summary statistics, and calculates the Spearman correlation between two categories.

    Parameters:
    - data (pd.DataFrame): Input data.
    """
    
    try:
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
        plt.show()
    except Exception as e:
        raise Exception(f"Error during correlation analysis: {str(e)}") from e

def hypothesis_testing(data):
    """
    Perform hypothesis testing.

    This function conducts independent t-tests to compare prices between different categories and prints the results.

    Parameters:
    - data (pd.DataFrame): Input data.
    """

    unique_category = pd.unique(data['category']).tolist()
    print(unique_category)

    try:
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
    except Exception as e:
        raise Exception(f"Error during hypothesis testing: {str(e)}") from e

if __name__ == "__main__":
    CSV_FILE_PATH = 'technical/data/food/wfp_food_prices_idn.csv'

    try:
        data = load_data(CSV_FILE_PATH)

        tidy_data = tidy_operations(data)

        preprocessed_data = preprocess_data(tidy_data)

        generate_profiling_report(preprocessed_data)

        analyze_price_trend(preprocessed_data)

        descriptive_statistics(preprocessed_data)

        category_analysis(preprocessed_data)

        correlation_analysis(preprocessed_data)

        hypothesis_testing(preprocessed_data)
    except Exception as e:
        print(f"An error occurred: {str(e)}")