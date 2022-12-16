# US BIKESHARE PROJECT Petter Strandberg

# We need below imports:
import time
import pandas as pd
import numpy as np

# Data from source, provided by Udacity, add capital letter to city
CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

# Reference below lists for month and date
months = ['January', 'February', 'March', 'April', 'May', 'June', 'all']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'all']

# Define filters as per the assignment
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # Welcome phrase
    print("--------------------------------------------------------------------------------------------------------\nWelcome! Let me show you some data highlights for bikeshare offerings in different cities. \n")

    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # City = input('Please select which city to view, you can select chicago, new york city, or washington. Please write in text below which city to view: \n \n> ')
    city_ok = False
    while not city_ok: # FUNKAR INTE - HUR FÅR JAG TILL ATT DEN LOOPAR TILLBAKS? OK NU!
        city = input('Please select which city to view, you can select chicago, new york city, or washington. Please write in text below which city to view: \n \n> ')
        if city.title() not in CITY_DATA.keys():
            print('Select a valid city, please try again')
        else:
            print('You selected ', city, ', now select month')
            city = city.title()
            city_ok = True

    # Get user input for month (all, january, february, ... , june), DO THE SAME AS FOR CITY!
    month_ok = False
    while not month_ok:
        month = input('Select month: Write month name January, February, March, April, May, or June, or select all by writing all:\n \n> ')

        if month.title() not in months:
            print('Not a valid month, please select between January, February, March, April, May, or June or all')
        else:
            print('You selected ', month, ', now select weekday')
            month = month.title()
            month_ok = True

    # Get user input for day of week (all, monday, tuesday, ... sunday), DO THE SAME AS FOR CITY!
    day_ok = False
    while not day_ok:
        day = input('Select weekday: Write weekday name Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday, or select all by writing all:\n \n> ')
        if day.title() not in days:
            print('Not a valid weekday, please select between Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday or all')
        else:
            print('You selected ', day)
            day = day.title()
            day_ok = True

    print('\n \nThank you very much for that, you selected:\nCity: ', city, '\nMonth: ', month, '\nWeekday: ', day)

    # To make it nice, print a number of dashes to keep it neat
    print("-"*40)

    # Returns result for city, month and weekday
    return city, month, day

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# FROM assignement, define loading of data, use similar as from PQ3 in previous chapter

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
    # Loads data for the specified city, and use start_time to get datetime functions
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['City'] = city

    # As in PQ3, get month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # As in PQ3, filter by month if applicable
    if month != 'all':
        # Use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # Filter by month to create the new dataframe
        df = df[df['month'] == month]

    # As in PQ3, filter by day of week if applicable
    if day != 'all':
        # Use the index of the months list to get the corresponding int
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = days.index(day) + 1

        # Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Variables used: most common monnt = mcm, most common day of week = mcdow, most common start hour = mcsh

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    mcm = df['month'].mode()[0]
    print('The most common month is: ', mcm)

    # Display the most common day of week
    mcdow = df['day_of_week'].mode()[0]
    print('The most common day is: ', mcdow)

    # Display the most common start hour
    mcsh = df['hour'].mode()[0]
    print('The most common start hour is: ', mcsh)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Variables used: most commonly used start station = mcuss, most commonly used end station = mcues, most frequent combination of start station and end station trip = mfcossaest

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    mcuss = df['Start Station'].mode()[0]
    print('The most commonly used start station is: ', mcuss)

    # Display most commonly used end station
    mcues = df['End Station'].mode()[0]
    print('The most commonly used end station is: ', mcues)

    # Display most frequent combination of start station and end station trip, USE "GROUP BY" AS WE I NEED COMBINATION
    cossaest = df.groupby(['Start Station','End Station'])

    mfcossaest = cossaest.size().sort_values(ascending=False).head(1)
    print('The most frequent combination of start and end station trip is: ', mfcossaest)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Variables used: total travel time = ttt, mean travel time = mtt

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time, ANVÄND "df = df[data].sum()", ALTERNATIVT df = pd.DataFrame(data) OCH SEN print(df.sum())
    ttt = df['Trip Duration'].sum()
    print('Travel time TOTAL is: ', ttt)

    # Display mean travel time, ANVÄND "df = df[data].mean()"
    mtt = df['Trip Duration'].mean()
    print('Travel time MEAN is: ', mtt)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# Variables used: counts of user types = cout

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types, ANVÄND df[data].value_counts()
    city = df['City'].iloc[0]
    print('city is ', city)

    cout = df['User Type'].value_counts()
    print('User type count is: ', cout)

    # Display counts of gender, ANVÄND df[data].value_counts(), GLÖM EJ ATT washington.csv INTE INNEHÅLLER GENDER ELLER FÖDELSEÅR
    # Display earliest, most recent, and most common year of birth, ANVÄND df[data].min/max/mode(), GLÖM EJ ATT washington.csv INTE INNEHÅLLER GENDER ELLER FÖDELSEÅR
    # cog = count of gender, eby = earliest birth year, mrby = most recent birth year, mcby = most common birth year
    if city != 'Washington':
        cog = df['Gender'].value_counts()
        print('Gender count is: ', cog)

        eby = df['Birth Year'].min()
        print('The earliest year of birth is: ', eby)

        mrby = df['Birth Year'].max()
        print('The most recent year of birth is: ', mrby)

        mcby = df['Birth Year'].mode()
        print('The most common year of birth is: ', mcby)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------#

# Display raw data if requested - MÅSTE KONTROLLERA OCH FIXA DENNA - OK NU!
def source_data(df):

    while True:
        source_data = input("Please let me know if you want to see source data for your selection, enter Yes or No please!\n").lower()
        
if source_data == "yes":
            print(df.iloc[row : row + 6])
            row += 6
        elif source_data == "no":
            break
        else:
            print("Please enter Yes or No, maybe you mis-spelled :)"


# FROM ASSIGNMENT def main(), add source_data dataframe and change the while statement accordingly

def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        source_data(df)

        restart = input('\nDo you want to start over and see other statistics? Type Yes or No below!\n')
        if restart.lower() != 'yes':
            print('\nThanks a lot for this session, have a nice day!\n\nヽ(ヅ)ノ\n\n')
            break

if __name__ == "__main__":
    main()

# END
