import os.path
import sqlite3
from InitialData.DatabaseData import ServerInitalData,\
                                    WIFISettingInitialData, \
                                    DBconnent,\
                                    GlobalFirewallInitalData,\
                                    UserLogin

class DatabaseManager:

######################## Tag Config Table #######################

    TAG_CONFIG_TABLE = 'tag_config'

    ROW_TAG_TABLE_ID = '_id'
    ROW_TAG_NAME = 'tag_name'
    ROW_SOURCE_INTERFACE = "source_interface"
    ROW_MODBUS_TCP_IP_INDEX = 'modbus_tcp_ip_id'
    ROW_PORT = 'port'
    ROW_SLAVE_ID = 'slave_id'
    ROW_FUNCTION_CODE = 'function_code'
    ROW_REG_ADDRESS = 'reg_address'
    ROW_NO_OF_REG_READ = 'no_of_reg_read'
    ROW_DATA_TYPE = 'datatype'
    ROW_MODBUS_FUNCTION = 'modbus_function'
    ROW_MULTIPLICATION_FACTOR = 'multiplication_factor'
    ROW_MODBUS_BASE_ADDRESS = 'modbus_base_address'
    ROW_MODBUS_STRING_INDEX = 'modbus_string_id'
    ROW_MQTT_TOPIC_INDEX = 'mqtt_topic_id'
    ROW_MQTT_FUCNTION = 'mqtt_function'
    ROW_TRANSMIT_TYPE = 'transmit_type'
    ROW_TRANSMIT_INTERVAL = 'transmit_interval'
    ROW_RAW_DATA_BUFFER = 'raw_data_buffer'
    ROW_PROCESSSED_DATA_BUFFER = 'processed_data_buffer'



    def __init__(self,path):
        self.dbpath = os.path.join(path,DBconnent.dbName)
        self.conn = sqlite3.connect(self.dbpath)

        # creating the table
        self.__createTagConfigTable()
        self.__createServerConfigTable()
        self.__createWifiSettingTable()
        self.__createGlobalFirewallTable()
        self.__createModbusTCPIPTable()
        self.__createMqttTopicListTable()
        self.__createSpecificFirewallTable()
        self.__createAdminAuthTable()

        # initialize the value in the table
        self.__initializeServerConfigTableData()
        self.__initializeWifiSettingTableData()
        self.__initializeGlobalFirewallTableData()
        self.__initializeUserLoginTableData()


        self.conn.close()

    def __dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d


    def __createTagConfigTable(self):
        self.conn.execute('CREATE TABLE IF NOT EXISTS '+self.TAG_CONFIG_TABLE +' ('
                          + self.ROW_TAG_TABLE_ID +' INTEGER PRIMARY KEY AUTOINCREMENT,'
                          + self.ROW_TAG_NAME +' TEXT ,'
                          + self.ROW_SOURCE_INTERFACE +' TEXT ,'
                          + self.ROW_MODBUS_TCP_IP_INDEX +' INTEGER, '
                          + self.ROW_PORT +' INTEGER, '
                          + self.ROW_SLAVE_ID +' INTEGER, '
                          + self.ROW_FUNCTION_CODE +' INTEGER, '
                          + self.ROW_REG_ADDRESS +' INTEGER, '
                          + self.ROW_NO_OF_REG_READ +' INTEGER, '
                          + self.ROW_DATA_TYPE +' CHAR(20), '
                          + self.ROW_MODBUS_FUNCTION +' INTEGER, '
                          + self.ROW_MODBUS_BASE_ADDRESS +' CHAR(20), '
                          + self.ROW_MODBUS_STRING_INDEX +' INTEGER, '
                          + self.ROW_MQTT_TOPIC_INDEX +' INTEGER, '
                          + self.ROW_MULTIPLICATION_FACTOR +' INTEGER, '
                          + self.ROW_MQTT_FUCNTION +' CHAR(20), '
                          + self.ROW_TRANSMIT_TYPE +' CHAR(20), '
                          + self.ROW_TRANSMIT_INTERVAL +' INTEGER, '
                          + self.ROW_RAW_DATA_BUFFER +' TEXT DEFAULT 0, '
                          + self.ROW_PROCESSSED_DATA_BUFFER +' TEXT DEFAULT 0'
                          +')')
        self.conn.commit()



    def insertIntoTagConfigTable(self,data):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()

        sqlQuery = "INSERT INTO " + self.TAG_CONFIG_TABLE + " ("+ \
                    self.ROW_TAG_NAME+","+ \
                    self.ROW_SOURCE_INTERFACE+","+ \
                    self.ROW_MODBUS_TCP_IP_INDEX+","+\
                    self.ROW_PORT+","+\
                    self.ROW_SLAVE_ID+","+\
                    self.ROW_FUNCTION_CODE+","+\
                    self.ROW_REG_ADDRESS+","+\
                    self.ROW_DATA_TYPE+","+\
                    self.ROW_NO_OF_REG_READ+","+\
                    self.ROW_MODBUS_FUNCTION+","+\
                    self.ROW_MULTIPLICATION_FACTOR+","+\
                    self.ROW_MODBUS_BASE_ADDRESS+","+\
                    self.ROW_MODBUS_STRING_INDEX+","+\
                    self.ROW_MQTT_TOPIC_INDEX+","+\
                    self.ROW_MQTT_FUCNTION+","+\
                    self.ROW_TRANSMIT_TYPE+","+\
                    self.ROW_TRANSMIT_INTERVAL+\
                    ") VALUES ("+\
                    "'"+data['tag_name']+"',"+\
                    "'"+data['source_interface']+"',"+\
                    data['modbus_tcp_ip']+","+\
                    data['port']+","+\
                    data['slave_id']+","+ \
                   "'"+data['function_code']+"',"+\
                    data['reg_address']+","+\
                    "'"+data['data_type']+"',"+\
                    data['no_of_reg_read']+","+\
                    "'"+data['modbus_function']+"',"+\
                    data['multiplication_factor']+","+\
                    "'"+data['modbus_base_address']+"',"+\
                    data['modbus_string_index']+","+ \
                   "'"+data['mqtt_topic_index']+"',"+\
                    "'"+data['mqtt_function']+"',"+ \
                   "'"+data['transmit_type']+"',"+ \
                   data['transmit_interval']+""+ \
                   ");"
        print(sqlQuery)
        cursor.execute(sqlQuery)
        conn.commit()
        conn.close()

    def updateTagConfigTableByID(self,id,data):

        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        sqlQuery = "UPDATE "+self.TAG_CONFIG_TABLE+" SET "+\
                    self.ROW_TAG_NAME + " = '"+ data["tag_name"] + "', "+\
                    self.ROW_SOURCE_INTERFACE + " = '"+ data["source_interface"] + "', "+\
                    self.ROW_MODBUS_TCP_IP_INDEX + " = "+ data["modbus_tcp_ip"] + ", "+\
                    self.ROW_PORT + " = "+ data["port"] + ", "+\
                    self.ROW_SLAVE_ID + " = "+ data["slave_id"] + ", "+\
                    self.ROW_FUNCTION_CODE + " = "+ data["function_code"] + ", "+\
                    self.ROW_REG_ADDRESS + " = "+ data["reg_address"] + ", "+\
                    self.ROW_DATA_TYPE + " = '"+ data["data_type"] + "', "+\
                    self.ROW_NO_OF_REG_READ + " = "+ data["no_of_reg_read"] + ", "+\
                    self.ROW_MODBUS_FUNCTION + " = '"+ data["modbus_function"] + "', "+\
                    self.ROW_MULTIPLICATION_FACTOR + " = "+ data["multiplication_factor"] + ", "+\
                    self.ROW_MODBUS_BASE_ADDRESS + " = '"+ data["modbus_base_address"] + "', "+\
                    self.ROW_MODBUS_STRING_INDEX + " = "+ data["modbus_string_index"] + ", "+\
                    self.ROW_MQTT_TOPIC_INDEX + " = "+ data["mqtt_topic_index"] + ", "+\
                    self.ROW_MQTT_FUCNTION + " = '"+ data["mqtt_function"] + "', "+\
                    self.ROW_TRANSMIT_INTERVAL + " = "+ data["transmit_interval"] + ", "+\
                    self.ROW_TRANSMIT_TYPE + " = '"+ data["transmit_type"] +"'"\
                    +" WHERE "+self.ROW_TAG_TABLE_ID+" = "+id
        cursor.execute(sqlQuery)
        conn.commit()
        conn.close()

    def deleteTagConfig(self,id):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM "+self.TAG_CONFIG_TABLE+" WHERE "+self.ROW_TAG_TABLE_ID+" = "+id)
        conn.commit()
        conn.close()

    def selectAllFromTagConfig(self):
        conn = sqlite3.connect(self.dbpath)
        conn.row_factory = self.__dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+self.TAG_CONFIG_TABLE)
        tagConfigData = cursor.fetchall()
        conn.close()
        return tagConfigData

    def selectFromTagConfigByID(self,id):
        conn = sqlite3.connect(self.dbpath)
        conn.row_factory = self.__dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+self.TAG_CONFIG_TABLE+" WHERE "+self.ROW_TAG_TABLE_ID+" = "+id)
        tagConfigData = cursor.fetchall()
        conn.close()
        return tagConfigData


    def selectFromTagConfigByName(self,name):
        conn = sqlite3.connect(self.dbpath)
        conn.row_factory = self.__dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+self.TAG_CONFIG_TABLE+" WHERE "+self.ROW_TAG_NAME+" = '"+name+"'")
        tagConfigData = cursor.fetchall()
        conn.close()
        return tagConfigData

    def getCountTagConfig(self):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM "+self.TAG_CONFIG_TABLE)
        count = cursor.fetchall()[0][0]
        conn.close()
        return count






#################### Server Config Table ##########################

    SERVER_CONFIG_TABLE = 'server_config'

    ROW_SERVER_TABLE_ID = '_id'
    ROW_SERVER_HOST = 'host'
    ROW_SERVER_PORT = 'port'
    ROW_SERVER_CLIENT = 'client'
    ROW_SERVER_QOS = 'qos'
    ROW_SERVER_PROTOCOL = 'protocol'
    ROW_SERVER_KEEPALIVESEC = 'keepalive'
    ROW_SERVER_USER_NAME = 'username'
    ROW_SERVER_PASSWORD = 'password'



    def __createServerConfigTable(self):
        self.conn.execute('CREATE TABLE IF NOT EXISTS '+self.SERVER_CONFIG_TABLE +' ('
                          + self.ROW_SERVER_TABLE_ID +' INTEGER PRIMARY KEY NOT NULL,'
                          + self.ROW_SERVER_HOST +' TEXT ,'
                          + self.ROW_SERVER_PROTOCOL +' TEXT ,'
                          + self.ROW_SERVER_PORT +' INTEGER, '
                          + self.ROW_SERVER_KEEPALIVESEC +' INTEGER, '
                          + self.ROW_SERVER_QOS +' INTEGER, '
                          + self.ROW_SERVER_CLIENT +' TEXT, '
                          + self.ROW_SERVER_USER_NAME +' TEXT, '
                          + self.ROW_SERVER_PASSWORD +' TEXT'
                          +')')
        self.conn.commit()


    def __initializeServerConfigTableData(self):
        sqlQuery = "INSERT OR IGNORE INTO " + self.SERVER_CONFIG_TABLE + " ("+ \
                   self.ROW_SERVER_TABLE_ID+","+ \
                   self.ROW_SERVER_HOST+","+ \
                   self.ROW_SERVER_PROTOCOL+","+ \
                   self.ROW_SERVER_PORT+","+ \
                   self.ROW_SERVER_KEEPALIVESEC+","+ \
                   self.ROW_SERVER_QOS+","+ \
                   self.ROW_SERVER_CLIENT+","+ \
                   self.ROW_SERVER_USER_NAME+","+ \
                   self.ROW_SERVER_PASSWORD+ \
                   ") VALUES ("+ \
                   "1,"+ \
                   "'"+ServerInitalData.URL+"',"+ \
                   "'"+ServerInitalData.PROTOCOL+"',"+ \
                   str(ServerInitalData.PORT)+","+ \
                   str(ServerInitalData.KEEPALIVESEC)+","+ \
                   str(ServerInitalData.QOS)+","+ \
                   "'"+ServerInitalData.CLIENTID+"',"+ \
                   "'"+ServerInitalData.USERNAME+"',"+ \
                   "'"+ServerInitalData.USERPASS+"'"+ \
                   ");"
        cursor = self.conn.cursor()
        cursor.execute(sqlQuery)
        self.conn.commit()

    def selectFromServerConfigTable(self):
        conn = sqlite3.connect(self.dbpath)
        conn.row_factory = self.__dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+self.SERVER_CONFIG_TABLE+ " WHERE "+self.ROW_SERVER_TABLE_ID+" = 1")
        serverConfig = cursor.fetchall()
        conn.close()
        return serverConfig



    def updateServerConfigTable(self,data):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        sqlQuery = "UPDATE "+self.SERVER_CONFIG_TABLE+" SET "+ \
                   self.ROW_SERVER_HOST + " = '"+ data["host"] + "', "+ \
                   self.ROW_SERVER_PROTOCOL + " = '"+ data["protocol"] + "', "+ \
                   self.ROW_SERVER_PORT + " = "+ data["port"] + ", "+ \
                   self.ROW_SERVER_KEEPALIVESEC + " = "+ data["keep_alive"] + ", "+ \
                   self.ROW_SERVER_QOS + " = "+ data["qos"] + ", "+ \
                   self.ROW_SERVER_CLIENT + " = '"+ data["client"] + "', "+ \
                   self.ROW_SERVER_USER_NAME + " = '"+ data["username"] + "', "+ \
                   self.ROW_SERVER_PASSWORD + " = '"+ data["password"] +"'" \
                   +" WHERE "+self.ROW_SERVER_TABLE_ID+" = 1"
        cursor.execute(sqlQuery)
        conn.commit()
        conn.close()






#################### Wifi Setting Table ##########################

    TABLE_WIFI_SETTING = 'wifi_setting'

    ROW_WIFI_ID = '_id'
    ROW_WIFI_SSID = 'ssid'
    ROW_WIFI_PASSWORD = 'password'

    def __createWifiSettingTable(self):
        self.conn.execute('CREATE TABLE IF NOT EXISTS '+self.TABLE_WIFI_SETTING +' ('
                          + self.ROW_WIFI_ID +' INTEGER PRIMARY KEY NOT NULL,'
                          + self.ROW_WIFI_SSID +' TEXT ,'
                          + self.ROW_WIFI_PASSWORD +' TEXT'
                          +')')
        self.conn.commit()



    def __initializeWifiSettingTableData(self):
        sqlQuery = "INSERT OR IGNORE INTO " + self.TABLE_WIFI_SETTING + " ("+ \
                   self.ROW_WIFI_ID+","+ \
                   self.ROW_WIFI_SSID+","+ \
                   self.ROW_WIFI_PASSWORD+ \
                   ") VALUES ("+ \
                   "1,"+ \
                   "'"+WIFISettingInitialData.SSID+"',"+ \
                   "'"+WIFISettingInitialData.PASSWORD+"'"+ \
                   ");"
        cursor = self.conn.cursor()
        cursor.execute(sqlQuery)
        self.conn.commit()


    def selectFromWifiSettingTable(self):
        conn = sqlite3.connect(self.dbpath)
        conn.row_factory = self.__dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+self.TABLE_WIFI_SETTING+ " WHERE "+self.ROW_WIFI_ID+" = 1")
        wifiConfig = cursor.fetchall()
        conn.close()
        return wifiConfig


    def updateWifiSettingTable(self,data):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        sqlQuery = "UPDATE "+self.TABLE_WIFI_SETTING+" SET "+ \
                   self.ROW_WIFI_SSID + " = '"+ data["ssid"] + "', "+ \
                   self.ROW_WIFI_PASSWORD + " = '"+ data["password"] +"'" \
                   +" WHERE "+self.ROW_WIFI_ID+" = 1"
        cursor.execute(sqlQuery)
        conn.commit()
        conn.close()





#################### Global Firewall Table ##########################

    TABLE_GLOBAL_FIREWALL = 'global_firewall'

    ROW_GLOBAL_ID = '_id'
    ROW_GLOBAL_INCOMING = 'incoming'
    ROW_GLOBAL_OUTGOING = 'outgoing'

    def __createGlobalFirewallTable(self):
        self.conn.execute('CREATE TABLE IF NOT EXISTS '+self.TABLE_GLOBAL_FIREWALL +' ('
                          + self.ROW_GLOBAL_ID +' INTEGER PRIMARY KEY NOT NULL,'
                          + self.ROW_GLOBAL_INCOMING +' TEXT ,'
                          + self.ROW_GLOBAL_OUTGOING +' TEXT'
                          +')')
        self.conn.commit()



    def __initializeGlobalFirewallTableData(self):
        sqlQuery = "INSERT OR IGNORE INTO " + self.TABLE_GLOBAL_FIREWALL + " ("+ \
                   self.ROW_GLOBAL_ID+","+ \
                   self.ROW_GLOBAL_INCOMING+","+ \
                   self.ROW_GLOBAL_OUTGOING+ \
                   ") VALUES ("+ \
                   "1,"+ \
                   "'"+GlobalFirewallInitalData.INCOMING+"',"+ \
                   "'"+GlobalFirewallInitalData.OUTGOING+"'"+ \
                   ");"
        cursor = self.conn.cursor()
        cursor.execute(sqlQuery)
        self.conn.commit()


    def selectFromGlobalFirewallTable(self):
        conn = sqlite3.connect(self.dbpath)
        conn.row_factory = self.__dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+self.TABLE_GLOBAL_FIREWALL+ " WHERE "+self.ROW_GLOBAL_ID+" = 1")
        globalConfig = cursor.fetchall()
        conn.close()
        return globalConfig


    def updateGlobalFirewallTable(self,data):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        sqlQuery = "UPDATE "+self.TABLE_GLOBAL_FIREWALL+" SET "+ \
                   self.ROW_GLOBAL_INCOMING + " = '"+ data["incoming"] + "', "+ \
                   self.ROW_GLOBAL_OUTGOING + " = '"+ data["outgoing"] +"'" \
                   +" WHERE "+self.ROW_GLOBAL_ID+" = 1"
        cursor.execute(sqlQuery)
        conn.commit()
        conn.close()





#################### MODBUS TCP IP Table ##########################

    TABLE_MODBUS_TCP_IP = 'modbus_tcp_ip'

    ROW_MODBUS_TCP_IP_ID = '_id'
    ROW_MODBUS_TCP_IP_IPADDRESS = 'ipaddress'

    def __createModbusTCPIPTable(self):
        self.conn.execute('CREATE TABLE IF NOT EXISTS '+self.TABLE_MODBUS_TCP_IP +' ('
                          + self.ROW_MODBUS_TCP_IP_ID +' INTEGER PRIMARY KEY AUTOINCREMENT,'
                          + self.ROW_MODBUS_TCP_IP_IPADDRESS +' TEXT'
                          +')')
        self.conn.commit()

    def insertIntoModbusTCPIPTable(self,data):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        sqlQuery = "INSERT INTO " + self.TABLE_MODBUS_TCP_IP + " ("+ \
                   self.ROW_MODBUS_TCP_IP_IPADDRESS+ \
                   ") VALUES ("+ \
                   "'"+data['ipaddress']+"'"+ \
                   ");"

        cursor.execute(sqlQuery)
        conn.commit()
        conn.close()
        pass

    def updateModbusTCPIPTableByID(self,id,data):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        sqlQuery = "UPDATE "+self.TABLE_MODBUS_TCP_IP+" SET "+ \
                   self.ROW_MODBUS_TCP_IP_IPADDRESS + " = '"+ data["ipaddress"] +"'" \
                   +" WHERE "+self.ROW_MODBUS_TCP_IP_ID+" = "+id
        cursor.execute(sqlQuery)
        conn.commit()
        conn.close()
        pass

    def deleteModbusTCPIPData(self,id):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM "+self.TABLE_MODBUS_TCP_IP+" WHERE "+self.ROW_MODBUS_TCP_IP_ID+" = "+id)
        conn.commit()
        conn.close()

    def selectAllFromModbusTCPIP(self):
        conn = sqlite3.connect(self.dbpath)
        conn.row_factory = self.__dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+self.TABLE_MODBUS_TCP_IP + " ORDER BY "+ self.ROW_MODBUS_TCP_IP_ID)
        modbusconfig = cursor.fetchall()
        conn.close()
        return modbusconfig

    def selectFromModbusTCPIPByID(self,id):
        conn = sqlite3.connect(self.dbpath)
        conn.row_factory = self.__dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+self.TABLE_MODBUS_TCP_IP+" WHERE "+self.ROW_MODBUS_TCP_IP_ID+" = "+id)
        modbusconfig = cursor.fetchall()
        conn.close()
        return modbusconfig





    #################### MQTT TOPIC LIST Table ##########################

    TABLE_MQTT_TOPIC_LIST = 'mqtt_topic_list'

    ROW_MQTT_TOPIC__ID = '_id'
    ROW_MQTT_TOPIC = 'topic'

    def __createMqttTopicListTable(self):
        self.conn.execute('CREATE TABLE IF NOT EXISTS '+self.TABLE_MQTT_TOPIC_LIST +' ('
                          + self.ROW_MQTT_TOPIC__ID +' INTEGER PRIMARY KEY AUTOINCREMENT,'
                          + self.ROW_MQTT_TOPIC +' TEXT'
                          +')')
        self.conn.commit()

    def insertIntoMqttTopicListTable(self,data):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        sqlQuery = "INSERT INTO " + self.TABLE_MQTT_TOPIC_LIST + " ("+ \
                   self.ROW_MQTT_TOPIC+ \
                   ") VALUES ("+ \
                   "'"+data['topic']+"'"+ \
                   ");"

        cursor.execute(sqlQuery)
        conn.commit()
        conn.close()
        pass

    def updateMqttTopicListTableByID(self,id,data):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        sqlQuery = "UPDATE "+self.TABLE_MQTT_TOPIC_LIST+" SET "+ \
                   self.ROW_MQTT_TOPIC + " = '"+ data["topic"] +"'" \
                   +" WHERE "+self.ROW_MQTT_TOPIC__ID+" = "+id
        cursor.execute(sqlQuery)
        conn.commit()
        conn.close()
        pass

    def deleteMqttTopicListData(self,id):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM "+self.TABLE_MQTT_TOPIC_LIST+" WHERE "+self.ROW_MQTT_TOPIC__ID+" = "+id)
        conn.commit()
        conn.close()

    def selectAllFromMqttTopicList(self):
        conn = sqlite3.connect(self.dbpath)
        conn.row_factory = self.__dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+self.TABLE_MQTT_TOPIC_LIST+" ORDER BY "+ self.ROW_MQTT_TOPIC__ID)
        modbusconfig = cursor.fetchall()
        conn.close()
        return modbusconfig

    def selectFromMqttTopicListByID(self,id):
        conn = sqlite3.connect(self.dbpath)
        conn.row_factory = self.__dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+self.TABLE_MQTT_TOPIC_LIST+" WHERE "+self.ROW_MQTT_TOPIC__ID+" = "+id)
        modbusconfig = cursor.fetchall()
        conn.close()
        return modbusconfig


    #################### SPECIFIC FIREWALL Table ##########################

    TABLE_SPECIFIC_FIREWALL = 'specific_firewall'

    ROW_SPECIFIC_FIREWALL_ID = '_id'
    ROW_SPECIFIC_FIREWALL_SOURCE_IP = 'source_ip'
    ROW_SPECIFIC_FIREWALL_SOURCE_PORT = 'source_port'
    ROW_SPECIFIC_FIREWALL_DESTINATION_IP = 'destination_ip'
    ROW_SPECIFIC_FIREWALL_DESTINATION_PORT = 'destination_port'
    ROW_SPECIFIC_FIREWALL_ACCESS = 'access'

    def __createSpecificFirewallTable(self):
        self.conn.execute('CREATE TABLE IF NOT EXISTS '+self.TABLE_SPECIFIC_FIREWALL +' ('
                          + self.ROW_SPECIFIC_FIREWALL_ID +' INTEGER PRIMARY KEY AUTOINCREMENT,'
                          + self.ROW_SPECIFIC_FIREWALL_SOURCE_IP +' TEXT,'
                          + self.ROW_SPECIFIC_FIREWALL_SOURCE_PORT +' INTEGER,'
                          + self.ROW_SPECIFIC_FIREWALL_DESTINATION_IP +' TEXT,'
                          + self.ROW_SPECIFIC_FIREWALL_DESTINATION_PORT +' INTEGER,'
                          + self.ROW_SPECIFIC_FIREWALL_ACCESS +' TEXT'
                          +')')
        self.conn.commit()

    def insertIntoSpecificFirewallTable(self,data):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        sqlQuery = "INSERT INTO " + self.TABLE_SPECIFIC_FIREWALL + " ("+ \
                   self.ROW_SPECIFIC_FIREWALL_SOURCE_IP+","+ \
                   self.ROW_SPECIFIC_FIREWALL_SOURCE_PORT+","+ \
                   self.ROW_SPECIFIC_FIREWALL_DESTINATION_IP+","+ \
                   self.ROW_SPECIFIC_FIREWALL_DESTINATION_PORT+","+ \
                   self.ROW_SPECIFIC_FIREWALL_ACCESS+ \
                   ") VALUES ("+ \
                   "'"+data['source_ip']+"',"+ \
                   ""+data['source_port']+","+ \
                   "'"+data['destination_ip']+"',"+ \
                   ""+data['destination_port']+","+ \
                   "'"+data['access']+"'"+ \
                   ");"

        cursor.execute(sqlQuery)
        conn.commit()
        conn.close()


    def updateSpecificFirewallTableByID(self,id,data):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        sqlQuery = "UPDATE "+self.TABLE_SPECIFIC_FIREWALL+" SET "+ \
                   self.ROW_SPECIFIC_FIREWALL_SOURCE_IP + " = '"+ data["source_ip"] + "', "+ \
                   self.ROW_SPECIFIC_FIREWALL_SOURCE_PORT + " = '"+ data["source_port"] + "', "+ \
                   self.ROW_SPECIFIC_FIREWALL_DESTINATION_IP + " = '"+ data["destination_ip"] + "', "+ \
                   self.ROW_SPECIFIC_FIREWALL_DESTINATION_PORT + " = '"+ data["destination_port"] + "', "+ \
                   self.ROW_SPECIFIC_FIREWALL_ACCESS + " = '"+ data["access"] +"'" \
                   +" WHERE "+self.ROW_SPECIFIC_FIREWALL_ID+" = "+id
        cursor.execute(sqlQuery)
        conn.commit()
        conn.close()
        pass

    def deleteSpecificFirewallData(self,id):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM "+self.TABLE_SPECIFIC_FIREWALL+" WHERE "+self.ROW_SPECIFIC_FIREWALL_ID+" = "+id)
        conn.commit()
        conn.close()

    def selectAllFromSpecificFirewall(self):
        conn = sqlite3.connect(self.dbpath)
        conn.row_factory = self.__dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+ self.TABLE_SPECIFIC_FIREWALL + " ORDER BY "+ self.ROW_SPECIFIC_FIREWALL_ID)
        modbusconfig = cursor.fetchall()
        conn.close()
        return modbusconfig

    def selectFromSpecificFirewallByID(self,id):
        conn = sqlite3.connect(self.dbpath)
        conn.row_factory = self.__dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+self.TABLE_SPECIFIC_FIREWALL+" WHERE "+self.ROW_SPECIFIC_FIREWALL_ID+" = "+id)
        modbusconfig = cursor.fetchall()
        conn.close()
        return modbusconfig

#################### ADMIN AUTH Table ##########################
    TABLE_ADMIN_AUTH_TABLE = 'admin_auth'

    ROW_ADMIN_AUTH_ID = '_id'
    ROW_ADMIN_AUTH_USER = 'username'
    ROW_ADMIN_AUTH_PASSWORD = 'password'

    def __createAdminAuthTable(self):
        self.conn.execute('CREATE TABLE IF NOT EXISTS '+self.TABLE_ADMIN_AUTH_TABLE +' ('
                          + self.ROW_ADMIN_AUTH_ID +' INTEGER PRIMARY KEY AUTOINCREMENT,'
                          + self.ROW_ADMIN_AUTH_USER +' TEXT,'
                          + self.ROW_ADMIN_AUTH_PASSWORD +' TEXT'
                          +')')
        self.conn.commit()

    def __initializeUserLoginTableData(self):
        sqlQuery = "INSERT OR IGNORE INTO " + self.TABLE_ADMIN_AUTH_TABLE + " ("+ \
                   self.ROW_ADMIN_AUTH_ID+","+ \
                   self.ROW_ADMIN_AUTH_USER+","+ \
                   self.ROW_ADMIN_AUTH_PASSWORD+ \
                   ") VALUES ("+ \
                   "1,"+ \
                   "'"+UserLogin.USERNAME+"',"+ \
                   "'"+UserLogin.PASSWORD+"'"+ \
                   ");"
        cursor = self.conn.cursor()
        cursor.execute(sqlQuery)
        self.conn.commit()

    def updateUserLoginTable(self,data):
        conn = sqlite3.connect(self.dbpath)
        cursor = conn.cursor()
        sqlQuery = "UPDATE "+self.TABLE_ADMIN_AUTH_TABLE+" SET "+ \
                   self.ROW_ADMIN_AUTH_USER + " = '"+ data["username"] + "', "+ \
                   self.ROW_ADMIN_AUTH_PASSWORD + " = '"+ data["password"] +"'" \
                   +" WHERE "+self.ROW_ADMIN_AUTH_ID+" = 1"
        cursor.execute(sqlQuery)
        conn.commit()
        conn.close()

    def selectFromUserLoginTable(self):
        conn = sqlite3.connect(self.dbpath)
        conn.row_factory = self.__dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+self.TABLE_ADMIN_AUTH_TABLE+ " WHERE "+self.ROW_ADMIN_AUTH_ID+" = 1")
        userlogin = cursor.fetchall()
        conn.close()
        return userlogin

    def selectFromUserLoginTableByID(self,id):
        conn = sqlite3.connect(self.dbpath)
        conn.row_factory = self.__dict_factory
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM "+self.TABLE_ADMIN_AUTH_TABLE+ " WHERE "+self.ROW_ADMIN_AUTH_ID+" = "+id)
        userlogin = cursor.fetchall()
        conn.close()
        return userlogin
