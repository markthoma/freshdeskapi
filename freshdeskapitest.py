#!/usr/bin/python3.5

import requests
import datetime
import json
from urllib.parse import urlencode

def get_companies():
    companies_data = []
    response = requests.get(
        '{0}/api/v2/companies?per_page=100'.format(base_url),
        auth=(api_key, password)
    )
    response_json = to_json(response)
    return [{'name': company['name'], 'id': company['id']} for company in response_json]

def validate_company_name(company_name):
    companies_data = get_companies()
    for company in companies_data:
        if company['name'].lower() == company_name.lower():
            return company['id']
    raise Exception("Name {0} not found in companies list.".format(company_name))

def display_companies(get_companies):
    return '\n'.join([company['name'] for company in get_companies()])

def to_json(response):
    try:
        return response.json()
    except Exception as e:
        raise Exception(
            "Tried to json() response body in non-JSON format. {e}".format(e)
        )

def all_tickets(base_url, company_id):
    page_number = 1
    ticket_list = []
    while True:
        response = requests.get(
            '{0}/api/v2/tickets?per_page=100&page={1}&company_id={2}'.format(base_url, page_number, company_id),
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
                quit()
        if days < 0:
            print('Not a valid number of days!')
            tryAgain = input('Try Again? [no]: ')
            if tryAgain == 'Y' or 'y':
                continue
            else:
                quit()
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
    print('Number of Resolved Tickets: ' + str(resolved_tickets))
    print('Number of Closed Tickets: ' + str(closed_tickets))
    print('Number of Open Tickets: ' + str(open_tickets))

base_url = input('https://')
api_key = input('API Key: ')
password = "xxxx"

print(display_companies(get_companies))
user_company = input("Company Name: ")
company_id = validate_company_name(user_company)
ticket_list = all_tickets(base_url, company_id)
startDate = ticket_activity()
tickets = filtered_tickets(ticket_list, startDate)
ticket_status(tickets)


#for ticket in filtered_tickets:
    #print('')
    #print('Ticket #' + str(ticket['id']))
    #print('Created on ', (ticket['created_at']))
    #if ticket['status'] == 2:
        #print('Status Open')
        #openTicket = openTicket + 1
    #if ticket['status'] == 3:
        #print('Status Pending')
    #if ticket['status'] == 4:
        #print('Status Resolved')
        #resolved = resolved + 1
    #if ticket['status'] == 5:
        #print('Status Closed')
        #closed = closed + 1
    #if ticket['status'] == 6:
        #print('Status Waiting On Customer')
    #if ticket['status'] == 10:
        #print('Status Fixed In Future Release')
    #if ticket['status'] == 12:
        #print('Status In Development')
    #print('Subject: ' + str(ticket['subject']))
