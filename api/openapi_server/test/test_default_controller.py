# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.check_criteria_request import CheckCriteriaRequest  # noqa: E501
from openapi_server.models.content_match_criteria import ContentMatchCriteria  # noqa: E501
from openapi_server.models.thumbnail import Thumbnail  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_check_criteria_post(self):
        """Test case for check_criteria_post

        
        """
        check_criteria_request = {
  "items" : [ "content_id1", "content_id2" ],
  "query" : {
    "name" : "TRUE",
    "operand" : {
      "subject" : "content_type",
      "predicate" : "=",
      "object" : "FILM"
    }
  }
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/discoverability/dataviz-api/0.1.0/check_criteria',
            method='POST',
            headers=headers,
            data=json.dumps(check_criteria_request),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_thumbnails_user_id_session_id_get(self):
        """Test case for thumbnails_user_id_session_id_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/discoverability/dataviz-api/0.1.0/thumbnails/{user_id}/{session_id}'.format(user_id='user_id_example', session_id='session_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_users_get(self):
        """Test case for users_get

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/discoverability/dataviz-api/0.1.0/users',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
