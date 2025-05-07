from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df_filepath = Path('clean_data') / 'combined_data.csv'
df = pd.read_csv(df_filepath)

month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
               'November', 'December']
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
month_mapping = {'January': 'Jan', 'February': 'Feb', 'March': 'Mar', 'April': 'Apr', 'May': 'May', 'June': 'Jun',
                 'July': 'Jul', 'August': 'Aug', 'September': 'Sep', 'October': 'Oct', 'November': 'Nov',
                 'December': 'Dec'}
day_mapping = {'Monday': 'Mon', 'Tuesday': 'Tue', 'Wednesday': 'Wed', 'Thursday': 'Thu', 'Friday': 'Fri',
               'Saturday': 'Sat', 'Sunday': 'Sun'}


def total_trips_per_user():
    sns.set_theme(style='whitegrid')
    sns.countplot(
        data=df,
        x='member_casual',
        palette='Set2',
        hue='member_casual'
    )

    plt.title('Total number of trips per user type')
    plt.xlabel('')
    plt.ylabel('Total trips (millions)')
    plt.savefig('fig_1.jpg')
    plt.show()


def total_trips_per_rideable():
    trips_per_rideable = df.groupby(['member_casual', 'rideable_type'])['ride_id'].nunique().reset_index(name='count')
    trips_per_rideable['rideable_type'] = trips_per_rideable['rideable_type'].str.replace('_', ' ')

    sns.set_theme(style='whitegrid')
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


def total_trips_per_month():
    trips_per_month = df.groupby(['member_casual', 'ride_month'])['ride_id'].nunique().reset_index(name='count')
    trips_per_month['ride_month'] = pd.Categorical(trips_per_month['ride_month'], categories=month_order, ordered=True)
    trips_per_month['ride_month'] = trips_per_month['ride_month'].map(month_mapping)

    sns.set_theme(style='whitegrid')
    sns.lineplot(
        data=trips_per_month,
        x='ride_month',
        y='count',
        palette='Set2',
        hue='member_casual',
        marker='o'
    )

    plt.title('Total number of trips per month')
    plt.xlabel('')
    plt.ylabel('Total trips')
    plt.legend(title='User type')
    plt.savefig('fig_3.jpg')
    plt.show()


def total_trips_per_day():
    trips_per_day = df.groupby(['member_casual', 'ride_day'])['ride_id'].nunique().reset_index(name='count')
    trips_per_day['ride_day'] = pd.Categorical(trips_per_day['ride_day'], categories=day_order, ordered=True)
    trips_per_day['ride_day'] = trips_per_day['ride_day'].map(day_mapping)

    sns.set_theme(style='whitegrid')
    sns.lineplot(
        data=trips_per_day,
        x='ride_day',
        y='count',
        palette='Set2',
        hue='member_casual',
        marker='o'
    )

    plt.title('Total number of trips per day of the week')
    plt.xlabel('')
    plt.ylabel('Total trips')
    plt.legend(title='User type')
    plt.savefig('fig_4.jpg')
    plt.show()


def total_trips_per_hour():
    df['start_hour'] = pd.to_datetime(df['started_at']).dt.hour
    trips_per_hour = df.groupby(['member_casual', 'start_hour'])['ride_id'].nunique().reset_index(name='count')

    sns.set_theme(style='whitegrid')
    sns.lineplot(
        data=trips_per_hour,
        x='start_hour',
        y='count',
        palette='Set2',
        hue='member_casual',
        marker='o'
    )

    plt.title('Total number of trips per hour of day (0-24h)')
    plt.xlabel('')
    plt.ylabel('Total trips')
    plt.xticks(range(0, 24))
    plt.legend(title='User type')
    plt.savefig('fig_5.jpg')
    plt.show()


def avg_ride_length_per_user():
    avg_per_user = df.groupby('member_casual')['ride_length_min'].mean().reset_index(name='avg')

    sns.set_theme(style='whitegrid')
    sns.barplot(
        data=avg_per_user,
        x='member_casual',
        y='avg',
        palette='Set2',
        hue='member_casual'
    )

    plt.title('Average ride length per user type')
    plt.xlabel('')
    plt.ylabel('Average ride length (minutes)')
    plt.savefig('fig_6.jpg')
    plt.show()


def avg_ride_length_per_rideable():
    avg_per_rideable = df.groupby(['member_casual', 'rideable_type'])['ride_length_min'].mean().reset_index(name='avg')
    avg_per_rideable['rideable_type'] = avg_per_rideable['rideable_type'].str.replace('_', ' ')

    sns.set_theme(style='whitegrid')
    sns.barplot(
        data=avg_per_rideable,
        x='rideable_type',
        y='avg',
        palette='Set2',
        hue='member_casual'
    )

    plt.title('Average ride length per bike type')
    plt.xlabel('')
    plt.ylabel('Average ride length (minutes)')
    plt.legend(title='User Type')
    plt.tight_layout()
    plt.savefig('fig_7.jpg')
    plt.show()


def avg_ride_length_per_month():
    avg_per_month = df.groupby(['member_casual', 'ride_month'])['ride_length_min'].mean().reset_index(name='avg')
    avg_per_month['ride_month'] = pd.Categorical(avg_per_month['ride_month'], categories=month_order, ordered=True)
    avg_per_month['ride_month'] = avg_per_month['ride_month'].map(month_mapping)

    sns.set_theme(style='whitegrid')
    sns.lineplot(
        data=avg_per_month,
        x='ride_month',
        y='avg',
        palette='Set2',
        hue='member_casual',
        marker='o'
    )

    plt.title('Average ride length per month')
    plt.xlabel('')
    plt.ylabel('Average ride length (minutes)')
    plt.legend(title='User type')
    plt.savefig('fig_8.jpg')
    plt.show()


def avg_ride_length_per_day():
    avg_per_day = df.groupby(['member_casual', 'ride_day'])['ride_length_min'].mean().reset_index(name='avg')
    avg_per_day['ride_day'] = pd.Categorical(avg_per_day['ride_day'], categories=day_order, ordered=True)
    avg_per_day['ride_day'] = avg_per_day['ride_day'].map(day_mapping)

    sns.set_theme(style='whitegrid')
    sns.lineplot(
        data=avg_per_day,
        x='ride_day',
        y='avg',
        palette='Set2',
        hue='member_casual',
        marker='o'
    )

    plt.title('Average ride length per day of the week')
    plt.xlabel('')
    plt.ylabel('Average ride length (minutes)')
    plt.legend(title='User type')
    plt.savefig('fig_9.jpg')
    plt.show()


def avg_ride_length_per_hour():
    df['start_hour'] = pd.to_datetime(df['started_at']).dt.hour
    avg_per_hour = df.groupby(['member_casual', 'start_hour'])['ride_length_min'].mean().reset_index(name='avg')

    sns.set_theme(style='whitegrid')
    sns.lineplot(
        data=avg_per_hour,
        x='start_hour',
        y='avg',
        palette='Set2',
        hue='member_casual',
        marker='o'
    )

    plt.title('Average ride length per hour of day (0-24)')
    plt.xlabel('')
    plt.ylabel('Average ride length (minutes)')
    plt.xticks(range(0, 24))
    plt.legend(title='User type')
    plt.savefig('fig_10.jpg')
    plt.show()


def main():
    total_trips_per_user()
    total_trips_per_rideable()
    total_trips_per_month()
    total_trips_per_day()
    total_trips_per_hour()
    avg_ride_length_per_user()
    avg_ride_length_per_rideable()
    avg_ride_length_per_month()
    avg_ride_length_per_day()
    avg_ride_length_per_hour()


if __name__ == '__main__':
    main()
