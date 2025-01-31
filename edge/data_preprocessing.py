import requests
from datetime import datetime


def fetch_pm25_data():
    url = "https://newcastle.urbanobservatory.ac.uk/api/v1.1/sensors/PER_AIRMON_MONITOR1135100/data/json/" \
          "?starttime=20230601&endtime=20230831"

    resp = requests.get(url)
    raw_data_dict = resp.json()

    pm25_data = []
    sensor_data = raw_data_dict.get("sensors", [])[0].get("data", {}).get("PM2.5", [])

    for record in sensor_data:
        timestamp = record.get("Timestamp")
        value = record.get("Value")
        pm25_data.append({"Timestamp": timestamp, "Value": value})

    return pm25_data


def remove_outliers(pm25_data_with_outliers):
    outlier_data = []

    for entry in pm25_data_with_outliers:
        value = entry.get("Value")
        if value > 50:
            outlier_data.append(entry)

    print(f"Outlier data {outlier_data}")

    data_wout_outliers = [i for i in pm25_data_with_outliers if i not in outlier_data]
    return data_wout_outliers


def calculate_24hour_average(clean_data):
    data_by_day = {}

    # First data record's timestamp collected to group data by 24-hour blocks
    start_timestamp = clean_data[0].get("Timestamp")
    current_day_values = []
    current_day_start = start_timestamp

    # Used for calculating which day number to assign to current record
    ms_per_day = 86400000

    for entry in clean_data:
        # Calculate the day number by finding how many full 24-hour intervals since start (// division stores ints)
        day_number = (entry['Timestamp'] - start_timestamp) // ms_per_day

        # If a new day has started, calculate and store the average for the previous day
        if day_number > (current_day_start - start_timestamp) // ms_per_day:
            # Calculate average for the current day and assign to the first timestamp
            data_by_day[current_day_start] = sum(current_day_values) / len(current_day_values)
            # Reset values for the next day
            current_day_start = entry['Timestamp']
            current_day_values = []

        # Append the values for the current day
        current_day_values.append(entry['Value'])

    # Handle last day's values
    if current_day_values:
        data_by_day[current_day_start] = sum(current_day_values) / len(current_day_values)

    for timestamp, avg in data_by_day.items():
        date = datetime.utcfromtimestamp(int(timestamp) / 1000).strftime('%Y-%m-%d %H:%M:%S')
        print(f"Date {date}, Average: {avg:.2f}")

    return data_by_day


def get_averaged_data():
    pm25_data = fetch_pm25_data()
    pm25_data = remove_outliers(pm25_data)
    pm25_averages = calculate_24hour_average(pm25_data)

    return pm25_averages


if __name__ == '__main__':
    data = fetch_pm25_data()
    print(data)
