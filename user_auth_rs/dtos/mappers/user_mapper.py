from ..user_dto import UserDTO
from flask import jsonify


class UserMapper(object):

    @staticmethod
    def map_to_dto(user):
        return jsonify(UserDTO(user.username, user.password, user.role).__dict__)
