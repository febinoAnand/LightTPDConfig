import os

from flask import Flask, render_template, request, redirect,session
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


@app.route("/auth",methods=['post'])
def auth():
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            userdata = db.selectFromUserLoginTable()[0]
        except Exception as e:
            print (e)
            return redirect('/')

        if userdata['username'] == data['username'] and userdata['password'] == data['password']:
            session['userid'] = userdata['_id']
            session['username'] = userdata['username']
            return redirect('/tagconfig')
        return render_template("login/login.html",errormessage = "Login Credential is wrong")

@app.route('/changepassword')
def changepassword():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    username = db.selectFromUserLoginTable()[0]['username']
    return render_template('login/changepassword.html',username=username)

@app.route('/changeauth',methods=['POST'])
def changeauth():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")

    data = request.form.to_dict()
    username = db.selectFromUserLoginTable()[0]['username']
    if request.method == 'POST':
        if data['password'] == '' or data['confirmpassword'] == '':
            return render_template('login/changepassword.html', username = username, errormessage = "Input Should not be empty")
        elif data['password'] != data['confirmpassword']:
            return render_template('login/changepassword.html', username = username, errormessage = "Confirm Password mismatch")

        session.pop('username')
        session.pop('userid')
        db.updateUserLoginTable(data)
        return render_template('login/login.html', errormessage = "Password changed. Login Again")

    return render_template('login/login.html',errormessage = "Not Valid input")


@app.route('/logout')
def logout():
    try:
        session.pop('username')
        session.pop('userid')
    except Exception as e:
        pass
    return redirect('/')

def usercheck(userid,username):
    try:
        data = db.selectFromUserLoginTableByID(userid)[0]
        if data['username'] == username:
            return 1
    except Exception as e:
        return 0
    return 0

def checksession():
    try:
        userid = session.get('userid')
        username = session.get('username')
        data = db.selectFromUserLoginTableByID(str(userid))[0]
        if data['username'] == username:
            return 1
    except Exception as e:
        print(e)
        return 0
    return 0


################ Tag Config Routes ########################


@app.route("/tagconfigview")
def tagconfigview():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
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
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    tagConfigData = db.selectAllFromTagConfig()
    return render_template("tagconfig/tagconfiglist.html",tagconfigdata = tagConfigData)


@app.route("/tagconfigdetails",methods=['POST'])
def tagconfigdetails():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
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
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.TAG_CONFIG_FILE)
    return redirect("/tagconfig")








################ Server Config Routes ########################

@app.route("/serverconfig")
def serverconfig():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    try:
        serverconfigdata = db.selectFromServerConfigTable()[0]
        return render_template("serverconfig/serverconfigview.html", configdata = serverconfigdata)
    except Exception as e:
        print (e)

    return render_template("serverconfig/serverconfigview.html", configdata = "")

@app.route("/updateserverdetails",methods=["POST"])
def updateserverconfig():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    if request.method == 'POST':
        serverconfigdata = request.form.to_dict()
        db.updateServerConfigTable(serverconfigdata)

    return redirect("/serverconfig")


@app.route("/generateserverdetailsfile")
def generateserverdetailsfile():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.SERVER_CONFIG_FILE)
    return redirect("/serverconfig")





################ MQTT Topic Routes ########################

@app.route("/mqtttopic")
def mqtttopic():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    data = db.selectAllFromMqttTopicList()
    return render_template("mqtttopic/mqtttopiclist.html",configdata = data)


@app.route("/mqtttopicview")
def mqtttopicview():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
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
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    id = request.args.get("id")
    if id:
        db.deleteMqttTopicListData(id)
    return redirect('/mqtttopic')

@app.route("/mqtttopicconfig",methods=['POST'])
def mqtttopicconfig():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
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
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.MQTT_TOPIC_CONFIG_FILE)
    return redirect("/mqtttopic")




################ MODBUS TCP IP Routes ########################

@app.route("/modbustcp")
def modbustcp():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    data = db.selectAllFromModbusTCPIP()
    return render_template("modbustcp/modbustcplist.html",configdata = data)

@app.route("/modbustcpview")
def modbustcpview():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
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
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    id = request.args.get("id")
    if id:
        db.deleteModbusTCPIPData(id)
    return redirect('/modbustcp')

@app.route("/modbustcpipconfig",methods=['POST'])
def modbustcpipconfig():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
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
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.MODBUS_TCP_IP_CONFIG_FILE)
    return redirect("/modbustcp")






################ Specific Firewall Config Routes ########################

@app.route("/specificfirewall")
def specificfirewall():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    data = db.selectAllFromSpecificFirewall()
    return render_template("firewall/specificfirewall.html",configdata = data)

@app.route("/specificfirewallview")
def specificfirewallview():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
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
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    id = request.args.get("id")
    if id:
        db.deleteSpecificFirewallData(id)
    return redirect("/specificfirewall")

@app.route("/specificfirewallconfig",methods=['POST'])
def specificfirewallconfig():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
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
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.SPECIFIC_FIREWALL_CONFIG_FILE)
    return redirect("/specificfirewall")




################ Global Firewall Config Routes ########################

@app.route("/globalfirewall")
def globalfirewall():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    try:
        data = db.selectFromGlobalFirewallTable()[0]
        return render_template("firewall/globalfirewall.html", configdata= data)
    except Exception as e:
        print(e)
    return render_template("firewall/globalfirewall.html", configdata= "")

@app.route("/updateglobalfirewall",methods=["POST"])
def updateglobalfirewall():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    if request.method == 'POST':
        globalFirewallData = request.form.to_dict()
        db.updateGlobalFirewallTable(globalFirewallData)
    return redirect("/globalfirewall")

@app.route("/generateglobalfirewall")
def generateglobalfirewall():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.GLOBAL_FIREWALL_CONFIG_FILE)
    return redirect("/globalfirewall")






################ Wifi Config Routes ########################

@app.route("/wifisetting")
def wifisetting():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    try:
        wificonfigdata = db.selectFromWifiSettingTable()[0]
        return render_template("wifisettings/wifisettings.html",configdata = wificonfigdata)
    except Exception as e:
        print(e)

    return render_template("wifisettings/wifisettings.html" , configdata = "")

@app.route("/updatewifisetting",methods=["POST"])
def updatewifisetting():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    if request.method == "POST":
        wifisettingdata = request.form.to_dict()
        db.updateWifiSettingTable(wifisettingdata)
    return redirect("/wifisetting")

@app.route("/generatewifisettingfile")
def generetewififile():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.WIFI_CONFIG_FILE)
    return redirect("/wifisetting")




if __name__ == "__main__":
    app.secret_key = "akjshdgfk2j3rg23h123ufg8723hfkjuh817232f8237da"
    app.run(debug=True)
