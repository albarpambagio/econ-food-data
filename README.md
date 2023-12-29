# Food Price Data Analysis


## Overview
This repository contains Python scripts for analyzing food price data using pandas, Plotly, statsmodels, and other libraries. The analysis includes data loading, tidy operations, preprocessing, trend analysis, descriptive statistics, category analysis, correlation analysis, hypothesis testing, and report generation.

## Installation
To use the scripts, ensure you have the required dependencies installed:
```
pip install pandas plotly statsmodels numpy matplotlib mpld3 scipy seaborn ydata-profiling
```

## Usage
1. Clone the repository:
```
git clone https://github.com/your-username/food-price-analysis.git
cd food-price-analysis
```
2. Load and preprocess data:
```
from data_analysis import load_data, tidy_operations, preprocess_data

# Load data from CSV
data = load_data("your_data.csv")

# Perform tidy operations
tidy_data = tidy_operations(data)

# Preprocess the data
preprocessed_data = preprocess_data(tidy_data)
```
3. Analyze data:
```
from data_analysis import generate_profiling_report, analyze_price_trend, descriptive_statistics, category_analysis, correlation_analysis, hypothesis_testing

# Generate profiling report
generate_profiling_report(preprocessed_data)

# Analyze price trend
analyze_price_trend(preprocessed_data)

# Perform descriptive statistics
descriptive_statistics(preprocessed_data)

# Analyze prices by category
category_analysis(preprocessed_data)

# Perform correlation analysis
correlation_analysis(preprocessed_data)

# Perform hypothesis testing
hypothesis_testing(preprocessed_data)
```

## My System Information & Details
```
Last updated: 2023-12-29T13:10:50.171050+07:00

Python implementation: CPython
Python version       : 3.11.5
IPython version      : 8.18.1

Compiler    : GCC 11.2.0
OS          : Linux
Release     : 5.15.0-91-generic
Machine     : x86_64
Processor   : x86_64
CPU cores   : 4
Architecture: 64bit
```
