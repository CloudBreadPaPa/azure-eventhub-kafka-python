# Apache kafka messages to event hub 
In this repository, produce `kafka` messages to `azure event hub` with python code

# Getting Started
TODO: Setup python 3.8+ environment and run code
- Create event hub in Azure portal or CLI
- review [azure-event-hubs-for-kafka](https://github.com/Azure/azure-event-hubs-for-kafka/tree/master/quickstart/python) repository
- Set endpoint and secret information
- Run `setup.sh`
  - pip package insall code, `sudo pip install confluent-kafka` remove `sudo` in case of using, conda env
- make & run`run-producer.sh` or `run-producer-loop.sh` with environment variable

## example `run-producer.sh` file
```
export ssl_ca_location="/usr/lib/ssl/certs/ca-certificates.crt"  # ubuntu ca certificate
export bootstrap_servers="<YOUR-EVENTHUB-NS>.servicebus.windows.net:9093"
export sasl_password="<YOUR-EVENTHUB-CONNECTION-STRING>"
export topic_name="<YOUR-EVENTHUB-NAME>"

python producer.py
```

# Build and Test
- Compatible with Python 3.8+