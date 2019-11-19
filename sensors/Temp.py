import sys
sys.path.append("..")
from utils.logger import exception, setInfo,info, logJson
from cloud import cayennemqtt
if __name__ == '__main__':
    setInfo()
    cayennemqtt