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
    IP_CONFIG_FILE = ConfigFileName.ipaddressFileName
    UART_CONFIG_FILE = ConfigFileName.uarConfigtFileName

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
                configTag.write("CONFIG_SERVER_MQTT_KEEPALIVESEC="+str(data["keepalive"])+"\n")
                configTag.write("CONFIG_SERVER_MQTT_SECURE_TOKEN="+str(data["secure_token"]))
            except Exception as e:
                configTag.write("CONFIG_SERVER_PROTOCOL=\n")
                configTag.write("CONFIG_SERVER_MQTT_URL=\n")
                configTag.write("CONFIG_SERVER_MQTT_PORT=\n")
                configTag.write("CONFIG_SERVER_MQTT_QOS=\n")
                configTag.write("CONFIG_SERVER_MQTT_USERNAME=\n")
                configTag.write("CONFIG_SERVER_MQTT_USERPASS=\n")
                configTag.write("CONFIG_SERVER_MQTT_CLIENTID=\n")
                configTag.write("CONFIG_SERVER_MQTT_KEEPALIVESEC=\n")
                configTag.write("CONFIG_SERVER_MQTT_SECURE_TOKEN=")

        elif fileType == self.IP_CONFIG_FILE:
            try:
                data = db.selectFromIPConfigTable()[0]
                configTag.write("[Match]\n")
                configTag.write(f"Name=eth0\n\n")

                configTag.write("[Network]\n")
                configTag.write(f"DHC=ipv4\n")
                configTag.write(f"Address=192.168.3.11/24\n")
                configTag.write(f"Address={data['ipconfig']}/24\n")
                configTag.write(f"#Gateway= gateway iP\n\n")

                configTag.write("[DHCP]\n")
                configTag.write("#When CriticalConnection is applied to networkd, the IP address will not\n")
                configTag.write("#change after this service was reloaded. Just reboot the system.\n")
                configTag.write("CriticalConnection=true\n")

            except Exception as e:
                configTag.write("[Match]\n")
                configTag.write(f"Name=eth0\n\n")
                
                configTag.write("[Network]\n")
                configTag.write("DHC=ipv4\n")
                configTag.write("Address=\n")
                configTag.write("#add new address field same like above line\n")
                configTag.write("#Gateway=\n\n")

                configTag.write("[DHCP]\n")
                configTag.write("#When CriticalConnection is applied to networkd, the IP address will not\n")
                configTag.write("#change after this service was reloaded. Just reboot the system.\n")
                configTag.write("CriticalConnection=true\n")

        elif fileType == self.UART_CONFIG_FILE:
            try:
                data = db.selectFromUartConfigTable()[0]
                configTag.write("CONFIG_UART_BAUD_RATE=" + str(data["baudrate"]) + "\n")
                configTag.write("CONFIG_UART_PARITY=" + str(data["parity"]) + "\n")
                configTag.write("CONFIG_UART_DATA_BITS=" + str(data["databits"]) + "\n")
                configTag.write("CONFIG_UART_STOP_BITS=" + str(data["stopbits"]) + "\n")
            except Exception as e:
                configTag.write("CONFIG_UART_BAUD_RATE=\n")
                configTag.write("CONFIG_UART_PARITY=\n")
                configTag.write("CONFIG_UART_DATA_BITS=\n")
                configTag.write("CONFIG_UART_STOP_BITS=\n")

            configTag.flush()
            os.fsync(configTag.fileno())
            configTag.close()

    def generateAllFile(self):
        pass




