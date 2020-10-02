import json
import math
import os
import logging
import requests
from requests.auth import HTTPBasicAuth


class DaisyconApi(object):
    def __init__(self, username, password, publisher_id):
        self._base_url = "https://services.daisycon.com"

        if not isinstance(username, str) or len(username) < 5:
            raise ValueError('Missing username')

        if not isinstance(password, str) or len(password) < 8:
            raise ValueError('Missing password')

        if not isinstance(publisher_id, str) or len('%s' % publisher_id) < 6:
            raise ValueError('Missing or Invalid publisher_id')

        self._user = username
        self._pw = password
        self._publisher_id = '%s' % publisher_id

    @property
    def publisher_id(self):
        return self._publisher_id

    def get_publisher_programs(self, page=1, per_page=1000, order_by="start_date", order_direction="desc"):
        """
        curl -X GET "https://services.daisycon.com/publishers/%publisher_id%/programs?order_direction=asc&page=1&per_page=10"
        -H "accept: application/json"
        -H "Authorization:
        """

        return self._api_GET_request("/publishers/%s/programs" % self.publisher_id, params={
            "page": page,
            "per_page": per_page,
            "order_by": order_by,
            "order_direction": order_direction
        })

    def get_productfeeds_v2(self, page=1, per_page=1000):
        """
        curl -X GET "https://services.daisycon.com/publishers/%publisher_id%/productfeeds.v2/program?page=1&per_page=100"
        -H "accept: application/json"
        -H "Authorization:
        """
        return self._api_GET_request("/publishers/%s/productfeeds.v2" % self.publisher_id, {
            "page": page,
            "per_page": per_page,
        })

    def _api_GET_request(self, url_suffix, params):
        target_url = "%s%s" % (self._base_url, url_suffix)
        response = requests.get(target_url, auth=HTTPBasicAuth(self._user, self._pw), params=params)
        data = response.json()
        total_count = dict(response.headers).get('X-Total-Count')
        if total_count:
            total_count = int(total_count)
        return data, total_count

    def read_json(self, identifier):
        file_path = '%s.json' % identifier
        if not os.path.exists(file_path):
            return None

        with open(file_path, 'r') as fp:
            return json.load(fp)

    def save_json(self, identifier, data):
        file_path = '%s.json' % identifier
        with open(file_path, 'w') as fp:
            json.dump(data, fp, indent=2)

    def load_from_cache(self, identifier, enabled=True):
        if enabled:
            return self.read_json(identifier)

        return None

    @classmethod
    def fetch_all_pages(cls, api_method):
        data_page_1, total_counts = api_method(page=1, per_page=1)

        pages = math.ceil(total_counts / 100)

        results = ()
        for i in range(0, pages):
            logging.info('Fetching page %s/%s' % (i + 1, pages))
            data_page, total_counts = api_method(page=i, per_page=100)
            results += tuple(data_page)
        return results
