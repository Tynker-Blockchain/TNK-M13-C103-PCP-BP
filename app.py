from flask import Flask, render_template, request, redirect, jsonify
import os
from time import time
from wallet import Account, Wallet
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
from flask_cors import CORS

def firebaseInitialization():
    cred = credentials.Certificate("config/serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://blockchain-wallet-a2812-default-rtdb.firebaseio.com'})
    print("🔥🔥🔥🔥🔥 Firebase Connected! 🔥🔥🔥🔥🔥")

firebaseInitialization()

STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)
app.use_static_for_root = True

ref = db.reference('adminAccount/')
account= ref.get()
if(not account):
    account = Account()

myWallet =  Wallet()

receiverAddress = None
tnxAmount =None
id=None

# Create variable payment status


@app.route("/", methods= ["GET", "POST"])
def index():
    global account, myWallet, receiverAddress, tnxAmount
      
    isConnected = myWallet.checkConnection()
    balance = "No Balance"
    transactions={    }
    address = None
    if(account):
        if(type(account)==dict):
            balance = myWallet.getBalance(account['address'])
            transactions = myWallet.getTransactions(account['address'])
            address= account['address']
        else:
            balance = myWallet.getBalance(account.address)
            transactions = myWallet.getTransactions(account.address)
            address= account.address
    
    amountList = []
    colorList=[]
    indicesTransactions = []

    reverseTransactions = transactions[::-1]

    for index, transaction in enumerate(reverseTransactions):
        
        colorList.append("red" if transaction["from"] == address else "blue")
        amountList.append(float(transaction["amount"]))
        indicesTransactions.append(index)
        
    traceTnx = {
        'x': indicesTransactions,
        'y': amountList,
        'name': 'Amount',
        'type': 'bar',
        'marker': { 'color' : colorList }
    }

    layoutTnx = {
        'title': 'Transaction History',
        'xaxis': { 'title': 'Transaction Index' },
        'yaxis': { 'title': 'Amount(ETH)' }
    }

    transactionData ={
            'trace': [traceTnx], 
            'layout': layoutTnx
            }
    
    transactionData = json.dumps(transactionData)

    return render_template('index.html', isConnected=isConnected,  
                           account= account, balance = balance, 
                           transactionData = transactionData,
                           receiverAddress = receiverAddress, 
                           tnxAmount= tnxAmount)

   
@app.route('/transactions')
def transactions():
    global account, myWallet    
    transactions = None
    if(type(account)==dict):
         transactions = myWallet.getTransactions(account['address'])
    else:
         transactions = myWallet.getTransactions(account.address)

    return render_template('transactions.html', account=account, transactions= transactions)

@app.route("/makeTransaction", methods = ["GET", "POST"])
def makeTransaction():
    # Access paymentStatus as tnxAmount, paymentStatus, global
    global myWallet, account, id

    senderType = 'ganache'
    accountAddress = None
    privateKey = None
    if(type(account)==dict):
        accountAddress = account['address']
        privateKey = account['privateKey']
    else:
        accountAddress = account.address
        privateKey = account.privateKey

    sender =accountAddress
    receiver = request.form.get("receiverAddress")
    amount = request.form.get("amount")

    if(sender == accountAddress):
        senderType = 'newAccountAddress'

    tnxHash= myWallet.makeTransactions(sender, receiver, amount, senderType, privateKey)
    myWallet.addTransactionHash(tnxHash, sender, receiver, amount)
    
    # Check is receiverAddress not none
    
        # Set receiverAddress to None
        
        # Set tnxAmount to None
        
        # Set paymentStatus to true

    return redirect("/")

@app.route('/payment')
def payment():
    global receiverAddress, tnxAmount, id
    receiverAddress = request.args.get("address")
    tnxAmount = int(request.args.get("amount"))/100000
    id = request.args.get("id")

    return redirect('/')


@app.route('/checkPaymentStatus')
def checkPaymentStatus():
    # Access paymentStatus as global
    
    # Check if paymentStatus is True
    
        # Set paymentStatus to False
        
        #Return JSON true, id
    
    # Pass paymentStatus as response instead of True
    return jsonify(True)

if __name__ == '__main__':
    app.run(debug = True, port=4000)
