import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import statsmodels.api as sm
from scipy.stats import pearsonr
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
#nice-to-have for twitter thread: infrastucture and food price (not yet/considered to be delayed)

#objectives
#descriptive stats (count, central tendency, variability, distribution)
#probability analysis
#correllation
#hypothesis testing



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
data_trend_median['date'] = pd.to_datetime(data_trend_median['date'])
data_trend_median = data_trend_median.dropna(subset=['price'])
numeric_date = pd.to_numeric(data_trend_median['date'])

#print(numeric_date.dtypes)

model = sm.OLS(data_trend_median['price'], sm.add_constant(numeric_date)).fit()
#model = sm.OLS(data_two_filtered['Jalan_Utama'], sm.add_constant(data_two_filtered['Tahun_Beroperasi'])).fit()

#print(data_trend_median[['price', 'date']].isnull().sum())
#print(model.summary())

# Check data types
#print(data_trend_median[['price', 'date']].dtypes)


fig = px.scatter(
    data_frame=data_trend_median,
    x='date',
    y="price",
    color="category",
    #line_dash="category", add detail (commodity) to hover
)

fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Price",
    title_text="Trend of Average Prices by Category Over the Years",
    title_font_family="Plus Jakarta Sans",
    title_font_size=24,
    title_font_color="black",
)

# Add the linear regression line
fig.add_trace(
    go.Scatter(
        x=data_trend_median['date'],
        y=model.predict(sm.add_constant(numeric_date)),
        mode='lines',
        line=dict(color="black", width=2),
        name="Linear Regression",
    )
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
#fig.update_traces(mode='lines+markers')
#fig.show()

'''

#FOOD PRICE & TOLL DEVElOPMENT
#print(data_two.describe())
#print(data_two.info())
#print(data_one_two.columns)

data_one_two = pd.concat([data_trend_median, data_two], axis=1).sort_index()

data_two = data_two.reset_index(drop=True)
data_two = data_two.drop(index=[38, 39, 40])


#TODO tarik regresi
data_two['Tahun_Beroperasi'] = pd.to_numeric(data_two['Tahun_Beroperasi'], errors='coerce').astype('float64')
data_two = data_two.sort_values(by=['Tahun_Beroperasi'])
data_two_filtered = data_two.loc[data_two['Tahun_Beroperasi'] >= 2008]
#print(data_two_filtered.head(5))

model = sm.OLS(data_two_filtered['Jalan_Utama'], sm.add_constant(data_two_filtered['Tahun_Beroperasi'])).fit()
print(model.summary())

fig = px.scatter(
    data_frame=data_two_filtered,
    x="Tahun_Beroperasi",
    y="Jalan_Utama",
    color="Nama_Ruas",
)

# Add the linear regression line
fig.add_trace(
    go.Scatter(
        x=data_two_filtered['Tahun_Beroperasi'],
        y=model.predict(sm.add_constant(data_two_filtered['Tahun_Beroperasi'])),
        mode='lines',
        line=dict(color="black", width=2),
        name="Linear Regression",
    )
)


fig.update_layout(
    xaxis_title="Tahun Beroperasi",
    yaxis_title="Panjang Tol (dalam km)",
    title=dict(text="Jalan Tol Beroperasi Tahun 2008-2015", font=dict(color="black", size=24, family="Plus Jakarta Sans")),
)

fig.update_traces(mode='lines+markers')

fig.show()


unique_values = data_two_filtered['Tahun_Beroperasi'].unique()

#print(unique_values)
#print(data_two.dtypes)
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

#TODO data transform first data set, so it'll match the latter
# take the median of each year ()

#print(data_trend_median.info())
#print(data_trend_median.columns)

#data_trend_median = data_trend.groupby(['date', 'category'], observed=False)['price'].median().reset_index()
data_trend_median_yearly = data_trend.groupby([data_trend['date'].dt.year, 'category'], observed=False)['price'].median().reset_index()
data_trend_median_yearly.rename(columns={'date': 'Tahun_Beroperasi'}, inplace=True)
data_two['Tahun_Beroperasi'] = pd.to_numeric(data_two['Tahun_Beroperasi'], errors='coerce').astype('Int64')

data_combined = pd.merge(data_trend_median_yearly, data_two, how='outer', on='Tahun_Beroperasi')
data_combined = data_combined.drop(['BUJT', 'Jalan_Akses'], axis=1).copy()


#print(data_trend_median_yearly.dtypes)
pd.set_option('display.max_columns', None)
#print(data_combined.head(20))
#print(data_combined.columns)
#data_trend_median_combine = data_trend_median.iloc

#TODO filter tahun range 2007-2015
#TODO merge catgeory into one 
fig = px.scatter(
    data_frame=data_combined,
    x='Tahun_Beroperasi',
    y=["price", 'Jalan_Utama'],
    color="category",
    #line_dash="category", add detail (commodity) to hover
)

'''
fig.update_layout(
    xaxis_title="Year",
    yaxis_title="Average Price",
    title_text="Trend of Average Prices by Category Yearly",
    title_font_family="Plus Jakarta Sans",
    title_font_size=24,
    title_font_color="black",
)
'''
fig.update_layout(
    xaxis_title="Year of Operation",
    yaxis_title="Values",
    title_text="Scatter Plot of Tahun_Beroperasi, Price, and Jalan_Utama",
    title_font_family="Plus Jakarta Sans",
    title_font_size=24,
    title_font_color="black",
)



'''
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Median Price (in IDR)",
    title=dict(text="Median Prices by Category Over Time", font=dict(color="black", size=24, family="Plus Jakarta Sans")),
)
'''
#fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
#fig.update_traces(mode='lines+markers', hovertemplate='%{text}', text=data_trend_mean['category'])
#fig.update_traces(mode='lines+markers')
#print(data_trend_median_yearly.dtypes)

#fig.show()
