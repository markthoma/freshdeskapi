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

def all_contacts():
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

def get_companies():
    companies_data = []
    response = requests.get(
        'https://{0}/api/v2/companies?per_page=100'.format(base_url),
        auth=(api_key, password)
    )
    response_json = to_json(response)
    return [{'name': company['name'], 'id': company['id']} for company in response_json]

def resolve_company_name(companies_data, contact):
    for company in companies_data:
        if contact['company_id'] == company['id']:
            return company['name']

def one_month_ago():
    newer_than = datetime.datetime.today() - datetime.timedelta(days=30)
    return newer_than

def get_tags(contact_tag_id):
    response = requests.get(
        'https://{0}/api/v2/contacts/{1}'.format(base_url, contact_tag_id),
        auth=(api_key, password)
    )
    response_json = to_json(response)
    return response_json['tags']

def unapproved(contact_list, companies_data, newer_than):
    contact_id = 1
    for contact in contact_list:
        if contact['active'] == False and datetime.datetime.strptime(
        contact['created_at'], "%Y-%m-%dT%H:%M:%SZ"
        ) >= newer_than:
            contact_tag_id = contact['id']
            print("\n", contact_id, ":")
            print("Name: ", contact['name'])
            print("Email: ", contact['email'])
            company_name = resolve_company_name(companies_data, contact)
            print("Company: ", company_name)
            print("Created At: ", contact['created_at'])
            print("Tags: ", get_tags(contact_tag_id))
            contact_id = contact_id + 1

companies_data = get_companies()
contact_list = all_contacts()
newer_than = one_month_ago()
unapproved(contact_list, companies_data, newer_than)
