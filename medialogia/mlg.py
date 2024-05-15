from datetime import datetime, timedelta
from typing import Optional, List
from zeep import Client as ZeepClient


class MLGException(Exception):
    def __init__(self, error_message, *args):
        super().__init__(*args)
        self.error_message = error_message

    def __str__(self):
        return self.error_message


class Client(object):
    API_CLIENT = ZeepClient('http://pr.mlg.ru/services/CubusService.svc?singleWsdl')

    def __init__(self, login: str, password: str) -> None:
        """
        :param login: str
        :param password: str
        """
        self.credentials = {'Login': login, 'Password': password}

    def _get_response(self, service: str, *args) -> any:
        response = self.API_CLIENT.service.__getattr__(service)(self.credentials, *args)
        if 'Error' in response and response['Error']:
            raise MLGException(response['Error'])
        return response

    def get_report(self, report_id: str) -> any:
        """
        :param report_id:
        :return: any
        """
        return self._get_response('GetReport', report_id)

    def create_report(self, search_query: str, author_urls: List[str], blog_urls: List[str]) -> any:
        """
        :param search_query: str
        :param author_urls: list (list of strings)
        :param blog_urls: list (list of strings)
        :return: any
        """
        return self._get_response('CreateReport', search_query, author_urls, blog_urls)

    def delete_report(self, report_id: str) -> any:
        """
        :param report_id: str
        :return: any
        """
        return self._get_response('DeleteReport', report_id)

    def get_posts(self, report_id: str, date_from: datetime, date_to: datetime,
                  page_index: Optional[int] = None, page_size: Optional[int] = None) -> any:
        """
        :param report_id: str
        :param date_from: datetime
        :param date_to: datetime
        :param page_index: int or None
        :param page_size: int or None
        :return: any
        """
        params = [report_id, date_from.strftime('%Y-%m-%dT%H:%M:%S'), date_to.strftime('%Y-%m-%dT%H:%M:%S')]
        if page_index:
            params.append(page_index)
        if page_size:
            if not page_index:
                params.append(50)
            params.append(page_size)
        return self._get_response('GetPosts', *params)

    def get_posts_by_objects(self, report_id: str, date_from: datetime, date_to: datetime) -> any:
        """
        :param report_id: str
        :param date_from: datetime (like 2018-11-01T10:06:00)
        :param date_to: datetime (like 2018-11-01T10:06:00)
        :return: any
        """
        return self._get_response('GetPostsStatsByObject', report_id,
                                  date_from.strftime('%Y-%m-%dT%H:%M:%S'),
                                  date_to.strftime('%Y-%m-%dT%H:%M:%S')
                                  )

    def update_report(self, report_id, search_query: str, author_urls: List[str], blog_urls: List[str]) -> any:
        """
        :param report_id: str
        :param search_query: str
        :param author_urls: list (list of strings)
        :param blog_urls: list (list of strings)
        :return: any
        """
        return self._get_response('UpdateReport', report_id, search_query, author_urls, blog_urls)

    def get_posts_with_sort(self, report_id: str, date_from: datetime, date_to: datetime,
                           sort_type: int, page_index: int, page_size: int) -> any:
        """
        :param report_id: str
        :param date_from: datetime (like 2018-11-01T10:06:00)
        :param date_to: datetime (like 2018-11-01T10:06:00)
        :param sort_type: int
        :param page_index: int
        :param page_size: int
        :return: any
        """
        return self._get_response('GetPostsWithSort', report_id, date_from.strftime('%Y-%m-%dT%H:%M:%S'),
                                  date_to.strftime('%Y-%m-%dT%H:%M:%S'), sort_type, page_index, page_size)

    def get_posts_from_timestamp(self, report_id: str, timestamp: datetime, page_index: int, page_size: int) -> any:
        """
        :param report_id: str
        :param timestamp: datetime (like 2018-11-22T10:10:00)
        :param page_index: int
        :param page_size: int
        :return: any
        """
        return self._get_response('GetPostsFromTimestamp', report_id, timestamp.strftime('%Y-%m-%dT%H:%M:%S'),
                                  page_index, page_size)

    def create_report_by_post_urls(self, post_urls: List[str]) -> any:
        """
        :param post_urls: list (list of strings)
        :return: any
        """
        return self._get_response('CreateReportByPostUrls', post_urls)

    def create_report_history(self, report_id: str, date_from: datetime) -> any:
        """
        :param report_id: str
        :param date_from: datetime (like 2018-11-01T10:06:00)
        :return: any
        """
        return self._get_response('CreateReportHistory', report_id, date_from.strftime('%Y-%m-%dT%H:%M:%S'))