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
        if fileType == self.IP_CONFIG_FILE:
            configFilePath ="/lib/systemd/network/10-eth0.network"
        else:
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
                ipconfig = data.get('ipconfig', '')
                gateway = data.get('defaultgateway', '').strip()
                subnet_mask = data.get('subnet', '').strip()

                def subnet_to_cidr(subnet):
                    mask_mapping = {
                        "255.255.255.255": "32",
                        "255.255.255.254": "31",
                        "255.255.255.252": "30",
                        "255.255.255.248": "29",
                        "255.255.255.240": "28",
                        "255.255.255.224": "27",
                        "255.255.255.192": "26",
                        "255.255.255.128": "25",
                        "255.255.255.0": "24",
                        "255.255.254.0": "23",
                        "255.255.252.0": "22",
                        "255.255.248.0": "21",
                        "255.255.240.0": "20",
                        "255.255.224.0": "19",
                        "255.255.192.0": "18",
                        "255.255.128.0": "17",
                        "255.255.0.0": "16",
                        "255.254.0.0": "15",
                        "255.252.0.0": "14",
                        "255.248.0.0": "13",
                        "255.240.0.0": "12",
                        "255.224.0.0": "11",
                        "255.192.0.0": "10",
                        "255.128.0.0": "9",
                        "255.0.0.0": "8",
                        "254.0.0.0": "7",
                        "252.0.0.0": "6",
                        "248.0.0.0": "5",
                        "240.0.0.0": "4",
                        "224.0.0.0": "3",
                        "192.0.0.0": "2",
                        "128.0.0.0": "1",
                        "0.0.0.0": "0"
                    }
                    return mask_mapping.get(subnet, "24")

                cidr_suffix = subnet_to_cidr(subnet_mask)

                configTag.write("[Match]\n")
                configTag.write("Name=eth0\n\n")

                configTag.write("[Network]\n")
                configTag.write("DHCP=ipv4\n")
                configTag.write("Address=192.168.3.11/24\n")
                if ipconfig and ipconfig != "192.168.3.11":
                    configTag.write("Address=" + str(ipconfig) + "/" + str(cidr_suffix) + "\n")
                if gateway:
                    configTag.write("Gateway=" + str(gateway) + "\n\n")

                configTag.write("[DHCP]\n")
                configTag.write("# When CriticalConnection is applied to networkd, the IP address will not\n")
                configTag.write("# change after this service was reloaded. Just reboot the system.\n")
                configTag.write("CriticalConnection=true\n")

            except Exception as e:
                configTag.write("[Match]\n")
                configTag.write("Name=eth0\n\n")

                configTag.write("[Network]\n")
                configTag.write("DHCP=ipv4\n")
                configTag.write("Address=\n")
                configTag.write("#add new address field same like above line\n")
                configTag.write("#Gateway=\n\n")

                configTag.write("[DHCP]\n")
                configTag.write("# When CriticalConnection is applied to networkd, the IP address will not\n")
                configTag.write("# change after this service was reloaded. Just reboot the system.\n")
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




