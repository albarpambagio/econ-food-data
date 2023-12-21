import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import statsmodels.api as sm
#from ydata_profiling import ProfileReport

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
#TODO minireport (keep it simple)


#analyses
#trends in price changes (by category over the years) ✅
#seasonal decomposition
#correlation (income and food price) 🧑‍🍳
#outlier detection
#nice-to-have for twitter thread: infrastucture and food price 🧑‍🍳


csv_file_path = 'technical/data/food/wfp_food_prices_idn.csv'
csv_file_path_two = 'technical/data/food/Jalan Tol Beroperasi di Indonesia Tahun 2015.csv'

'''profiling
profile = ProfileReport(
    data, minimal=True, title="Profiling Report: Food Price"
)
profile.to_file("your_report.html")
'''

data = pd.read_csv(csv_file_path, low_memory=False)
data_two = pd.read_csv(csv_file_path_two, delimiter=';')
data['price'] = pd.to_numeric(data['price'], errors='coerce')

data['date'] = pd.to_datetime(data['date'], errors='coerce', format='%Y-%m-%d')
data = data.assign(
    data_year=data['date'].dt.year,
    data_month=data['date'].dt.month,
    data_day=data['date'].dt.day
)
#data = data.set_index('date')


#data_uncluttered = data.drop(['admin1', 'admin2', 'latitude', 'longitude', 'usdprice'], axis=1, inplace=True)
data = data.drop(['admin1', 'admin2', 'latitude', 'longitude', 'usdprice'], axis=1).copy()
data = data.drop(data.index[0])

data = data.rename(columns={'data_year': 'year', 'data_month': 'month', 'data_day': 'day'})

categorical_columns = ['market', 'category', 'commodity', 'unit', 'priceflag', 'pricetype', 'currency']
data[categorical_columns] = data[categorical_columns].astype('category')

data['priceflag'] = data['priceflag'].str.replace('#', '').astype('category')
data['pricetype'] = data['pricetype'].str.replace('#', '').astype('category')


#data['priceflag'] = data['priceflag'].astype(str)
#data_info = data.info()
#data_duplicate= data.duplicated().sum()
#data_mixed = data['priceflag'].isnull().sum()
#data_mixed_info = data['priceflag'].dtypes()
#print(f"Number of duplicated rows: {data_duplicate}")
#data_info= data.columns
#print(data_info)
# Clean special characters

#print(data['priceflag'].unique())
#print(data['pricetype'].unique())

#print(data['currency'].unique())

# tidy data
# melt
tidy_data_one = data.melt(id_vars=['market', 'year', 'month', 'day', 'price'], var_name='variables', value_vars=['category', 
  'commodity', 'unit', 'priceflag', 'pricetype', 'currency'])
#print(tidy_data_one.head(20))
#print(data.index)

#viz

# line plot 
# price trend

#TODO provide boxplot to present the outlier
#TODO do hypothesis testing for the median trend
data_trend = data.loc[(data['market'] == 'National Average')]
data_trend_median = data_trend.groupby(['date', 'category'], observed=False)['price'].median().reset_index()
data_trend_median['date'] = data_trend_median['date'].astype(str) 
#print(data_trend_mean.median(20))
'''
fig = px.line(
    data_frame=data_trend_median,
    x="date",
    y="price",
    color="category",
    line_dash="category",
)
'''

''' 
fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Price",
    title_text="Trend of Average Prices by Category Over the Years",
    title_font_family="Plus Jakarta Sans",
    title_font_size=24,
    title_font_color="black",
    title_font_weight="semibold",
)
'''

'''
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Median Price (in IDR)",
    title=dict(text="Median Prices by Category Over Time", font=dict(color="black", size=24, family="Plus Jakarta Sans")),
)
#fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
#fig.update_traces(mode='lines+markers', hovertemplate='%{text}', text=data_trend_mean['category'])
fig.update_traces(mode='lines+markers')

'''


#FOOD PRICE & TOLL DEVElOPMENT
#print(data_two.describe())
#print(data_two.info())
#print(data_one_two.columns)

data_one_two = pd.concat([data_trend_median, data_two], axis=1).sort_index()

data_two = data_two.reset_index(drop=True)
data_two = data_two.drop(index=[38, 39, 40])

''' 
#TODO tarik regresi
fig = px.line(
    data_frame=data_two,
    x="Tahun_Beroperasi",
    y="Jalan_Utama",
    color="Nama_Ruas",
    line_dash="Nama_Ruas",
)
fig.update_layout(
    xaxis_title="Tahun Beroperasi",
    yaxis_title="Panjang Tol (dalam km)",
    title=dict(text="Jalan Tol Beroperasi Tahun 1978-2015", font=dict(color="black", size=24, family="Plus Jakarta Sans")),
)

fig.update_traces(mode='lines+markers')

#fig.show()
#print(data_two.columns)
''' 

'''
status: not yet
#combining the two datasets
data_trend_median['year'] = pd.to_datetime(data_trend_median['date']).dt.year
data_two['Tahun_Beroperasi'] = pd.to_numeric(data_two['Tahun_Beroperasi'], errors='coerce').astype('Int64')

data_combined = pd.merge(data_trend_median, data_two, left_on='year', right_on='Tahun_Beroperasi', how='inner')
data_combined = data_combined.drop(columns=['Tahun_Beroperasi', 'year'])

# Create a subplot with two rows (one for line plot, one for scatter plot)
fig = make_subplots(rows=2, cols=1, subplot_titles=["Combined Data (Line Plot)", "Toll Data (Scatter Plot)"])

# Line Plot
fig.add_trace(
    go.Scatter(
        x=data_combined["date"],
        y=data_combined["price"],
        mode="lines+markers",
        marker=dict(size=8),
        line=dict(color="blue", dash="solid"),
        name="Line Plot",
    ),
    row=1,
    col=1,
)

# Scatter Plot (with a custom color scale)
color_scale = px.colors.qualitative.Set1  # You can choose a different color scale
category_colors = data_combined["category"].astype(str).map({category: color_scale[i % len(color_scale)] for i, category in enumerate(data_combined["category"].unique())})
fig.add_trace(
    go.Scatter(
        x=data_combined["date"],
        y=data_combined["price"],
        mode="markers",
        marker=dict(size=8, color=category_colors),
        name="Scatter Plot",
    ),
    row=2,
    col=1,
)

# Update layout
fig.update_layout(
    xaxis_title="Date",
    title_text="Combined Data Visualization",
    showlegend=False,
    height=600,
)

# Show the combined plot
fig.show()
'''