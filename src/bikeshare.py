import time
import datetime
import pandas as pd

CITY_DATA = {"chicago": "chicago.csv",
             "new york city": "new_york_city.csv",
             "washington": "washington.csv"}

DEFAULT_SELECT = "all"


def get_months_list(month_num=False):
    """Returns months"""
    month_names = ["january", "february", "march", "april", "may", "june"]
    if(month_num):
        return month_names[month_num - 1].title()

    return month_names


def get_month():
    """ Displays months prompt and handles selection """
    month = None
    months = get_months_list()

    print("\nPlease select month or type \"" + DEFAULT_SELECT + "\"")
    for idx, m in enumerate(months):
        print("\t" + str(idx + 1) + ". " + m.title())

    while not month:
        user_input = input("Select: 1-" + str(len(months)) + ": ")
        if user_input.lower() == DEFAULT_SELECT:
            month = DEFAULT_SELECT
            break

        try:
            if int(user_input) > len(months) or int(user_input) < 1:
                raise Exception("Invalid month")
            else:
                month = months[int(user_input) - 1]
        except Exception as err:
            print("\nPlease select valid month between 1-" + str(len(months)))

    return month


def get_day():
    """ Displays days prompt and handles selection """
    selected_day = None
    days = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            ]
    print("\nPlease select day of the week or type \"" + DEFAULT_SELECT + "\"")
    for idx, day in enumerate(days):
        print("\t" + str(idx + 1) + ". " + day.title())

    while not selected_day:
        user_selection = input("Select (1-7): ")
        if user_selection.lower() == DEFAULT_SELECT:
            selected_day = DEFAULT_SELECT
            break

        try:
            if int(user_selection) <= 7 and int(user_selection) >= 0:
                selected_day = days[int(user_selection) - 1]
            else:
                raise Exception("Invalid day of the week")
        except Exception as err:
            print("\nPlease select valid day of the week between 1 - 7")

    return selected_day


def get_city():
    """ Displays cities prompt and handles selection """
    print("""
Please select city name to analyze:
        1. Chicago
        2. New york city
        3. Washington
                """)

    city = None
    while not city:
        city_idx = input("Select 1-" + str(len(CITY_DATA)) + ": ")
        cities_name_list = list(CITY_DATA.keys())
        try:
            if int(city_idx) <= len(cities_name_list) and int(city_idx) >= 0:
                city = cities_name_list[int(city_idx) - 1]
            else:
                raise Exception("Invalid city")
        except Exception as err:
            print("\nPlease select valid city name between 1-" + str(len(cities_name_list)))

    return city


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let\'s explore some US bikeshare data!")

    city = get_city()
    month = get_month()
    day = get_day()

    print("-"*40)
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
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.weekday_name

    if month != DEFAULT_SELECT:
        months = get_months_list()
        month = months.index(month) + 1
        df = df[df["month"] == month]

    if day != DEFAULT_SELECT:
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    most_popular_month = df.month.mode()[0]
    print("Most common month: " + get_months_list(int(most_popular_month)))

    most_popular_weekday = df.day_of_week.mode()[0]
    print("Most common day of week: " + most_popular_weekday)

    hours = df["Start Time"].dt.hour
    most_popular_hour = hours.mode()[0]
    print("Most common start hour: " + str(most_popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    most_common_station = df["Start Station"].mode()[0]
    print("Most popular start station: " + most_common_station)

    # display most commonly used end station
    most_common_end_station = df["End Station"].mode()[0]
    print("Most popular end station: " + most_common_end_station)

    # display most frequent combination of start station and end station trip
    trips = "[ " + df["Start Station"] + " ] -->> [ " + df["End Station"] + " ]"
    most_common_trip = trips.mode()[0]
    print("Most popular Trip: " + most_common_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def sec_to_time(sec):
    return str(datetime.timedelta(seconds=float(sec)))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    total_duration = df["Trip Duration"].sum()
    print("Total travel time: " + sec_to_time(total_duration))

    trip_mean = df["Trip Duration"].mean()
    print("Mean travel time: " + sec_to_time(trip_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...")
    start_time = time.time()

    # Display counts of user types
    if "User Type" in df:
        print("\nUsers by Type:")
        print("======================")
        genders = df.groupby("User Type")
        print(genders.size().reset_index(name='Count'))
        print("======================\n")

    # Display counts of gender
    if "Gender" in df:
        print("Users by Gender:")
        print("==================")
        genders = df.groupby("Gender")
        print(genders.size().reset_index(name='Count'))
        print("==================\n")

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        print("Years of birth")
        print("==================")

        oldest = df["Birth Year"].min()
        youngest = df["Birth Year"].max()
        common = df["Birth Year"].mode()[0]
        print("     Oldest: " + str(int(oldest)))
        print("   Youngest: " + str(int(youngest)))
        print("Most common: " + str(int(common)))

        print("==================\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-"*40)


def display_raw_data(df):
    """ Show raw data to user """
    current_idx = 0
    show_next = input("Would you like to see raw data? y/n: ")

    while True:
        if show_next.lower() == "y":
            if current_idx >= len(df):
                print("That's it!")
                break

            df_now = df[current_idx: current_idx + 5]
            current_idx += 5
            print(df_now)

            show_next = input("\nShow next 5 rows? y/n: ")
        else:
            break


def main():
    while True:
        city, month, day = get_filters()

        while True:
            print("\nYour selection:")
            print("==================")
            print("City: " + city.title())

            if month != DEFAULT_SELECT:
                month_num = get_months_list().index(month) + 1
                print("Month: " + datetime.date(1900, month_num, 1).strftime("%B").title())
            else:
                print("Month: " + DEFAULT_SELECT.title())

            if day != DEFAULT_SELECT:
                print("Day of the week: " + day.title())
            else:
                print("Day of the week: " + DEFAULT_SELECT.title())

            print("==================")
            edit_selection = input("\nWould You like to edit your selection? y/n: ")
            if edit_selection.lower() == "y":
                city, month, day = get_filters()
            else:
                break

        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()

