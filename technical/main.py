# main_script.py

from watermark import watermark
from data_loading import load_data
from data_operations import tidy_operations, preprocess_data
from data_analysis import (
    generate_profiling_report,
    analyze_price_trend,
    descriptive_statistics,
    category_analysis,
    correlation_analysis,
    hypothesis_testing,
)

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

print(watermark())