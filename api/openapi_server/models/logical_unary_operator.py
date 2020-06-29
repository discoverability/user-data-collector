# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.logical_unary_operator_all_of import LogicalUnaryOperatorAllOf
from openapi_server import util

from openapi_server.models.logical_unary_operator_all_of import LogicalUnaryOperatorAllOf  # noqa: E501

class LogicalUnaryOperator(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, name=None, operand=None):  # noqa: E501
        """LogicalUnaryOperator - a model defined in OpenAPI

        :param name: The name of this LogicalUnaryOperator.  # noqa: E501
        :type name: str
        :param operand: The operand of this LogicalUnaryOperator.  # noqa: E501
        :type operand: object
        """
        self.openapi_types = {
            'name': str,
            'operand': object
        }

        self.attribute_map = {
            'name': 'name',
            'operand': 'operand'
        }

        self._name = name
        self._operand = operand

    @classmethod
    def from_dict(cls, dikt) -> 'LogicalUnaryOperator':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The LogicalUnaryOperator of this LogicalUnaryOperator.  # noqa: E501
        :rtype: LogicalUnaryOperator
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self):
        """Gets the name of this LogicalUnaryOperator.


        :return: The name of this LogicalUnaryOperator.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this LogicalUnaryOperator.


        :param name: The name of this LogicalUnaryOperator.
        :type name: str
        """
        allowed_values = ["TRUE", "FALSE"]  # noqa: E501
        if name not in allowed_values:
            raise ValueError(
                "Invalid value for `name` ({0}), must be one of {1}"
                .format(name, allowed_values)
            )

        self._name = name

    @property
    def operand(self):
        """Gets the operand of this LogicalUnaryOperator.


        :return: The operand of this LogicalUnaryOperator.
        :rtype: object
        """
        return self._operand

    @operand.setter
    def operand(self, operand):
        """Sets the operand of this LogicalUnaryOperator.


        :param operand: The operand of this LogicalUnaryOperator.
        :type operand: object
        """

        self._operand = operand
