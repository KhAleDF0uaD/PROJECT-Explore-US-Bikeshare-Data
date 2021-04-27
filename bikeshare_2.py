import time
import pandas as pd
import numpy as np

CITY_DATA = { 'ch': 'chicago.csv',
              'ny': 'new_york_city.csv',
              'w': 'washington.csv' }
def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('To view the available bikeshare data, kindly type:\n (ch) for Chicago\n (ny) for New York City\n (w) for Washington:\n ').lower()

    while city not in {'ch','ny','w'}:
        print('That\'s invalid input.')
        city = input('To view the available bikeshare data, kindly type:\n (ch) for Chicago\n (ny) for New York City\n (w) for Washington:\n ').lower()

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = input('\n\nTo filter {}\'s data by a particular month, please type the month or all for not filtering by month:\n-January\n-February\n-March\n-April\n-May\n-June\n-All\n\n:'.format(city.title())).lower()

    while month not in months:
        print("That's invalid choice, please type a valid month name or all.")
        month = input('\n\nTo filter {}\'s data by a particular month, please type the month or all for not filtering by month:\n-January\n-February\n-March\n-April\n-May\n-June\n-All\n\n:'.format(city.title())).lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = input('\n\nTo filter {}\'s data by a particular day, please type the day or all for not filtering by day:\n-monday\n-tuesday\n-wednesday\n-thursday\n-friday\n-saturday\n-Sunday\n-All\n\n:'.format(city.title())).lower()

    while day not in days:
        print('Wrong entry, come on! just enter a right day name or all.')
        day = input('\n\nTo filter {}\'s data by a particular day, please type the day or all for not filtering by day:\n-monday\n-tuesday\n-wednesday\n-thursday\n-friday\n-saturday\n-Sunday\n-All\n\n:'.format(city.title())).lower()


    return city, month, day


def load_data(city, month, day):
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]

    print('Most Common Month is:', most_common_month)
    print('Most Common Day is:', most_common_day)
    print('Most Common Hour is:', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_commonly_used_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    most_commonly_used_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    df['route'] = df['Start Station'] + '-' + df['End Station']
    most_frequent_route = df['route'].mode()[0]

    print('most commonly used start station is:', most_commonly_used_start_station)
    print('most commonly used end station is:', most_commonly_used_end_station)
    print('most frequent route is:', most_frequent_route)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time (in seconds) is: ' + str(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time (in seconds) is: ' + str(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Counts of user types : \n" + str(user_types))

    if CITY_DATA == 'chicago.csv' or CITY_DATA == 'new_york_city.csv':
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print("Counts of gender : \n" + str(gender))

    # Display earliest, most recent, and most common year of birth
        earliest_birth = df['Birth Year'].min()
        most_recent_birth = df['Birth Year'].max()
        most_common_birth = df['Birth Year'].mode()[0]
        print('Earliest birth is: {}\n'.format(earliest_birth))
        print('Most recent birth is: {}\n'.format(most_recent_birth))
        print('Most common birth is: {}\n'.format(most_common_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):

    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nWould you like to view next five row of raw data? Enter yes or no.\n')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df.head())

        time_stats(df)

        station_stats(df)

        trip_duration_stats(df)

        user_stats(df)

        while True:
            view_raw_data = input('\nRaw data is available to check...would you like to view first five row of raw data? Enter yes or no.\n')
            if view_raw_data.lower() != 'yes':
                break
            display_raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('⁩Goodbye⁩')
            break


if __name__ == "__main__":
	main()
