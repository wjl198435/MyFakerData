__version__ = '2.0.3'

# MQTT_BROKER = "192.168.8.102"
MQTT_BROKER = "192.168.8.102"
MQTT_PORT = 1883
MQTT_CLIENT_ID = "demo_wd"
MQTT_USER = "demo"
MQTT_PSW = "demo"
MQTT_PROTOCOL = "3.1"

MQTT_DIS_PREFIX = "homeassistant"

# 身份验证API
ApiHost = MQTT_BROKER


DB_USER = 'hass'
DB_PSD = 'hass'
DB_HOST = '192.168.8.102'
# DB_HOST = "192.168.8.102"
DB_DATABASE =  "iot_db2"
DB_CHARSET = "utf8"

BIG_DATA_USER = 'hass'
BIG_DATA_PSD = 'hass'
BIG_DATA_HOST = DB_HOST
BIG_DATA_DATABASE = 'iot_big_data_db_test'
BIG_DATA_CHARSET = 'utf8'

DB_URL = 'mysql+pymysql://'+DB_USER+':'+DB_PSD+'@'+DB_HOST+'/'+DB_DATABASE+'?charset='+DB_CHARSET

BD_DATA_URL = 'mysql+pymysql://'+BIG_DATA_USER+':'+BIG_DATA_PSD+'@'+BIG_DATA_HOST+'/'+BIG_DATA_DATABASE+'?charset='+DB_CHARSET

PIG_PRICE_URL = "http://www.dongbao120.com/jinrizhujia/"