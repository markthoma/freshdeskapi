#!/usr/bin/python3.5

import requests
import datetime
import json
import sys
import csv
from freshdesk import (
    to_json,
    generate_time_delta,
    get,
    get_all_objects,
    api_key
)
from urllib.parse import urlencode

BASE_URL = 'https://osirium.freshdesk.com'
AUTH_TUPLE = (api_key(), 'xxxx')
filename = '/home/mark/Documents/Freshdesk/FreshdeskAPI/oldcontacts.csv'

def all_contacts():
    contact_list = get_all_objects('contacts', BASE_URL, AUTH_TUPLE)
    return contact_list

def get_old_objects(object_list, time_delta):
    old_objects = [
        object_dict for object_dict in object_list if datetime.datetime.strptime(
            object_dict['created_at'], "%Y-%m-%dT%H:%M:%SZ"
        ) <= time_delta and 'created_at' in object_dict
    ]
    return old_objects

def get_contact_company_name(company_list, contact):
    for company in company_list:
        if contact['company_id'] == company['id']:
            return company['name']
    return None

def all_companies():
    company_list = get_all_objects('companies', BASE_URL, AUTH_TUPLE)
    return company_list

def create_csv(old_contacts, company_list, time_delta):
    with open(filename,'w+', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(['Contacts older than ' + str(time_delta.strftime("%Y-%m-%d")) + ' as of ' + datetime.datetime.now().strftime("%Y-%m-%d")])
        writer.writerow(['Name', 'eMail', 'Company', 'Created At', 'Last Updated'])
        for contact in old_contacts:
                company_name = get_contact_company_name(company_list, contact)
                contact_info = [contact['name'],
                                contact['email'],
                                company_name,
                                contact['created_at'],
                                contact['updated_at']
                                ]
                writer.writerow(contact_info)


if __name__ == '__main__':

    time_delta = generate_time_delta(180)
    print('getting companies...')
    company_list = all_companies()
    print('getting contacts...')
    contact_list = all_contacts()
    print('getting old contacts...')
    old_contacts = get_old_objects(contact_list, time_delta)
    create_csv(old_contacts, company_list, time_delta)
