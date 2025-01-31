from datetime import datetime
import pandas as pd
import matplotlib
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from ml_engine import MLPredictor


def collect(msg):
    print(f"Message from producer: {msg} \n")

    data = [(datetime.utcfromtimestamp(int(ts) / 1000).strftime('%Y-%m-%d %H:%M:%S'), value) for ts, value in msg.items()]
    df = pd.DataFrame(data, columns=["Timestamp", "Value"])
    print(df)

    return df


def save_chart(pm25_df):
    # Set matplotlib to use Agg backend to avoid GTK3 issue
    matplotlib.use('Agg')

    plt.figure(figsize=(8, 4), dpi=200)
    plt.plot(pm25_df['Timestamp'], pm25_df['Value'], color="#FF3B1D", marker='.', linestyle="-")
    plt.title("PM2.5 Daily Averages Over Time")
    plt.xlabel("DateTime")
    plt.ylabel("Value")
    plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.grid()

    plt.savefig("output/Averages_over_time.png")


def predict(pm25_df):
    predictor = MLPredictor(pm25_df)
    predictor.train()
    forecast = predictor.predict()
    print(forecast)

    # Get canvas
    fig = predictor.plot_result(forecast)
    fig.savefig("output/prediction.png")
