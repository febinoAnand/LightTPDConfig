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

class WIFISettingInitialData:
    SSID = "ssid"
    PASSWORD = "pass"

class GlobalFirewallInitalData:
    INCOMING = 'DENY'
    OUTGOING = 'ALLOW'

class UserLogin:
    USERNAME = 'admin'
    PASSWORD = 'admin'