from data_pipeline import start_pipeline
from database import connect_db
from data_analytics import *
from data_visualization import *
import json
import os

def save_analytics_data(yearly_crimes, crime_top5_cats, arrest_years, overall_arrest_rate):
    os.makedirs("static/analytics", exist_ok = True)

    data = {
        "yearly_crimes": yearly_crimes.to_dict(orient="records"),
        "crime_top5_cats": crime_top5_cats.to_dict(orient="records"),
        "arrest_years": arrest_years.to_dict(orient="records"),
        "overall_arrest_rate": overall_arrest_rate
    }

    with open("static/analytics/usecase4.json", "w",) as f:
        json.dump(data, f, indent = 4, default = str)


def save_outliers_info(outliers, stats):

    os.makedirs("static/analytics", exist_ok=True)
    filepath = "static/analytics/crime_outliers.txt"

    with open(filepath, "w") as file:

        file.write("=" * 60)
        file.write("\n\tCRIME COUNT OUTLIER ANALYSIS")
        file.write("\n" + "=" * 60)

        file.write("\n\nIQR STATISTICS")
        file.write("\n" + "-" * 40)

        file.write(f"\nQUARTER 1: {stats['quarter_1']}")
        file.write(f"\nQUARTER 3: {stats['quarter_3']}")
        file.write(f"\nIQR: {stats['IQR']}")
        file.write(f"\nLower Bound: {stats['lower_bound']}")
        file.write(f"\nUpper Bound: {stats['upper_bound']}")

        file.write("\n\nOUTLIER COMMUNITIES")
        file.write("\n" + "-" * 40)

        if outliers.empty:
            file.write("\nNo extreme crime-count outliers were identified.")

        else:
            file.write( "\n" + outliers[[ "COMMUNITY_CODE", "COMMUNITY_NAME", "TOTAL_CRIMES"]].to_string(index=False))

        file.write("\n\n" + "=" * 60)

    print(f"Outlier information saved to: {filepath}")

    return filepath

def run_analytics(processed_datasets):
    crime_data = processed_datasets["crime_data"]
    community_data = processed_datasets["city_community_data"]

    db_connection = connect_db()

    try:
        yearly_crimes = get_crime_yearly_trend(db_connection)

        crime_top10_cats = get_crime_by_category(db_connection, limit = 10)
        crime_top5_cats = get_crime_by_category(db_connection, limit = 5)

        yearly_arrests = get_arrest_count_yearly(db_connection)
        overall_arrest_rate, arrest_years = get_arrest_rates(crime_data, db_connection)

        arrest_outcome = get_arrest_outcome(crime_data)
        crime_month_day_data = get_crime_month_day_heatmap(crime_data)

        top_community_crimes = get_top_community_crime(crime_data, community_data, limit = 10)
        crime_by_day_hours = get_crime_hour_intensity(crime_data)

        mean_crime_boxplt, stats, outliers = get_mean_crime_boxplot(crime_data, community_data)

        crime_correlation = get_crime_correlation(crime_data)



        save_analytics_data(yearly_crimes, crime_top5_cats, arrest_years, overall_arrest_rate)

        

        plot_line_graph(data = yearly_crimes , x_axis = "INCIDENT_YEAR", y_axis = "TOTAL_CRIMES", graph_title = "Crime Trend Over Years", x_label = "Years",
                        y_label = "Total Num of Crimes", mark = "p", filename = "crime_yearly_trend.png", marksize = 8, linewidth = 2, color = "#E03F4F")

        plot_line_graph(data = crime_by_day_hours , x_axis = "HOUR", y_axis = "TOTAL_CRIMES", graph_title = "Crime Intensity by HOur", x_label = "Hour of Day",
                        y_label = "Number of Crimes", mark = "X", filename = "crime_hour_intensity.png", marksize = 8, linewidth = 2, color = "#EA591F")

        plot_bargraph(data = crime_top10_cats, x_axis = "CRIME_COUNT", y_axis = "PRIMARY_TYPE", graph_title="Top 10 Crime Categories", x_label="Number of Crimes",
                      y_label="Crime Category", filename="top_10_crime_categories.png", hue = "PRIMARY_TYPE", palette = "magma", legend = True, grid = True, annotate="CRIME_PERCENTAGE",
                      annotate_format=".2f", annotate_suffix="%")

        plot_bargraph(data = yearly_arrests, x_axis = "INCIDENT_YEAR", y_axis = "ARREST_COUNT", graph_title="Arrests Per Year", x_label="Years",
                      y_label="Number of Arrests", filename="arrests_yearly.png", hue = "ARREST_COUNT", palette = "summer", legend = True, grid = True, annotate="ARREST_PERCENTAGE",
                      annotate_format=".2f", annotate_suffix="%", orientation="vertical")

        plot_bargraph(data = top_community_crimes, x_axis = "TOTAL_CRIMES", y_axis = "COMMUNITY_NAME", graph_title="Top 10 Community Areas by Crime Count", x_label="Number of Crimes",
                      y_label="Community Area", filename="top_10_communities.png", hue = "COMMUNITY_NAME", palette = "Spectral", legend = True, grid = True, annotate="TOTAL_CRIMES",
                      annotate_format=",", annotate_suffix="")

        plot_boxplot(data = mean_crime_boxplt, column = "TOTAL_CRIMES", graph_title = "Distribution of Crime Counts Across Communities",
                     y_label = "Number of Crimes", filename = "community_crime_distribution.png")

        plot_piechart(data = arrest_outcome, labels = "OUTCOME", values = "CRIME_COUNT", graph_title = "Crime Outcomes - Arrest vs No Arrest",
                      filename = "arrest_outcome.png", explode = [0.05,0],shadow = False, colors = ["#BE5B50", "#FBDB93"])

        plot_heatmap(data = crime_correlation, graph_title = "Crime Feature Correlation Matrix", x_label = "Crime Features", y_label = "Crime Features",
            filename = "crime_correlation_heatmap.png", annotation = True, annotation_format = ".2f", color = "cividis")

        plot_heatmap(data = crime_month_day_data, graph_title = "Crime Frequency by Month and Day of Week", x_label = "Day of Week", y_label = "Month",
                     filename = "crime_month_day_heatmap.png", annotation = True, annotation_format = "d", color = "PiYG")

        save_outliers_info(outliers, stats)
        print("\nAnalytics completed successfully.")
        print("Visualizations generated successfully.")


    finally:

        db_connection.close()


def initial_setup():

    print("\n")
    print("=" * 60)
    print("INITIAL APPLICATION SETUP")
    print("=" * 60)

    processed_datasets = start_pipeline()
    run_analytics(processed_datasets)


    print("\n")
    print("=" * 60)
    print("INITIAL SETUP COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    initial_setup()
