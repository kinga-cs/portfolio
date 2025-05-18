from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_filepath = Path('..') / ('clean_data') / 'combined_data.csv'
df = pd.read_csv(df_filepath)

month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
               'November', 'December']
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
month_mapping = {'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr', 'May': 'May', 'June': 'Jun',
                 'July': 'Jul', 'August': 'Aug', 'September': 'Sep', 'October': 'Oct', 'November': 'Nov',
                 'December': 'Dec'}
day_mapping = {'Monday': 'Mon', 'Tuesday': 'Tue', 'Wednesday': 'Wed', 'Thursday': 'Thu', 'Friday': 'Fri',
               'Saturday': 'Sat', 'Sunday': 'Sun'}

def total_trips_per_rideable():
    trips_per_rideable = df.groupby(['member_casual', 'rideable_type'])['ride_id'].nunique().reset_index(name='count')
    trips_per_rideable['rideable_type'] = trips_per_rideable['rideable_type'].str.replace('_', ' ')

    sns.set_theme(style='whitegrid')
    plt.figure(figsize=(8, 4))
    sns.barplot(
        data=trips_per_rideable,
        x='rideable_type',
        y='count',
        hue='member_casual',
        palette='Set2')

    plt.title('Total number of trips per bike type')
    plt.xlabel('')
    plt.ylabel('Total trips (millions)')
    plt.legend(title='User type')
    plt.tight_layout()
    plt.savefig('fig_2.jpg')
    plt.show()


total_trips_per_rideable()
