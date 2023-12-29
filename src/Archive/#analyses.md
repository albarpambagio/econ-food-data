#analyses
#trends in price changes (by category over the years) ✅
#seasonal decomposition
#correlation (income and food price) 🧑‍🍳
#outlier detection
#nice-to-have for twitter thread: infrastucture and food price (not yet/considered to be delayed)

#objectives
#descriptive stats (count, central tendency, variability, distribution)

#analisis mean (exclude: national average), modus, boxplot, stdev (can be clustered) ✅

#probability analysis
#probability analysis_discrete
#category and/or commodity with highest price
#probability analysis_continuous
#analisa variabel kontinu: proporsi a. daerah yang harganya berada di atas national average Rp. x b. ... di bawah national average
'''
Continuous Variable Analysis:

    Price Analysis:
        Variable: Price
        Analysis:
            Descriptive Statistics: Mean, Median, Standard Deviation, Range
            Distribution Plots: Histogram, Kernel Density Plot
            Outlier Detection: Box plots or Z-scores

    Spatial Analysis:
        Variables: Latitude, Longitude
        Analysis:
            Spatial Distribution Maps
            Spatial Autocorrelation Analysis
            Geographic Data Visualization

    Time Series Analysis:
        Variable: Date
        Analysis:
            Time Series Plots
            Seasonal Decomposition
            Autocorrelation and Partial Autocorrelation Functions

Discrete Variable Analysis:

    Categorical Analysis:
        Variables: Category, Commodity, Unit, Price Flag, Price Type, Currency
        Analysis:
            Frequency Tables
            Bar Charts
            Chi-square tests for independence (e.g., testing if the distribution of categories is independent of another variable)

    Market Analysis:
        Variable: Market
        Analysis:
            Frequency Tables
            Bar Charts
            Market Share Analysis

    Price Type Analysis:
        Variable: Price Type
        Analysis:
            Frequency Tables
            Bar Charts
            Comparisons of means (e.g., t-tests) for different price types

    Currency Analysis:
        Variable: Currency
        Analysis:
            Frequency Tables
            Bar Charts
            Comparisons of means (e.g., t-tests) for different currencies

    Commodity Analysis:
        Variable: Commodity
        Analysis:
            Frequency Tables
            Bar Charts
            Comparisons of means (e.g., ANOVA) for different commodities
'''
#correllation (price and time)
'''
    Geographical Variables:
        Latitude
        Longitude

    Price and Quantity Variables:
        Price
        Unit
        USD Price

    Time Series Variables:
        Date (if treated as a continuous variable)
        Price

    Commodity Type Variables:
        Category
        Commodity

    Price Type Variables:
        Price Flag
        Price Type
        '''
#hypothesis testing
'''
    Price Difference between Categories:
        Null Hypothesis (H0): There is no significant difference in prices between different categories.
        Alternative Hypothesis (H1): There is a significant difference in prices between different categories.
        Test: One-way Analysis of Variance (ANOVA) or t-tests for comparing means.

    Effect of Commodity Type on Price:
        Null Hypothesis (H0): The type of commodity does not significantly affect the price.
        Alternative Hypothesis (H1): The type of commodity has a significant effect on the price.
        Test: Analysis of Covariance (ANCOVA) or t-tests for comparing means.

    Geographical Variation in Prices:
        Null Hypothesis (H0): There is no spatial variation in prices (no correlation between prices and geographical location).
        Alternative Hypothesis (H1): There is a spatial variation in prices.
        Test: Spatial autocorrelation analysis or correlation tests.

    Temporal Trends in Prices:
        Null Hypothesis (H0): There is no significant temporal trend in prices over time.
        Alternative Hypothesis (H1): There is a significant temporal trend in prices.
        Test: Time series analysis or regression analysis.

    Price Difference by Price Type:
        Null Hypothesis (H0): There is no significant difference in prices between different price types.
        Alternative Hypothesis (H1): There is a significant difference in prices between different price types.
        Test: t-tests or Analysis of Variance (ANOVA).
'''