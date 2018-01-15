#!/usr/bin/python3.5

import requests
import datetime
import json
import sys
from urllib.parse import urlencode

def get_companies():
    companies_data = []
    response = requests.get(
        'https://{0}/api/v2/companies?per_page=100'.format(base_url),
        auth=(api_key, password)
    )
    response_json = to_json(response)
    return [{'name': company['name'], 'id': company['id']} for company in response_json]

def to_json(response):
    try:
        return response.json()
    except Exception as e:
        raise Exception(
            "Tried to json() response body in non-JSON format. {e}".format(e)
        )

def display_companies(get_companies):
    return '\n'.join([company['name'] for company in get_companies()])

def validate_company_name(get_companies):
    valid_company = False
    companies_data = get_companies()
    while valid_company == False:
        user_company = input("Company Name: ")
        for company in companies_data:
            if company['name'].lower() == user_company.lower():
                return company['id']
                valid_company = True
        print("Name {0} not found in companies list.".format(user_company))
        try_again = input("Try again? [no] ")
        if try_again == 'Y' or 'y':
            continue
        else:
            sys.exit()

def all_tickets(base_url, company_id):
    page_number = 1
    ticket_list = []
    while True:
        response = requests.get(
            'https://{0}/api/v2/tickets?per_page=100&page={1}&company_id={2}'.format(base_url, page_number, company_id),
            auth=(api_key, password)
        )
        response_json = to_json(response)
        if len(response_json) > 0:
            ticket_list.append(response_json)
            page_number += 1
        else:
            break
    ticket_list = sum(ticket_list, [])
    return ticket_list

def ticket_activity():
    dayCheck = False
    while dayCheck == False:
        try:
            days = int(input("For the last x days: "))
        except ValueError:
            print('Not a valid number of days!')
            tryAgain = input('Try Again? [no]: ')
            if tryAgain == 'Y' or 'y':
                continue
            else:
                sys.exit()
        if days < 0:
            print('Not a valid number of days!')
            tryAgain = input('Try Again? [no]: ')
            if tryAgain == 'Y' or 'y':
                continue
            else:
                sys.exit()
        else:
            dayCheck = True
    startDate = datetime.datetime.today() - datetime.timedelta(days=days)
    print('Looking for ticket activity since ' + str(startDate))
    return startDate

def filtered_tickets(ticket_list, startDate):
    tickets = [
        ticket for ticket in ticket_list if datetime.datetime.strptime(
        ticket['created_at'], "%Y-%m-%dT%H:%M:%SZ"
        ) >= startDate
    ]
    return tickets

def ticket_status(tickets):
    open_tickets = len([ticket for ticket in tickets if ticket['status'] == 2])
    pending_tickets = len([ticket for ticket in tickets if ticket['status'] == 3])
    resolved_tickets = len([ticket for ticket in tickets if ticket['status'] == 4])
    closed_tickets = len([ticket for ticket in tickets if ticket['status'] == 5])
    waiting_tickets = len([ticket for ticket in tickets if ticket['status'] == 6])
    future_release_fix = len([ticket for ticket in tickets if ticket['status'] == 10])
    development_tickets = len([ticket for ticket in tickets if ticket['status'] == 12])
    print('Number of Open Tickets: ' + str(open_tickets))
    print('Number of Resolved Tickets: ' + str(resolved_tickets))
    print('Number of Closed Tickets: ' + str(closed_tickets))
    print('Number of Tickets Waiting for Customer: ' + str(waiting_tickets))
    print('Number of Tickets fixed in Future Release: ' + str(future_release_fix_tickets))
    print('Number of Tickets in Development: ' + str(development_tickets))


base_url = input('https://')
#osirium.freshdesk.com
api_key = input('API Key: ')
#jAnlRWX0pkJwphYDWG
password = "xxxx"

print(display_companies(get_companies))
company_id = validate_company_name(get_companies)
ticket_list = all_tickets(base_url, company_id)
startDate = ticket_activity()
tickets = filtered_tickets(ticket_list, startDate)
ticket_status(tickets)
