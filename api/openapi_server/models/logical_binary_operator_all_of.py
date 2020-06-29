# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class LogicalBinaryOperatorAllOf(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, name=None, operand1=None, operand2=None):  # noqa: E501
        """LogicalBinaryOperatorAllOf - a model defined in OpenAPI

        :param name: The name of this LogicalBinaryOperatorAllOf.  # noqa: E501
        :type name: str
        :param operand1: The operand1 of this LogicalBinaryOperatorAllOf.  # noqa: E501
        :type operand1: object
        :param operand2: The operand2 of this LogicalBinaryOperatorAllOf.  # noqa: E501
        :type operand2: object
        """
        self.openapi_types = {
            'name': str,
            'operand1': object,
            'operand2': object
        }

        self.attribute_map = {
            'name': 'name',
            'operand1': 'operand1',
            'operand2': 'operand2'
        }

        self._name = name
        self._operand1 = operand1
        self._operand2 = operand2

    @classmethod
    def from_dict(cls, dikt) -> 'LogicalBinaryOperatorAllOf':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The LogicalBinaryOperator_allOf of this LogicalBinaryOperatorAllOf.  # noqa: E501
        :rtype: LogicalBinaryOperatorAllOf
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self):
        """Gets the name of this LogicalBinaryOperatorAllOf.


        :return: The name of this LogicalBinaryOperatorAllOf.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this LogicalBinaryOperatorAllOf.


        :param name: The name of this LogicalBinaryOperatorAllOf.
        :type name: str
        """
        allowed_values = ["AND", "OR"]  # noqa: E501
        if name not in allowed_values:
            raise ValueError(
                "Invalid value for `name` ({0}), must be one of {1}"
                .format(name, allowed_values)
            )

        self._name = name

    @property
    def operand1(self):
        """Gets the operand1 of this LogicalBinaryOperatorAllOf.


        :return: The operand1 of this LogicalBinaryOperatorAllOf.
        :rtype: object
        """
        return self._operand1

    @operand1.setter
    def operand1(self, operand1):
        """Sets the operand1 of this LogicalBinaryOperatorAllOf.


        :param operand1: The operand1 of this LogicalBinaryOperatorAllOf.
        :type operand1: object
        """

        self._operand1 = operand1

    @property
    def operand2(self):
        """Gets the operand2 of this LogicalBinaryOperatorAllOf.


        :return: The operand2 of this LogicalBinaryOperatorAllOf.
        :rtype: object
        """
        return self._operand2

    @operand2.setter
    def operand2(self, operand2):
        """Sets the operand2 of this LogicalBinaryOperatorAllOf.


        :param operand2: The operand2 of this LogicalBinaryOperatorAllOf.
        :type operand2: object
        """

        self._operand2 = operand2
