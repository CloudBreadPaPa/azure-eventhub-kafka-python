#!/usr/bin/env python
import os
import sys
import random
import string
import time
import json
from datetime import datetime
from confluent_kafka import Producer

ssl_ca_location = os.environ['ssl_ca_location']
bootstrap_servers = os.environ['bootstrap_servers']
sasl_password = os.environ['sasl_password']
topic_name = os.environ['topic_name']

if __name__ == '__main__':

    conf = {
        'bootstrap.servers': bootstrap_servers,
        'security.protocol': 'SASL_SSL',
        'ssl.ca.location': ssl_ca_location,
        'sasl.mechanism': 'PLAIN',
        'sasl.username': '$ConnectionString',
        'sasl.password': sasl_password,
        'client.id': 'python-example-producer'
    }

    # Create Producer instance
    p = Producer(**conf)

    def delivery_callback(err, msg):
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write(
                '%% Message delivered to %s [%d] @ %o\n' %
                (msg.topic(), msg.partition(), msg.offset()))

    def build_message():
        msg = {}
        msg["product_num"] = round(random.uniform(1, 10))
        msg["product_price"] = round(random.uniform(100, 10000))
        msg["product_description"] = ''.join(random.SystemRandom().choice(string.ascii_letters+string.digits) for _ in range(10))
        msg["product_production_dt"] = str(datetime.utcnow())
        return json.dumps(msg)

    # Infinite loop, send messages to event hub
    while True:
        try:
            p.produce(topic_name, build_message(), callback=delivery_callback)
        except BufferError as e:
            sys.stderr.write(
                '%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
                len(p))
        p.poll(0)
        time.sleep(1)
