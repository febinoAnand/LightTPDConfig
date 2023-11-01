from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("login/login.html")


@app.route("/tagconfigview")
def tagconfigview():
    return render_template("tagconfig/tagconfigview.html")


@app.route("/tagconfig")
def tagconfig():
    return render_template("tagconfig/tagconfigtable.html")

@app.route("/mqtttopic")
def mqtttopic():
    return render_template("mqtttopic/mqtttopiclist.html")


@app.route("/mqtttopicview")
def mqtttopicview():
    return render_template("mqtttopic/mqtttopicview.html")

@app.route("/modbustcp")
def modbustcp():
    return render_template("modbustcp/modbustcplist.html")

@app.route("/modbustcpview")
def modbustcpview():
    return render_template("modbustcp/modbustcpview.html")



@app.route("/specificfirewall")
def specificfirewall():
    return render_template("firewall/specificfirewall.html")

@app.route("/specificfirewallview")
def specificfirewallview():
    return render_template("firewall/specificfirewallview.html")


@app.route("/globalfirewall")
def globalfirewall():
    return render_template("firewall/globalfirewall.html")

@app.route("/serverconfig")
def serverconfig():
    return render_template("serverconfig/serverconfigview.html")


@app.route("/wifisetting")
def wifisetting():
    return render_template("wifisettings/wifisettings.html")




if __name__ == "__main__":
    app.run(debug=True)
