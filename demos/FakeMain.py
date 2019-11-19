# 参考教程 https://www.cnblogs.com/mrchige/p/6389588.html
# from faker import Faker
# import paho.mqtt.client as mqtt
from sqlalchemy import create_engine
import time
# from .config import MQTTHOST, MQTTPORT, DB_URL
# from .sensors import fake_sensor_data

# f = Faker(locale='zh_CN')


# mqttClient = mqtt.Client()
# 连接MQTT服务器
# def on_mqtt_connect():
#     mqttClient.connect(MQTTHOST, MQTTPORT, 60)
#     mqttClient.loop_start()
# # publish 消息
# def on_publish(topic, payload, qos):
#     print("on_publish")
#     mqttClient.publish(topic, payload, qos)
# # 消息处理函数
# def on_message_come(lient, userdata, msg):
#     print(msg.topic + " " + ":" + str(msg.payload))
#     # subscribe 消息
# def on_subscribe():
#     print("on_publish")
#     mqttClient.subscribe("/server", 1)
#     mqttClient.on_message = on_message_come # 消息到来处理函数

# mqtt_topic=["sensors/iot_simulator",
#     "pigs/profile/add",
#     "pigs/profile/update",
#     "sensors/temp",
#     "sensors/humi",
#     "sensors/light",
#     "sensors/aqi"]


# def main():
#     on_mqtt_connect()
#     # on_publish("/cayennemqtt_test.py/server", "Hello Python!", 1)
#     # on_publish("sensors/".format(), "Hello Python!", 1)
#     # on_subscribe()
#     while True:
#         # python字典类型转换为json对象
#
#         user_name = f.user_name()
#         clientid = abs(hash(user_name))
#         location = f.numerify() #单元编号
#         s_index = f.random_int(min=0, max=len(sensor_type)-1)
#
#         json_str = fake_sensor_data(clientid, user_name ,sensor_type=sensor_type[s_index], unit=sensor_unit_list[s_index], min=sensor_range_min[s_index], max=sensor_range_max[s_index])
#
#
#         engine = create_engine(DB_URL)
#         print(engine)
#         # on_publish("sensors/{}/{}/{}/{}".format(user_name,clientid, sensor_type[s_index],  location), json_str, 1)
#         # print(json_str)
#         time.sleep(3)

if __name__ == '__main__':
    print("hello")
  # main()







