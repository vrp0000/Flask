from flask import Flask,redirect,url_for,request
from _datetime import datetime
app =  Flask(__name__)
@app.route('/paymentprocess',methods = ['POST'])
#/<CreditCardNumber>/<CardHolder>/<float:Amount>/<ExpirationDate>')
def PocessPayment():

    #==================Intialisers as per data-type
    cardno = int(request.form['CreditCardNumber'])
    holder =request.form['CardHolder']
    expdate = datetime.strptime((request.form['ExpirationDate']),'%Y-%m-%d')
    amount = int(request.form['Amount'])
    pin = request.form['SecurityCode']
    validity =1
    status =0
    #=============Check for Validity

    if ((amount > 0) and (len(str(cardno)) == 16) and (isinstance(holder,str)) and (holder != '')) :
        validity = 1
        for character in holder:
            if character.isdigit():
                validity = 0
                break

    else :
        validity = 0
        status = 0

    #=============Payment Gateway based on Amount
    if(validity == 1):
        if amount<=20 :
            status = ChealPaymentGateway()
        elif amount>=21 or amount <=500:
            status = ExpensivePaymentGateway()
            if status !=1 :
                ChealPaymentGateway()
        elif amount>500:
            for i in range (3):
                status = redirPremiumPaymentGateway()
                if status ==1 :
                    break

    #===============Method Return Based on payment Status
    if status ==1 :
        return '200 OK'
    elif (validity ==0 ):
        return '400 Bad Request'
    else :
        return '500 Internal Server Error'

#====================Defining Payment Gateway for self testing
def PremiumPaymentGateway():
    return 1
def ExpensivePaymentGateway():
    return 1
def ChealPaymentGateway():
    return 1
@app.route('/hello')
def hello():
    return 'Hello World'
#app.add_url_rule('/', 'hello', hello)

if __name__ == '__main__':
    app.run(debug=True)