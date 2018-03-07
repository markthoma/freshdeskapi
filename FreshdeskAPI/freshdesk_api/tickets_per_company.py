#!/usr/bin/python3.5

import requests
import datetime
import json
import sys
from urllib.parse import urlencode
from difflib import get_close_matches
from freshdesk import (
    to_json,
    generate_time_delta,
    get,
    get_all_objects,
    api_key
)

BASE_URL = 'https://osirium.freshdesk.com'
AUTH_TUPLE = (api_key(), 'xxxx')

def display_companies():
    return '\n'.join([company['name'] for company in all_companies()])

def all_companies():
    company_list = get_all_objects('companies', BASE_URL, AUTH_TUPLE)
    return company_list

def validate_company_name():
    valid_company = False
    companies_data = all_companies()
    while valid_company == False:
        user_company = input("Company Name: ")
        for company in companies_data:
            if company['name'].lower() == user_company.lower():
                return company['id']
                valid_company = True
            else:
                company_names = []
                for company in companies_data:
                    company_names.append(company['name'])
                if len(get_close_matches(user_company.lower(), company_names)) > 0:
                    try_again = input("Did you mean %a instead? Enter Y if yes, or N if no: " % get_close_matches(user_company.lower(), company_names)[0])
                    if try_again.lower() == 'y':
                        return company['id']
                        valid_company = True
                    else:
                        break
        print("Name {0} not found in companies list.".format(user_company))
        try_again = input("Try again? [no] ")
        if try_again.lower().startswith("y"):
            continue
        else:
            sys.exit()


def all_tickets(company_id):
    extra_filter = '&company_id=' + str(company_id)
    ticket_list = get_all_objects('tickets', BASE_URL, AUTH_TUPLE, extra_filter)
    return ticket_list

def ticket_activity():
    day_check = False
    while day_check == False:
        try:
            days = int(input("For the last x days: "))
        except ValueError:
            print('Not a valid number of days!')
            try_again = input('Try Again? [no]: ')
            if try_again.lower().startswith("y"):
                continue
            else:
                sys.exit()
        if days < 0:
            print('Not a valid number of days!')
            try_again = input('Try Again? [no]: ')
            if try_again.lower().startswith("y"):
                continue
            else:
                sys.exit()
        else:
            day_check = True
    start_date = generate_time_delta(days)
    print("Looking for Tickets created since " + str(start_date))
    return start_date

def filtered_tickets(ticket_list, startDate):
    #  What happens if created_at isn't a key?
    tickets = [
        ticket for ticket in ticket_list if datetime.datetime.strptime(
        ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ"
        ) >= startDate
    ]
    return tickets

def ticket_status_count(status):
    count = len([ticket for ticket in tickets if ticket['status'] == status])
    return str(count)

if __name__ == '__main__':
    print(display_companies())
    company_id = validate_company_name()
    ticket_list = all_tickets(company_id)
    startDate = ticket_activity()
    tickets = filtered_tickets(ticket_list, startDate)
    print('Number of Open Tickets: ' + ticket_status_count(2))
    print('Number of Resolved Tickets: ' + ticket_status_count(4))
    print('Number of Closed Tickets: ' + ticket_status_count(5))
    print('Number of Tickets Waiting for Customer: ' + ticket_status_count(6))
    print('Number of Tickets fixed in Future Release: ' + ticket_status_count(10))
    print('Number of Tickets in Development: ' + ticket_status_count(12))
