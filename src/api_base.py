from json import JSONDecodeError
# from ratelimit import limits
import requests

import logging
logger = logging.getLogger(__name__)


class ApiBase:
    def __init__(self, url):
        """

        :param url:
        """
        self.url = url

    def get_api_response(self, method, protocol, uri, params="", headers={}, proxies={}) -> object:
        """

        :param method:
        :param protocol:
        :param uri:
        :param params:
        :param headers:
        :param proxies:
        :return:
        """
        request_url = protocol + "://" + self.url + uri
        if method == "get":
            return self.call_get_api(request_url, params, headers, proxies)
        elif method == 'post':
            pass
        elif method == 'put':
            pass

    # @limits(calls=15, period=TIME_PERIOD)
    def call_get_api(self, request_url, params, headers, proxies) -> object:
        """

        :param request_url:
        :param params:
        :param headers:
        :param proxies:
        :return:
        """
        print("API: {} params: {}, headers: {} , proxies: {}".format(
            request_url, params, headers, proxies
        ))
        if headers and proxies:
            response = requests.get(request_url, params, headers, proxies)
        elif headers:
            response = requests.get(request_url, params, headers)
        elif proxies:
            response = requests.get(request_url, params, proxies)
        else:
            response = requests.get(request_url, params)
        print("response {}".format(self.parse_response(response)))
        return response

    def parse_response(self, response):
        try:
            print("response {}".format(response.json()))
            return response.json()
        except JSONDecodeError as e:
            print("response {}".format(response.text))
            return response.text
