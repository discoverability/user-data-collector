# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class ContentMatchCriteria(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, content_id=None, match=None):  # noqa: E501
        """ContentMatchCriteria - a model defined in OpenAPI

        :param content_id: The content_id of this ContentMatchCriteria.  # noqa: E501
        :type content_id: str
        :param match: The match of this ContentMatchCriteria.  # noqa: E501
        :type match: bool
        """
        self.openapi_types = {
            'content_id': str,
            'match': bool
        }

        self.attribute_map = {
            'content_id': 'content_id',
            'match': 'match'
        }

        self._content_id = content_id
        self._match = match

    @classmethod
    def from_dict(cls, dikt) -> 'ContentMatchCriteria':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ContentMatchCriteria of this ContentMatchCriteria.  # noqa: E501
        :rtype: ContentMatchCriteria
        """
        return util.deserialize_model(dikt, cls)

    @property
    def content_id(self):
        """Gets the content_id of this ContentMatchCriteria.


        :return: The content_id of this ContentMatchCriteria.
        :rtype: str
        """
        return self._content_id

    @content_id.setter
    def content_id(self, content_id):
        """Sets the content_id of this ContentMatchCriteria.


        :param content_id: The content_id of this ContentMatchCriteria.
        :type content_id: str
        """

        self._content_id = content_id

    @property
    def match(self):
        """Gets the match of this ContentMatchCriteria.


        :return: The match of this ContentMatchCriteria.
        :rtype: bool
        """
        return self._match

    @match.setter
    def match(self, match):
        """Sets the match of this ContentMatchCriteria.


        :param match: The match of this ContentMatchCriteria.
        :type match: bool
        """

        self._match = match