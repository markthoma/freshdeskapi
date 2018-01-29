#!/usr/bin/python3.5

import requests
import datetime
import json
import sys
from urllib.parse import urlencode

base_url = input('https://')
#osirium.freshdesk.com
api_key = input('API Key: ')
#jAnlRWX0pkJwphYDWG
password = "xxxx"

def to_json(response):
    try:
        return response.json()
    except Exception as e:
        raise Exception(
            "Tried to json() response body in non-JSON format. {e}".format(e)
        )

def six_months_ago():
    older_than = datetime.datetime.today() - datetime.timedelta(days=180)
    print('Looking for contacts created before {0}'.format(older_than))
    return older_than

def all_tickets(base_url):
    page_number = 1
    contact_list = []
    while True:
        response = requests.get(
            'https://{0}/api/v2/contacts?per_page=100&page={1}'.format(base_url, page_number),
            auth=(api_key, password)
        )
        response_json = to_json(response)
        if len(response_json) > 0:
            contact_list.append(response_json)
            page_number += 1
        else:
            break
    contact_list = sum(contact_list, [])
    return contact_list

def get_old_contacts(contact_list, older_than):
    old_contacts = [
        contact for contact in contact_list if datetime.datetime.strptime(
        contact['created_at'], "%Y-%m-%dT%H:%M:%SZ"
        ) <= older_than
    ]
    return old_contacts

def get_companies():
    companies_data = []
    response = requests.get(
        'https://{0}/api/v2/companies?per_page=100'.format(base_url),
        auth=(api_key, password)
    )
    response_json = to_json(response)
    return [{'name': company['name'], 'id': company['id']} for company in response_json]

def resolve_company_name(companies_data):
    for company in companies_data:
        if contact['company_id'] == company['id']:
            return company['name']

older_than = six_months_ago()
companies_data = get_companies()
contact_list = all_tickets(base_url)
old_contacts = get_old_contacts(contact_list, older_than)
contact_id = 1
for contact in old_contacts:
    print("\nID: ", contact_id)
    print("Name: ", contact['name'])
    company_name = resolve_company_name(companies_data)
    print("Company: ", company_name)
    print("Created At: ", contact['created_at'])
    print("Last Updated: ", contact['updated_at'])
    contact_id = contact_id + 1
