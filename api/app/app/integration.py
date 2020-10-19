#!/usr/bin/env python
import pika
from app.models import Lolomo, NetflixSuggestMetadata


class MessagingGateway:

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='integration', exchange_type='topic')

    @classmethod
    def publish(cls, entity):
        if type(entity) == Lolomo:
            MessagingGateway().publish_lolomo(entity)
        elif type(entity) == NetflixSuggestMetadata:
            MessagingGateway().publish_thumbnail(entity)
        else:
            pass

    def publish_lolomo(self, lolomo):
        self.channel.basic_publish(exchange='integration',
                                   routing_key='integration.lolomo',
                                   body=lolomo.json())
        self.close()

    def publish_thumbnail(self, thumbnail):
        self.channel.basic_publish(exchange='integration',
                                   routing_key='integration.thumbnail',
                                   body=thumbnail.json_content())

        self.close()

    def close(self):

        self.connection.close()
