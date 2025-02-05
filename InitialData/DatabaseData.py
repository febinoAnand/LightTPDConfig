class DBconnent:
    dbName = "config.db"
    username = ""
    password = ""

class ServerInitalData:
    PROTOCOL="MQTT"
    URL=""
    PORT=0
    QOS=1
    USERNAME="user"
    USERPASS="pass"
    CLIENTID="client_I"
    KEEPALIVESEC=0
    SECURETOKEN = "2aa98d2b-7e3d-48ce-8fd9-2330a3489afa"

class WIFISettingInitialData:
    SSID = "ssid"
    PASSWORD = "pass"

class GlobalFirewallInitalData:
    INCOMING = 'DENY'
    OUTGOING = 'ALLOW'

class UserLogin:
    USERNAME = 'admin'
    PASSWORD = 'admin'

class IPConfigInitalData:
    IPADDRESS="192.168.3.11"
    SUBNET="255.255.255.0"
    DEFAULTGATEWAY=""

class UARTConfigInitalData:
    BAUDRATE=110
    PARITY="None"
    DATABITS=8
    STOPBITS=8