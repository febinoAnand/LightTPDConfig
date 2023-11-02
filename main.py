import os

from flask import Flask, render_template, request, redirect
from DatabaseManager import DatabaseManager
from FileGenerator import ConfigFileGenerator
import sys

configFolderLocation = ""
configFileGenerator = ""
db = ""

def validateFilePath():
    testfilePath = os.path.join(configFolderLocation,"testfile.txt")
    testFile = open(testfilePath,'w')
    testFile.write("testing..")
    testFile.close()
    os.remove(testfilePath)

try:
    configFolderLocation = sys.argv[1]
    validateFilePath()
    configFileGenerator = ConfigFileGenerator(configFolderLocation)
    db = DatabaseManager(configFolderLocation)
except:
    print ("Kindly give correct absolute path")
    sys.exit(1)



app = Flask(__name__)

@app.route("/")
def home():
    return render_template("login/login.html")




################ Tag Config Routes ########################

@app.route("/tagconfigview")
def tagconfigview():
    id = request.args.get('id')
    modbustcpdropdown = db.selectAllFromModbusTCPIP()
    mqtttopicdropdown = db.selectAllFromMqttTopicList()
    if id:
        try:
            tagconfigdata = db.selectFromTagConfigByID(id)[0]
            return render_template("tagconfig/tagconfigview.html",tagconfigdata = tagconfigdata, modbustcpdropdown = modbustcpdropdown, mqtttopicdropdown = mqtttopicdropdown)
        except Exception as e:
            print(e)
    return render_template("tagconfig/tagconfigview.html", tagconfigdata="", modbustcpdropdown = modbustcpdropdown, mqtttopicdropdown = mqtttopicdropdown)

@app.route("/deletetagconfig")
def deletetagconfig():
    id = request.args.get("id")
    if id:
        db.deleteTagConfig(id)
    return redirect('/tagconfig')


@app.route("/tagconfig")
def tagconfig():
    tagConfigData = db.selectAllFromTagConfig()
    return render_template("tagconfig/tagconfigtable.html",tagconfigdata = tagConfigData)


@app.route("/tagconfigdetails",methods=['POST'])
def tagconfigdetails():
    if request.method == 'POST':
        #TODO validate the data
        id = request.args.get("id")
        data = request.form.to_dict()
        if not id:
            db.insertIntoTagConfigTable(data)
        else:
            db.updateTagConfigTableByID(id,data)
    return redirect("/tagconfig")

@app.route("/generatetagconfigfile")
def generatetagconfigfile():
    configFileGenerator.generateFile(ConfigFileGenerator.TAG_CONFIG_FILE)
    return redirect("/tagconfig")





################ Server Config Routes ########################

@app.route("/serverconfig")
def serverconfig():
    try:
        serverconfigdata = db.selectFromServerConfigTable()[0]
        return render_template("serverconfig/serverconfigview.html", configdata = serverconfigdata)
    except Exception as e:
        print (e)

    return render_template("serverconfig/serverconfigview.html", configdata = "")

@app.route("/updateserverdetails",methods=["POST"])
def updateserverconfig():
    if request.method == 'POST':
        serverconfigdata = request.form.to_dict()
        db.updateServerConfigTable(serverconfigdata)

    return redirect("/serverconfig")


@app.route("/generateserverdetailsfile")
def generateserverdetailsfile():
    configFileGenerator.generateFile(ConfigFileGenerator.SERVER_CONFIG_FILE)
    return redirect("/serverconfig")





################ MQTT Topic Routes ########################

@app.route("/mqtttopic")
def mqtttopic():
    data = db.selectAllFromMqttTopicList()
    return render_template("mqtttopic/mqtttopiclist.html",configdata = data)


@app.route("/mqtttopicview")
def mqtttopicview():
    id = request.args.get('id')
    if id:
        try:
            data = db.selectFromMqttTopicListByID(id)[0]
            return render_template("mqtttopic/mqtttopicview.html",configdata = data)
        except Exception as e:
            print(e)
    return render_template("mqtttopic/mqtttopicview.html",configdata = "")

@app.route("/deletemqttconfig")
def deletemqttconfig():
    id = request.args.get("id")
    if id:
        db.deleteMqttTopicListData(id)
    return redirect('/mqtttopic')

@app.route("/mqtttopicconfig",methods=['POST'])
def mqtttopicconfig():
    if request.method == 'POST':
        #TODO validate the data
        id = request.args.get("id")
        data = request.form.to_dict()
        if not id:
            db.insertIntoMqttTopicListTable(data)
        else:
            db.updateMqttTopicListTableByID(id,data)
    return redirect("/mqtttopic")

@app.route("/generatemqttconfigfile")
def generatemqttconfigfile():
    configFileGenerator.generateFile(ConfigFileGenerator.MQTT_TOPIC_CONFIG_FILE)
    return redirect("/mqtttopic")




################ MODBUS TCP IP Routes ########################

@app.route("/modbustcp")
def modbustcp():
    data = db.selectAllFromModbusTCPIP()
    return render_template("modbustcp/modbustcplist.html",configdata = data)

@app.route("/modbustcpview")
def modbustcpview():
    id = request.args.get('id')
    if id:
        try:
            data = db.selectFromModbusTCPIPByID(id)[0]
            return render_template("modbustcp/modbustcpview.html",configdata= data)
        except Exception as e:
            print(e)
    return render_template("modbustcp/modbustcpview.html",configdata= "")

@app.route("/deletemodbustcoipview")
def deletemodbustcoipview():
    id = request.args.get("id")
    if id:
        db.deleteModbusTCPIPData(id)
    return redirect('/modbustcp')

@app.route("/modbustcpipconfig",methods=['POST'])
def modbustcpipconfig():
    if request.method == 'POST':
        #TODO validate the data
        id = request.args.get("id")
        data = request.form.to_dict()
        if not id:
            db.insertIntoModbusTCPIPTable(data)
        else:
            db.updateModbusTCPIPTableByID(id,data)
    return redirect("/modbustcp")

@app.route("/generatemodbustcpipconfigfile")
def generatemodbustcpipconfigfile():
    configFileGenerator.generateFile(ConfigFileGenerator.MODBUS_TCP_IP_CONFIG_FILE)
    return redirect("/modbustcp")






################ Specific Firewall Config Routes ########################

@app.route("/specificfirewall")
def specificfirewall():
    data = db.selectAllFromSpecificFirewall()
    return render_template("firewall/specificfirewall.html",configdata = data)

@app.route("/specificfirewallview")
def specificfirewallview():
    id = request.args.get('id')
    if id:
        try:
            data = db.selectFromSpecificFirewallByID(id)[0]
            return render_template("firewall/specificfirewallview.html",configdata=data)
        except Exception as e:
            print(e)
    return render_template("firewall/specificfirewallview.html",configdata='')


@app.route("/deletespecificfirewalldata")
def deletespecificfirewalldata():
    id = request.args.get("id")
    if id:
        db.deleteSpecificFirewallData(id)
    return redirect("/specificfirewall")

@app.route("/specificfirewallconfig",methods=['POST'])
def specificfirewallconfig():
    if request.method == 'POST':
        #TODO validate the data
        id = request.args.get("id")
        data = request.form.to_dict()
        if not id:
            db.insertIntoSpecificFirewallTable(data)
        else:
            db.updateSpecificFirewallTableByID(id,data)
    return redirect("/specificfirewall")

@app.route("/generatespecificconfigfile")
def generatespecificconfigfile():
    configFileGenerator.generateFile(ConfigFileGenerator.SPECIFIC_FIREWALL_CONFIG_FILE)
    return redirect("/specificfirewall")




################ Global Firewall Config Routes ########################

@app.route("/globalfirewall")
def globalfirewall():
    try:
        data = db.selectFromGlobalFirewallTable()[0]
        return render_template("firewall/globalfirewall.html", configdata= data)
    except Exception as e:
        print(e)
    return render_template("firewall/globalfirewall.html", configdata= "")

@app.route("/updateglobalfirewall",methods=["POST"])
def updateglobalfirewall():
    if request.method == 'POST':
        globalFirewallData = request.form.to_dict()
        db.updateGlobalFirewallTable(globalFirewallData)
    return redirect("/globalfirewall")

@app.route("/generateglobalfirewall")
def generateglobalfirewall():
    configFileGenerator.generateFile(ConfigFileGenerator.GLOBAL_FIREWALL_CONFIG_FILE)
    return redirect("/globalfirewall")






################ Wifi Config Routes ########################

@app.route("/wifisetting")
def wifisetting():
    try:
        wificonfigdata = db.selectFromWifiSettingTable()[0]
        return render_template("wifisettings/wifisettings.html",configdata = wificonfigdata)
    except Exception as e:
        print(e)

    return render_template("wifisettings/wifisettings.html" , configdata = "")

@app.route("/updatewifisetting",methods=["POST"])
def updatewifisetting():
    if request.method == "POST":
        wifisettingdata = request.form.to_dict()
        db.updateWifiSettingTable(wifisettingdata)
    return redirect("/wifisetting")

@app.route("/generatewifisettingfile")
def generetewififile():
    configFileGenerator.generateFile(ConfigFileGenerator.WIFI_CONFIG_FILE)
    return redirect("/wifisetting")




if __name__ == "__main__":
    app.run(debug=True)
