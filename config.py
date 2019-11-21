__version__ = '2.0.3'

# MQTT_BROKER = "192.168.8.102"
MQTT_BROKER = "172.29.46.236"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "demo_wd"
MQTT_USER = "demo"
MQTT_PSW = "demo"
MQTT_PROTOCOL = "3.1"

# 身份验证API
ApiHost = MQTT_BROKER


DB_USER = 'hass'
DB_PSD = 'hass'
DB_HOST = '172.29.46.236'
# DB_HOST = "192.168.8.102"
DB_DATABASE =  "iot_db2"
DB_CHARSET = "utf8"

IOT_BIG_DATA_USER = 'hass'
IOT_BIG_DATA_PSD = 'hass'
IOT_BIG_DATA_HOST = DB_HOST
IOT_BIG_DATA_DATABASE = 'iot_big_data_db'
IOT_BIG_DATA_CHARSET = 'utf8'

DB_URL ='mysql+pymysql://'+DB_USER+':'+DB_PSD+'@'+DB_HOST+'/'+DB_DATABASE+'?charset='+DB_CHARSET

PIG_PRICE_URL = "http://www.dongbao120.com/jinrizhujia/"