#!/usr/bin/env python
#
# Copyright (c) Microsoft Corporation. All rights reserved.
# Copyright 2016 Confluent Inc.
# Licensed under the MIT License.
# Licensed under the Apache License, Version 2.0
#
# Original Confluent sample modified for use with Azure Event Hubs for Apache Kafka Ecosystems

import os
import sys
from confluent_kafka import Producer

ssl_ca_location = os.environ['ssl_ca_location']
bootstrap_servers = os.environ['bootstrap_servers']
sasl_password = os.environ['sasl_password']
topic_name = os.environ['topic_name']

if __name__ == '__main__':
    # Producer configuration
    conf = {
        'bootstrap.servers': bootstrap_servers, #replace
        'security.protocol': 'SASL_SSL',
        'ssl.ca.location': ssl_ca_location,
        'sasl.mechanism': 'PLAIN',
        'sasl.username': '$ConnectionString',
        'sasl.password': sasl_password,          #replace
        'client.id': 'python-example-producer'
    }

    # Create Producer instance
    p = Producer(**conf)


    def delivery_callback(err, msg):
        if err:
            sys.stderr.write('%% Message failed delivery: %s\n' % err)
        else:
            sys.stderr.write('%% Message delivered to %s [%d] @ %o\n' % (msg.topic(), msg.partition(), msg.offset()))


    # Write 1-10 to topic
    for i in range(0, 10):
        try:
            p.produce(topic_name, str(i), callback=delivery_callback)
        except BufferError as e:
            sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(p))
        p.poll(0)

    # Wait until all messages have been delivered
    sys.stderr.write('%% Waiting for %d deliveries\n' % len(p))
    p.flush()