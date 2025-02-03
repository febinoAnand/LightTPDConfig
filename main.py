import os

from flask import Flask, render_template, request, redirect,session, flash,url_for
from DatabaseManager import DatabaseManager
from FileGenerator import ConfigFileGenerator
from InitialData.FileName import ConfigFileName
import sys

configFolderLocation = ""
configFileGenerator = ""
db = ""

def validateFilePath(path):
    testfilePath = os.path.join(path,"testfile.txt")
    testFile = open(testfilePath,'w')
    testFile.write("testing..")
    testFile.close()
    os.remove(testfilePath)

try:
    configFolderLocation = sys.argv[1]
    validateFilePath(configFolderLocation)
    configFileGenerator = ConfigFileGenerator(configFolderLocation)
    db = DatabaseManager(configFolderLocation)
except Exception as e:
    print (e)
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
    return render_template('login/changepasswordview.html',username=username)

@app.route('/changeauth',methods=['POST'])
def changeauth():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")

    data = request.form.to_dict()
    username = db.selectFromUserLoginTable()[0]['username']
    if request.method == 'POST':
        if data['password'] == '' or data['confirmpassword'] == '':
            return render_template('login/changepasswordview.html', username = username, errormessage = "Input Should not be empty")
        elif data['password'] != data['confirmpassword']:
            return render_template('login/changepasswordview.html', username = username, errormessage = "Confirm Password mismatch")

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
            return render_template("tagconfig/tagconfigform.html",tagconfigdata = tagconfigdata, modbustcpdropdown = modbustcpdropdown, mqtttopicdropdown = mqtttopicdropdown)
        except Exception as e:
            print(e)
    return render_template("tagconfig/tagconfigform.html", tagconfigdata="", modbustcpdropdown = modbustcpdropdown, mqtttopicdropdown = mqtttopicdropdown)

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
    return render_template("tagconfig/tagconfig.html",tagconfigdata = tagConfigData)


@app.route("/tagconfigdetails",methods=['POST'])
def tagconfigdetails():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    if request.method == 'POST':

        id = request.args.get("id")
        data = request.form.to_dict()
        data = {i:'0' if not j else j for i,j in data.items()}

        isTagExist = ""
        try:
            count = db.getCountTagConfig()
            isTagExist = db.selectFromTagConfigByName(data['tag_name'])[0]
        except Exception as e:
            print(e)

        if not id:
            if count >= 1000:
                msg = "Exceed Limit....!!! Already 1000 Tag was added. Cant able to add Tags"
            elif not isTagExist:
                db.insertIntoTagConfigTable(data)
                msg = "Success....!!!Tag Name : "+data["tag_name"]+" was added"
            else:
                msg = "Duplicate....!!!Tag Name : "+data["tag_name"]+" was already Exist"
        else:
            if not isTagExist:
                db.updateTagConfigTableByID(id,data)
                msg = "Success....!!!Tag Name : "+data["tag_name"]+"  was updated"
            elif id == str(isTagExist["_id"]):
                db.updateTagConfigTableByID(id,data)
                msg = "Success....!!!Tag Name : "+data["tag_name"]+"  was updated"
            else:
                msg = "Duplicate....!!!Tag Name : "+data["tag_name"]+"  was alreadyasdf Exist"

    return alertAndRedirect(msg,'/tagconfig')


@app.route("/generatetagconfigfile")
def generatetagconfigfile():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.TAG_CONFIG_FILE)
    return alertAndRedirect("Success....!!!Tag Config file was generated","/tagconfig")








################ Server Config Routes ########################

@app.route("/serverconfig")
def serverconfig():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    try:
        serverconfigdata = db.selectFromServerConfigTable()[0]
        return render_template("serverconfig/serverconfigform.html", configdata = serverconfigdata)
    except Exception as e:
        print (e)

    return render_template("serverconfig/serverconfigform.html", configdata = "")

@app.route("/updateserverdetails",methods=["POST"])
def updateserverconfig():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    if request.method == 'POST':
        serverconfigdata = request.form.to_dict()
        db.updateServerConfigTable(serverconfigdata)
    return alertAndRedirect("Success....!!!Server details updated","/serverconfig")


@app.route("/generateserverdetailsfile")
def generateserverdetailsfile():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.SERVER_CONFIG_FILE)
    return alertAndRedirect("Success....!!!Server config file was generated","/serverconfig")


################ IP Config Routes ########################

@app.route("/ipconfig")
def ipconfig():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    try:
        ipconfigdata = db.selectFromIPConfigTable()[0]
        return render_template("ipaddress/ipconfigform.html", configdata = ipconfigdata)
    except Exception as e:
        print (e)

    return render_template("ipaddress/ipconfigform.html", configdata = "")

@app.route("/updateipdetails",methods=["POST"])
def updateipconfig():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    if request.method == 'POST':
        ipconfigdata = request.form.to_dict()
        db.updateIPConfigTable(ipconfigdata)
    return alertAndRedirect("Success....!!!IP details updated","/ipconfig")


@app.route("/generateipdetailsfile")
def generateipdetailsfile():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.IP_CONFIG_FILE)
    return alertAndRedirect("Success....!!!IP config file was generated","/ipconfig")





################ MQTT Topic Routes ########################

@app.route("/mqtttopic")
def mqtttopic():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    data = db.selectAllFromMqttTopicList()
    return render_template("mqtttopic/mqtttopictable.html",configdata = data)


@app.route("/mqtttopicview")
def mqtttopicview():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    id = request.args.get('id')
    if id:
        try:
            data = db.selectFromMqttTopicListByID(id)[0]
            return render_template("mqtttopic/mqtttopicform.html",configdata = data)
        except Exception as e:
            print(e)
    return render_template("mqtttopic/mqtttopicform.html",configdata = "")

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

        id = request.args.get("id")
        data = request.form.to_dict()
        if not id:
            db.insertIntoMqttTopicListTable(data)
            msg = "Success....!!! MQTT topic was created"
        else:
            db.updateMqttTopicListTableByID(id,data)
            msg = "Success....!!! MQTT topic was updated"

    return alertAndRedirect(msg,"/mqtttopic")

@app.route("/generatemqttconfigfile")
def generatemqttconfigfile():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.MQTT_TOPIC_CONFIG_FILE)
    return alertAndRedirect("Success....!!! MQTT Topic file was generated","/mqtttopic")




################ MODBUS TCP IP Routes ########################

@app.route("/modbustcp")
def modbustcp():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    data = db.selectAllFromModbusTCPIP()
    return render_template("modbustcp/modbustcptable.html",configdata = data)

@app.route("/modbustcpview")
def modbustcpview():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    id = request.args.get('id')
    if id:
        try:
            data = db.selectFromModbusTCPIPByID(id)[0]
            return render_template("modbustcp/modbustcpform.html",configdata= data)
        except Exception as e:
            print(e)
    return render_template("modbustcp/modbustcpform.html",configdata= "")

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

        id = request.args.get("id")
        data = request.form.to_dict()
        if not id:
            db.insertIntoModbusTCPIPTable(data)
            msg = "Success....!!! IP address was Added"
        else:
            db.updateModbusTCPIPTableByID(id,data)
            msg = "Success....!!! IP address was Updated"

    return alertAndRedirect(msg,"/modbustcp")

@app.route("/generatemodbustcpipconfigfile")
def generatemodbustcpipconfigfile():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.MODBUS_TCP_IP_CONFIG_FILE)
    return alertAndRedirect("Success....!!! MODBUS TCP IP file was generated","/modbustcp")






################ Specific Firewall Config Routes ########################

@app.route("/specificfirewall")
def specificfirewall():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    data = db.selectAllFromSpecificFirewall()
    return render_template("firewall/specificfirewalltable.html",configdata = data)

@app.route("/specificfirewallview")
def specificfirewallview():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    id = request.args.get('id')
    if id:
        try:
            data = db.selectFromSpecificFirewallByID(id)[0]
            return render_template("firewall/specificfirewallform.html",configdata=data)
        except Exception as e:
            print(e)
    return render_template("firewall/specificfirewallform.html",configdata='')


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
        id = request.args.get("id")
        data = request.form.to_dict()
        data = {i:'0' if not j else j for i,j in data.items()}
        if not id:
            db.insertIntoSpecificFirewallTable(data)
            msg = "Success....!!! Firewall created"
        else:
            db.updateSpecificFirewallTableByID(id,data)
            msg = "Success....!!! Firewall updated"
    return alertAndRedirect(msg,"/specificfirewall")

@app.route("/generatespecificconfigfile")
def generatespecificconfigfile():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.SPECIFIC_FIREWALL_CONFIG_FILE)
    return alertAndRedirect("Success....!!! Specific firewall file was updated","/specificfirewall")




################ Global Firewall Config Routes ########################

@app.route("/globalfirewall")
def globalfirewall():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    try:
        data = db.selectFromGlobalFirewallTable()[0]
        return render_template("firewall/globalfirewallform.html", configdata= data)
    except Exception as e:
        print(e)
    return render_template("firewall/globalfirewallform.html", configdata= "")

@app.route("/updateglobalfirewall",methods=["POST"])
def updateglobalfirewall():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    if request.method == 'POST':
        globalFirewallData = request.form.to_dict()
        # print (globalFirewallData)
        db.updateGlobalFirewallTable(globalFirewallData)
    return alertAndRedirect("Firewall updated","/globalfirewall")

@app.route("/generateglobalfirewall")
def generateglobalfirewall():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.GLOBAL_FIREWALL_CONFIG_FILE)
    return alertAndRedirect("Success....!!!Global firewall config file was generated","/globalfirewall")






################ Wifi Config Routes ########################

@app.route("/wifisetting")
def wifisetting():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    try:
        wificonfigdata = db.selectFromWifiSettingTable()[0]
        return render_template("wifisettings/wifisettingsform.html",configdata = wificonfigdata)
    except Exception as e:
        print(e)

    return render_template("wifisettings/wifisettingsform.html" , configdata = "")

@app.route("/updatewifisetting",methods=["POST"])
def updatewifisetting():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    if request.method == "POST":
        wifisettingdata = request.form.to_dict()
        db.updateWifiSettingTable(wifisettingdata)
    return alertAndRedirect("Success....!!! WIFI setting was updated","/wifisetting")

@app.route("/generatewifisettingfile")
def generetewififile():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    configFileGenerator.generateFile(ConfigFileGenerator.WIFI_CONFIG_FILE)
    return alertAndRedirect("WIFI Config file was generated","/wifisetting")

################ About ########################
@app.route("/about")
def about():
    if checksession() == 0:
        return render_template('login/login.html',errormessage = "Session Expired")
    file = []
    try:
        about_file_path = os.path.join(configFolderLocation,ConfigFileName.aboutFileName)
        about_file = open(about_file_path,'r')
        file_data = about_file.read().split('\n')
        for unsplitData in file_data:
            file.append(unsplitData.split(','))
    except Exception as e:
        print (e)
        file = [["Error","Can't read the file. Kindly Check file format"]]
    return render_template('about/aboutview.html',file=file)

################ Utility ########################

def alertAndRedirect(message,redirect_to):
    return "<script>alert('"+message+"'); window.location = '"+redirect_to+"'; </script>"

if __name__ == "__main__":
    app.secret_key = "akjshdgfk2j3rg23h123ufg8723hfkjuh817232f8237da"
    app.run(debug=False,use_reloader=False,host="0.0.0.0")
