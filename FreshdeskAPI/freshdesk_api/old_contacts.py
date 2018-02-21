#!/usr/bin/python3.5

import requests
import datetime
import json
import sys
from freshdesk import (
    to_json,
    generate_time_delta,
    get,
    get_companies,
    get_all_objects
)
from urllib.parse import urlencode

BASE_URL = 'https://osirium.freshdesk.com'
AUTH_TUPLE = (input('API Key: '), 'xxxx')

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

if __name__ == '__main__':

    time_delta = generate_time_delta(180)
    company_list = get_companies(BASE_URL, AUTH_TUPLE)
    contact_list = all_contacts()
    old_contacts = get_old_objects(contact_list, time_delta)
    contact_id = 1
    for contact in old_contacts:
        print("\nID: ", contact_id)
        print("Name: ", contact['name'])
        company_name = get_contact_company_name(company_list, contact)
        print("Company: ", company_name)
        print("Created At: ", contact['created_at'])
        print("Last Updated: ", contact['updated_at'])
        contact_id = contact_id + 1
