# MQTTHOST = "192.168.8.102"
# MQTTPORT = 1883
#

DB_USER = 'hass'
DB_PSD = 'hass'
DB_HOST = "192.168.8.102"
DB_DATABASE =  "iot_db2"
DB_CHARSET = "utf8"

IOT_BIG_DATA_USER = 'hass'
IOT_BIG_DATA_PSD = 'hass'
IOT_BIG_DATA_HOST = '192.168.8.102'
IOT_BIG_DATA_DATABASE = 'iot_big_data_db'
IOT_BIG_DATA_CHARSET = 'utf8'

DB_URL ='mysql+pymysql://'+DB_USER+':'+DB_PSD+'@'+DB_HOST+'/'+DB_DATABASE+'?charset='+DB_CHARSET

PIG_PRICE_URL = "http://www.dongbao120.com/jinrizhujia/"