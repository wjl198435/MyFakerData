from influxdb import InfluxDBClient

json_body = [
    # {
    #     "measurement": "cpu_load_short",
    #     "tags": {
    #         "host": "server01",
    #         "region": "us-west"
    #     },
    #     "time": "2009-11-10T23:00:00Z",
    #     "fields": {
    #         "value": 0.64
    #     }
    # }
    {
        "measurement": "cpu_load_short",
        "tags": {
            "省份": "广东",
            "猪种": "外三元"
        },
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "价格": 24.64
        }
    }
]

client = InfluxDBClient('192.168.8.104', 8086, 'root', 'root', 'example')

client.create_database('example')

client.write_points(json_body)

result = client.query('select value from cpu_load_short;')

print("Result: {0}".format(result))