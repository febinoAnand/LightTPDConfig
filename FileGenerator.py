import os
from DatabaseManager import DatabaseManager
from InitialData.FileName import ConfigFileName


class ConfigFileGenerator:
    WIFI_CONFIG_FILE = ConfigFileName.wifiConfigFileName
    SERVER_CONFIG_FILE = ConfigFileName.serverConfigFileName
    GLOBAL_FIREWALL_CONFIG_FILE = ConfigFileName.globalFireWallFileName
    MODBUS_TCP_IP_CONFIG_FILE = ConfigFileName.modbusTCPIPConfigFileName
    MQTT_TOPIC_CONFIG_FILE = ConfigFileName.mqttTopicFileName
    SPECIFIC_FIREWALL_CONFIG_FILE = ConfigFileName.specificFireWallFileName
    TAG_CONFIG_FILE = ConfigFileName.tagConfigFilename

    def __init__(self,path):
        self.path = path
        return

    def generateFile(self,fileType):
        configFilePath = os.path.join(self.path, fileType)
        configTag = open(configFilePath,'w')
        db = DatabaseManager(self.path)

        if fileType == self.WIFI_CONFIG_FILE:
            try:
                data = db.selectFromWifiSettingTable()[0]
                configTag.write("CONFIG_WIFI_SSID="+data["ssid"]+"\n")
                configTag.write("CONFIG_WIFI_PASS="+data["password"])
            except Exception as e:
                configTag.write("CONFIG_WIFI_SSID=\n")
                configTag.write("CONFIG_WIFI_PASS=")

        elif fileType == self.GLOBAL_FIREWALL_CONFIG_FILE:
            try:
                data = db.selectFromGlobalFirewallTable()[0]
                configTag.write("CONFIG_FIREWALL_DEFAULT_INCOMING="+data['incoming']+"\n")
                configTag.write("CONFIG_FIREWALL_DEFAULT_OUTGOING="+data['outgoing'])

            except Exception as e:
                configTag.write("CONFIG_FIREWALL_DEFAULT_INCOMING="+"\n")
                configTag.write("CONFIG_FIREWALL_DEFAULT_OUTGOING=")

        elif fileType == self.MODBUS_TCP_IP_CONFIG_FILE:
            try:
                data = db.selectAllFromModbusTCPIP()
                for ip in data:
                    configTag.write(ip['ipaddress']+",\n")
            except Exception as e:
                print (e)
                configTag.write("")

        elif fileType == self.TAG_CONFIG_FILE:
            try:
                dataList = db.selectAllFromTagConfig()
                for data in dataList:
                    configTag.write(data['tag_name']+",")
                    configTag.write(str(data['source_interface'])+",")
                    configTag.write(str(data['modbus_tcp_ip_id'])+",")
                    configTag.write(str(data['port'])+",")
                    configTag.write(str(data['slave_id'])+",")
                    configTag.write(str(data['function_code'])+",")
                    configTag.write(str(data['reg_address'])+",")
                    configTag.write(str(data['no_of_reg_read'])+",")
                    configTag.write(str(data['datatype'])+",")
                    configTag.write(str(data['modbus_function'])+",")
                    configTag.write(str(data['multiplication_factor'])+",")
                    configTag.write(str(data['modbus_base_address'])+",")
                    configTag.write(str(data['modbus_string_id'])+",")
                    configTag.write(str(data['mqtt_topic_id'])+",")
                    configTag.write(str(data['mqtt_function'])+",")
                    configTag.write(str(data['transmit_type'])+",")
                    configTag.write(str(data['transmit_interval'])+",")
                    configTag.write(str(data['raw_data_buffer'])+",")
                    configTag.write(str(data['processed_data_buffer']))
                    configTag.write(",\n")
            except Exception as e:
                print (e)
                configTag.write("")

        elif fileType == self.SPECIFIC_FIREWALL_CONFIG_FILE:
            try:
                dataList = db.selectAllFromSpecificFirewall()
                for data in dataList:
                    configTag.write(data['source_ip']+",")
                    configTag.write(str(data['source_port'])+",")
                    configTag.write(data['destination_ip']+",")
                    configTag.write(str(data['destination_port'])+",")
                    configTag.write(data['access'])
                    configTag.write("\n")
            except Exception as e:
                print (e)
                configTag.write("")


        elif fileType == self.MQTT_TOPIC_CONFIG_FILE:
            try:
                data = db.selectAllFromMqttTopicList()
                for topic in data:
                    configTag.write(topic['topic']+",\n")
            except Exception as e:
                print (e)
                configTag.write("")


        elif fileType == self.SERVER_CONFIG_FILE:
            try:
                data = db.selectFromServerConfigTable()[0]
                configTag.write("CONFIG_SERVER_PROTOCOL="+data["protocol"]+"\n")
                configTag.write("CONFIG_SERVER_MQTT_URL="+data["host"]+"\n")
                configTag.write("CONFIG_SERVER_MQTT_PORT="+str(data["port"])+"\n")
                configTag.write("CONFIG_SERVER_MQTT_QOS="+str(data["qos"])+"\n")
                configTag.write("CONFIG_SERVER_MQTT_USERNAME="+data["username"]+"\n")
                configTag.write("CONFIG_SERVER_MQTT_USERPASS="+data["password"]+"\n")
                configTag.write("CONFIG_SERVER_MQTT_CLIENTID="+data["client"]+"\n")
                configTag.write("CONFIG_SERVER_MQTT_KEEPALIVESEC="+str(data["keepalive"]))
            except Exception as e:
                configTag.write("CONFIG_SERVER_PROTOCOL=\n")
                configTag.write("CONFIG_SERVER_MQTT_URL=\n")
                configTag.write("CONFIG_SERVER_MQTT_PORT=\n")
                configTag.write("CONFIG_SERVER_MQTT_QOS=\n")
                configTag.write("CONFIG_SERVER_MQTT_USERNAME=\n")
                configTag.write("CONFIG_SERVER_MQTT_USERPASS=\n")
                configTag.write("CONFIG_SERVER_MQTT_CLIENTID=\n")
                configTag.write("CONFIG_SERVER_MQTT_KEEPALIVESEC=")

        configTag.close()

    def generateAllFile(self):
        pass




