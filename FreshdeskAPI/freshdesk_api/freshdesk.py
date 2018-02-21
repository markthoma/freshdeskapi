#!/usr/bin/python3

import requests
import datetime

def check_status(response):
    #  Check all response status codes
    #  with this function.
    #
    #  Raise a FreshdeskAPIException if something
    #  goes wrong.
    pass


def get(url, auth_tuple, params=None):
    print(f"Sending GET request to URL {url} with params {params}...")
    response = requests.get(url, auth=auth_tuple, params=params)
    check_status(response)
    return response


def to_json(response):
    try:
        return response.json()
    except ValueError as e:
        raise Exception(
            "Tried to json() response body in non-JSON format. {e}".format(e)
        )
    except Exception as e:
        raise Exception(
            "Unhandled exception returning response JSON: {e}".format(e)
        )

def generate_time_delta(days):
    time_delta = datetime.datetime.today() - datetime.timedelta(days=days)
    return time_delta

def get_companies(base_url, auth_tuple):
    companies_data = []
    response = requests.get(
        '{0}/api/v2/companies?per_page=100'.format(base_url),
        auth=auth_tuple
    )
    response_json = to_json(response)
    return [
        {
            'name': company['name'],
            'id': company['id']
        } for company in response_json
    ]

def get_all_objects(resource, base_url, AUTH_TUPLE, extra_filter=None):
    object_list = []
    page_number = 1
    if extra_filter == None:
        extra_filter = ''
    while True:
        url = f"{base_url}/api/v2/{resource}?per_page=100&page={page_number}{extra_filter}"
        response = requests.get(url, auth = AUTH_TUPLE)
        response_json = to_json(response)
        if len(response_json) > 0:
            object_list.append(response_json)
            page_number += 1
        else:
            break
    object_list = sum(object_list, [])
    return object_list
