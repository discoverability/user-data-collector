import connexion
import six

from openapi_server.models.check_criteria_request import CheckCriteriaRequest  # noqa: E501
from openapi_server.models.content_match_criteria import ContentMatchCriteria  # noqa: E501
from openapi_server.models.thumbnail import Thumbnail  # noqa: E501
from openapi_server.models.user import User  # noqa: E501
from openapi_server import util


def check_criteria_post(check_criteria_request):  # noqa: E501
    """check_criteria_post

     # noqa: E501

    :param check_criteria_request: allow criteria checking for a list of content
    :type check_criteria_request: dict | bytes

    :rtype: List[ContentMatchCriteria]
    """
    if connexion.request.is_json:
        check_criteria_request = CheckCriteriaRequest.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def thumbnails_user_id_session_id_get(user_id, session_id):  # noqa: E501
    """thumbnails_user_id_session_id_get

    provides a list of users and their associated streaming sessions # noqa: E501

    :param user_id: user anonymised id
    :type user_id: str
    :param session_id: session for a particular user
    :type session_id: str

    :rtype: List[Thumbnail]
    """
    return 'do some magic!'


def users_get():  # noqa: E501
    """users_get

     # noqa: E501


    :rtype: List[User]
    """
    return 'do some magic!'
