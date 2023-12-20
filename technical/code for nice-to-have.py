import pandas as pd
import statsmodels.api as sm
import plotly.express as px

# Assuming you have a DataFrame named 'data' with relevant columns

# Step 1: Data Preprocessing
# Merge datasets or select relevant columns
# Handle missing values and outliers

# Step 2: Explore Data
# Provide summary statistics
print(data.describe())

# Step 3: Correlation Analysis
correlation_matrix = data.corr()

# Plot heatmap using Plotly
fig = px.imshow(correlation_matrix,
                labels=dict(x="Variables", y="Variables", color="Correlation"),
                x=correlation_matrix.columns,
                y=correlation_matrix.columns,
                color_continuous_scale="coolwarm")

fig.update_layout(title="Correlation Matrix", width=800, height=600)
fig.show()

# Step 4: Regression Analysis
# Assuming 'food_price' is the dependent variable and 'toll_road_length' is an independent variable
X = data[['toll_road_length']]  # Independent variable(s)
y = data['food_price']  # Dependent variable

# Add a constant term to the independent variables
X = sm.add_constant(X)

# Fit the regression model
model = sm.OLS(y, X).fit()

# Step 5: Interpret Results
print(model.summary())

# Step 6: Visualize Regression Line
fig = px.scatter(data, x='toll_road_length', y='food_price', title='Regression Analysis: Toll Road Length vs. Food Price')
fig.add_trace(px.line(x=data['toll_road_length'], y=model.predict(X), name='Regression Line').data[0])

fig.show()
