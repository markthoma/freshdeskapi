#!/usr/bin/python3.5

import requests
import datetime
import json
import sys
import csv
from urllib.parse import urlencode
from freshdesk import (
    to_json,
    generate_time_delta,
    get,
    get_companies,
    get_all_objects
)

BASE_URL = 'https://osirium.freshdesk.com'
AUTH_TUPLE = (input('API Key: '), 'xxxx')

def all_contacts():
    contact_list = get_all_objects('contacts', BASE_URL, AUTH_TUPLE)
    return contact_list

def resolve_company_name(companies_data, contact):
    for company in companies_data:
        if contact['company_id'] == company['id']:
            return company['name']

def get_tags(contact_tag_id):
    response = requests.get(
        '{0}/api/v2/contacts/{1}'.format(BASE_URL, contact_tag_id),
        auth=AUTH_TUPLE
    )
    response_json = to_json(response)
    return response_json['tags']

def create_csv(contact_list, companies_data, newer_than):
    with open('/home/mark/Documents/Freshdesk/FreshdeskAPI/unverifiededcontacts.csv', 'w') as f:
        fieldnames = ['Name', 'eMail', 'Company', 'Created at', 'Tags']
        writer = csv.writer(f, delimiter=',')
        writer.writerow(fieldnames)
        for contact in contact_list:
            if contact['active'] == False and datetime.datetime.strptime(
            contact['created_at'], "%Y-%m-%dT%H:%M:%SZ"
            ) >= newer_than:
                contact_tag_id = contact['id']
                name = contact['name']
                email = contact['email']
                company_name = resolve_company_name(companies_data, contact)
                company = str(company_name)
                created_at = contact['created_at']
                tags = str(get_tags(contact_tag_id))
                data = [name , email , company , created_at , tags]
                writer.writerow(data)

if __name__ == '__main__':
    companies_data = get_companies(BASE_URL, AUTH_TUPLE)
    contact_list = all_contacts()
    newer_than = generate_time_delta(30)
    create_csv(contact_list, companies_data, newer_than)
