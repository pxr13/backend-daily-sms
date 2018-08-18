from flask_restful import Resource, reqparse

from errors import DbError, UpdateMessageError

message_counter = 1  # REMOVE: only for rapid prototyping
db = []


def add_to_parser(parser, field, type):
    parser.add_argument(field, type=type, location='json')


class Message(Resource):
    parser = reqparse.RequestParser()
    add_to_parser(parser, 'text', str)
    add_to_parser(parser, 'send_time', str)
    add_to_parser(parser, 'frequency', list)
    add_to_parser(parser, 'active', bool)

    def post(self, user_id):
        """Create a daily message"""
        data = Message.parser.parse_args()
        new_message = {**data, 'user_id': user_id,
                       'message_id': message_counter}

        try:
            db.append(new_message)
        except RuntimeError:
            raise DBError('Error saving to DB.')

        return new_message, 201

    def put(self, user_id, message_id):
        """Update daily message properties"""
        for idx, message in enumerate(db):
            if message['message_id'] == message_id:
                self._update_db(message)
                break
        else:
            raise UpdateMessageError(user_id, message_id)

        return {'success': 'ok'}, 202

    def _update_db(self, message):
        data = Message.parser.parse_args()
        message.update(data)


class MessageList(Resource):
    def get(self, id):
        """Return all messages for given user"""
        return [message for message in db if message['user_id'] == id]
