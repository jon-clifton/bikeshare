import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
city, month, day = "", "", ""

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # City Filter
    city = input("Please select a city (Chicago, New York, or Washington:").lower()
    print("City selected:", city.title())
    while city not in ["chicago", "new york", "washington"]:
        print(city.title(), "is not a valid city. Please choose Chicago, New York, or Washington.")
        city = input("Please type a VALID city: Chicago, New York, or Washington").lower()
        print("City selected:", city.title())

    # Month Filter
    print("Now you can filter by month or show all months.")
    month = input("Please select a month or type ALL to see all months combined:").lower()
    print("Month selected:", month.title())
    while month not in ["all", "january", "february", "march", "april", "may", "june"]:
        print(month.title(), "is not a valid option. Please type a valid month or ALL.")
        month = input("Months available are January, February, March, April, May, June or ALL").lower()
        print("Month selected:", month.title())

    # Day Filter
    print("Now you can filter by day or show all days.")
    day = input("Please select a day (Monday, Tuesday...) or type ALL to see all days combined:").lower()
    print("Day selected:", day.title())
    while day not in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        print(day.title(), "is not a valid option. Please type a valid day or ALL.")
        day = input("Days available are Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or ALL").lower()
        print("Day selected:", day.title())

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # datetime conversion
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # append month, day of week, hour and trip
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['start_end'] = df['Start Station'] + ' to ' + df['End Station']

    # Month Filter
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        df = df[df['month'] == month]

    # Day Filter
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Popular Month
    popular_month = df['month'].mode()[0]
    print(popular_month, "was the most popular month.")
        
    # Popular Day
    popular_day = df['day_of_week'].mode()[0]
    print(popular_day, "was the most popular day of the week.")

    # Popular Hour
    popular_hour = df['hour'].mode()[0]
    print("{}:00 was the most popular hour.".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Popular Start
    popular_start = df['Start Station'].mode()[0]
    print(popular_start, "was the most popular start station.")

    # Popular End
    popular_end = df['End Station'].mode()[0]
    print(popular_end, "was the most popular end station.")

    # Popular Trip
    popular_trip = df['start_end'].mode()[0]
    print(popular_trip, "was the most popular trip.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time was", round((sum(df['Trip Duration']/60)/60)/24,1), "days.")

    # display mean travel time
    print("The average travel time was", round(np.mean(df['Trip Duration'])/60,2), "minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    print()
    
    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print(genders)
        print()
    
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliest_dob = df['Birth Year'].min()
        most_recent_dob = df['Birth Year'].max()
        popular_dob = round(df['Birth Year'].mode()[0],0)
    
        print("The oldest user was born on", earliest_dob)
        print("The youngest user was born on", most_recent_dob)
        print("The most common date of birth was", popular_dob)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Asks the user if they would like 5 rows of raw data until they don't.
    """
    start_raw = 0
    end_raw = 5
    
    ask = input("Would you like to see 5 rows of raw data, yes or no?").lower()
        
    while ask not in ["yes","no"]:
        print(ask, "is not a valid input.")
        ask = input("Do you want 5 rows of data, yes or no?").lower()
        
    while ask == "yes":
            print(df.iloc[start_raw : end_raw])
            start_raw += 5
            end_raw += 5
            ask = input("Would you like 5 more rows, yes or no?")

def main():
    """ The main function that calls all other functions. """
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()