import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def clean_data(df):
    df = df.dropna(subset=['Start Time', 'End Time', 'Trip Duration', 'Start Station', 'End Station', 'User Type'])
    df['Trip Duration'] = pd.to_numeric(df['Trip Duration'], errors='coerce')
    df = df.dropna(subset=['Trip Duration'])
    return df

def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    
    city = input("Enter a city (chicago, new york city, washington): ").lower()
    while city not in ('chicago', 'new york city', 'washington'):
        print('Invalid Input!')
        city = input("Please enter a valid city (chicago, new york city, washington): ").lower()
    
    month = input('Which month? January, February, March, April, May, or June? (Type "all" for no filter): ').lower()
    day = input('Which day? Please type your response as an integer (e.g., 1=Sunday, 7=Saturday). (Type "all" for no filter): ').lower()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df = clean_data(df)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['day_of_week'] == day]
    
    if df.empty:
        print(f"No data available for {month} and {day}.")
    
    return df

def show_raw_data(df):
    start_row = 0
    while True:
        show_data = input("\nWould you like to see 5 lines of raw data? (yes/no): ").lower()
        if show_data == 'yes':
            print(df.iloc[start_row:start_row+5])
            start_row += 5
        elif show_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    if not df.empty:
        most_month = df['month'].mode()[0] if not df['month'].mode().empty else 'N/A'
        most_day = df['day_of_week'].mode()[0] if not df['day_of_week'].mode().empty else 'N/A'
        most_hour = df['hour'].mode()[0] if not df['hour'].mode().empty else 'N/A'
    else:
        most_month = most_day = most_hour = 'N/A'
        
    print(f"Most common month: {most_month}")
    print(f"Most common day of the week: {most_day}")
    print(f"Most common start hour: {most_hour}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    if not df.empty:
        most_start_station = df['Start Station'].mode()[0] if not df['Start Station'].mode().empty else 'N/A'
        most_end_station = df['End Station'].mode()[0] if not df['End Station'].mode().empty else 'N/A'
        most_combination = (df['Start Station'] + " to " + df['End Station']).mode()[0] if not (df['Start Station'] + " to " + df['End Station']).mode().empty else 'N/A'
    else:
        most_start_station = most_end_station = most_combination = 'N/A'
        
    print(f"Most common start station: {most_start_station}")
    print(f"Most common end station: {most_end_station}")
    print(f"Most common trip: {most_combination}")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    if not df.empty:
        total_travel_time = df['Trip Duration'].sum()
        mean_travel_time = df['Trip Duration'].mean()
    else:
        total_travel_time = mean_travel_time = 'N/A'
        
    print(f"Total travel time: {total_travel_time} seconds")
    print(f"Average travel time: {mean_travel_time} seconds")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    print('\nCalculating User Stats....\n')
    start_time = time.time()
    
    if not df.empty:
        user_types = df['User Type'].value_counts()
        print(f"User types count:\n{user_types}")
        if 'Gender' in df.columns:
            gender_stats = df['Gender'].value_counts()
            print(f"Gender count:\n{gender_stats}")
        else:
            print("Gender data is not available for this city.")
        if 'Birth Year' in df.columns:
            earliest_birth_year = df['Birth Year'].min()
            most_recent_birth_year = df['Birth Year'].max()
            most_common_birth_year = df['Birth Year'].mode()[0]
            print(f"Earliest year of birth: {earliest_birth_year}")
            print(f"Most recent year of birth: {most_recent_birth_year}")
            print(f"Most common year of birth: {most_common_birth_year}")
        else:
            print("Birth year data is not available for this city.")
    else:
        print("No data available for the specified filters, SORRY!")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        show_raw_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? If so, Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
    main()