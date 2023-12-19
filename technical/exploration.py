import pandas as pd
#from ydata_profiling import ProfileReport

🧑‍🍳
#TODO data transform before viz
#TODO date data handling ✅ 

#tidy data
#TODO apply basic tidy data concept (cleansing) ✅ 
#TODO handle mixed data type
'''
mixed_type_columns = data.iloc[:, [4, 5, 12, 13]]
print(mixed_type_columns.applymap(type).nunique())
'''
#TODO check duplicated ✅
#TODO add comments/docstring
#TODO handle missing values 
#TODO apply some extended tidy data structure (if necessary)
#TODO handle outliers
#TODO data transformation https://aeturrell.github.io/coding-for-economists/data-transformation.html
#TODO data analysis, stats work, & visualization
#TODO OOP
#TODO deploy profiling to streamlit
#TODO minireport (keep it simple)





#hypothesis
#trends in price changes (weather, season, inflation)
#price Relationships between Categories
#income and food price
#nice-to-have for twitter thread: infrastucture and food price


csv_file_path = 'technical/data/food/wfp_food_prices_idn.csv'

'''profiling
profile = ProfileReport(
    data, minimal=True, title="Profiling Report: Food Price"
)
profile.to_file("your_report.html")
'''

data = pd.read_csv(csv_file_path)
data['price'] = pd.to_numeric(data['price'], errors='coerce')

data['date'] = pd.to_datetime(data['date'], errors='coerce', format='%Y-%m-%d')
data = data.assign(
    data_year=data['date'].dt.year,
    data_month=data['date'].dt.month,
    data_day=data['date'].dt.day
)
data = data.set_index('date')


#data_uncluttered = data.drop(['admin1', 'admin2', 'latitude', 'longitude', 'usdprice'], axis=1, inplace=True)
data_uncluttered = data.drop(['admin1', 'admin2', 'latitude', 'longitude', 'usdprice'], axis=1).copy()

data = data.rename(columns={'data_year': 'year', 'data_month': 'month', 'data_day': 'day'})

categorical_columns = ['market', 'category', 'commodity', 'unit', 'priceflag', 'pricetype', 'currency']
data[categorical_columns] = data[categorical_columns].astype('category')


data_info = data.info()
data_duplicate= data.duplicated().sum()
print(f"Number of duplicated rows: {data_duplicate}")

# data analysis





