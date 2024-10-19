import sys

import numpy as np
import pandas as pd


def parse_nyt_data(file_path=''):
    """
    Parse the NYT covid database and return a list of tuples. Each tuple describes one entry in the source data set.
    Date: the day on which the record was taken in YYYY-MM-DD format
    County: the county name within the State
    State: the US state for the entry
    Cases: the cumulative number of COVID-19 cases reported in that locality
    Deaths: the cumulative number of COVID-19 death in the locality

    :param file_path: Path to data file
    :return: A List of tuples containing (date, county, state, cases, deaths) information
    """
    # data point list
    data=[]

    # open the NYT file path
    try:
        fin = open(file_path)
    except FileNotFoundError:
        print('File ', file_path, ' not found. Exiting!')
        sys.exit(-1)

    # get rid of the headers
    fin.readline()

    # while not done parsing file
    done = False

    # loop and read file
    while not done:
        line = fin.readline()

        if line == '':
            done = True
            continue

        # format is date,county,state,fips,cases,deaths
        (date, county, state, fips, cases, deaths) = line.rstrip().split(",")

        # clean up the data to remove empty entries
        if cases=='':
            cases=0
        if deaths=='':
            deaths=0

        # convert elements into ints
        try:
            entry = (date,county,state, int(cases), int(deaths))
        except ValueError:
            print('Invalid parse of ', entry)

        # place entries as tuple into list
        data.append(entry)


    return data

def first_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    :return:
    """
    RC_first_case_date = None
    HB_first_case_date = None

    # find the earliest instance in rockingham where there is a covid case, and save the date of it
    for (date, county, state, cases, deaths) in data:
        if county == "Rockingham" and state == "Virginia":
            if cases > 0:
                RC_first_case_date = date
                break

    # do the same thing for hburg
    for (date, county, state, cases, deaths) in data:
        if county == "Harrisonburg city" and state == "Virginia":
            if cases > 0:
                HB_first_case_date = date
                break

    print("The first covid case in Rockingham County occurred on:", RC_first_case_date)
    print("The first covid case in Harrisonburg City occurred on:", HB_first_case_date)
    print()

    return RC_first_case_date, HB_first_case_date

def second_question(data):
    """
    # Write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    :return:
    """
    RC_max_case_date = None
    HB_max_case_date = None

    # find the max daily change in cases, and save the date of it
    last_cases = 0
    max_change = 0
    for (date, county, state, cases, deaths) in data:
        if county == "Rockingham" and state == "Virginia":
            change = cases - last_cases  # don't have to worry about negative change since cases are cumulative
            # if this change is greater than the previous max change, make it the new max
            if change > max_change:
                RC_max_case_date = date
                max_change = change
            last_cases = cases

    print(f"The maximum daily increase in cases in Rockingham County occurred on: "
          f"{RC_max_case_date}, with {max_change} cases.")

    # do the same thing for hburg
    last_cases = 0
    max_change = 0
    for (date, county, state, cases, deaths) in data:
        if county == "Harrisonburg city" and state == "Virginia":
            change = cases - last_cases
            # if this change is greater than the previous max change, make it the new max
            if change > max_change:
                HB_max_case_date = date
                max_change = change
            last_cases = cases

    print(f"The maximum daily increase in cases in Harrisonburg City occurred on: "
          f"{HB_max_case_date}, with {max_change} cases.")
    print()

    return RC_max_case_date, HB_max_case_date

def third_question(data):
    """
    # Write code to address the following question:Use print() to display your responses.
    # What was the worst 7-day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.
    :return:
    """
    # initialize some variables
    RC_max_7day = None
    RC_max_change = 0
    HB_max_7day = None
    HB_max_change = 0

    last_cases = 0
    day2 = 0
    day3 = 0
    day4 = 0
    day5 = 0
    day6 = 0
    day7 = 0

    # create a running 7day period, find the total new cases in the period, and do a running max finder for each period
    for (date, county, state, cases, deaths) in data:
        if county == "Rockingham" and state == "Virginia":
            change = cases - last_cases # find the new daily cases
            last_cases = cases # update the last number of cases

            # update each day in our 7day period, to the next date
            day1 = day2
            day2 = day3
            day3 = day4
            day4 = day5
            day5 = day6
            day6 = day7
            day7 = change

            # add up all the new cases over this particular 7day period, and do a running maximum finder
            change_7day = day7 + day6 + day5 + day4 + day3 + day2 + day1
            if change_7day > RC_max_change:
                RC_max_7day = date
                RC_max_change = change_7day

    # do the same thing for hburg
    for (date, county, state, cases, deaths) in data:
        # add up the total new cases in the first 7 days
        if county == "Harrisonburg city" and state == "Virginia":
            change = cases - last_cases # find the new daily cases
            last_cases = cases # update the last number of cases

            # update each day in our 7day period, to the next date
            day1 = day2
            day2 = day3
            day3 = day4
            day4 = day5
            day5 = day6
            day6 = day7
            day7 = change

            # add up all the new cases over this particular 7day period, and do a running maximum finder
            change_7day = day7 + day6 + day5 + day4 + day3 + day2 + day1
            if change_7day > HB_max_change:
                HB_max_7day = date
                HB_max_change = change_7day

    print(f"The worst 7-day period in Rockingham County was the 7-day period ENDING on:"
          f" {RC_max_7day}, with {RC_max_change} new cases.")
    print(f"The worst 7-day period in Harrisonburg City was the 7-day period ENDING on:"
          f" {HB_max_7day}, with {HB_max_change} new cases.")

    return

if __name__ == "__main__":
    data = parse_nyt_data('us-counties.csv')

    #for (date, county, state, cases, deaths) in data:
    #    print('On ', date, ' in ', county, ' ', state, ' there were ', cases, ' cases and ', deaths, ' deaths')


    # write code to address the following question: Use print() to display your responses.
    # When was the first positive COVID case in Rockingham County?
    # When was the first positive COVID case in Harrisonburg?
    first_question(data)


    # write code to address the following question: Use print() to display your responses.
    # What day was the greatest number of new daily cases recorded in Harrisonburg?
    # What day was the greatest number of new daily cases recorded in Rockingham County?
    second_question(data)

    # write code to address the following question:Use print() to display your responses.
    # What was the worst seven day period in either the city and county for new COVID cases?
    # This is the 7-day period where the number of new cases was maximal.
    third_question(data)
