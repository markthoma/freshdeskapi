#!/usr/bin/python3.5

import requests
import datetime
import json
import sys
import csv
from freshdesk import (
    to_json,
    generate_time_delta,
    get_all_objects,
    api_key
)
from urllib.parse import urlencode

BASE_URL = 'https://osirium.freshdesk.com'
AUTH_TUPLE = (api_key(), 'xxxx')
filename = '/home/mark/Documents/Freshdesk/FreshdeskAPI/unverifiededcontacts.csv'

def all_contacts():
    contact_list = get_all_objects('contacts', BASE_URL, AUTH_TUPLE)
    return contact_list

def get_companies():
    companies_data = []
    companies = get_all_objects('companies', BASE_URL, AUTH_TUPLE)
    return [{'name': company['name'], 'id': company['id']} for company in companies]

def resolve_company_name(companies_data, contact):
    for company in companies_data:
        if contact['company_id'] == company['id']:
            return company['name']

def get_tags(contact_id):
    response = requests.get(
        '{0}/api/v2/contacts/{1}'.format(BASE_URL, contact_id),
        auth=AUTH_TUPLE
    )
    response_json = to_json(response)
    return response_json['tags']

def unapproved_contact(contact_list, companies_data, newer_than):
    with open(filename,'w+', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['Generated on ' + datetime.datetime.now().strftime("%Y-%m-%d")])
        writer.writerow(['Name', 'Email', 'Company', 'Created At', 'Tags'])
        for contact in contact_list:
            if contact['active'] == False and datetime.datetime.strptime(
            contact['created_at'], "%Y-%m-%dT%H:%M:%SZ"
            ) >= newer_than:
                contact_id = contact['id']
                company_name = resolve_company_name(companies_data, contact)
                contact_info = [contact['name'],
                                contact['email'],
                                company_name,
                                contact['created_at'],
                                get_tags(contact_id)
                                ]
                writer.writerow(contact_info)


if __name__ == '__main__':

    companies_data = get_companies()
    contact_list = all_contacts()
    newer_than = generate_time_delta(30)
    unapproved_contact(contact_list, companies_data, newer_than)
