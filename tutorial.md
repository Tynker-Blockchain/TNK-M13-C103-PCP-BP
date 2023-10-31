Refund Confirmation
==================


In this activity, you will learn to refund the amount to the account address that has made the payment.


<img src= "https://s3.amazonaws.com/media-p.slid.es/uploads/1525749/images/10787573/PCP.gif" width = "480" height = "320">


Follow the given steps to complete this activity:




1. Create a Payment Status


* Open the file `app.py`.


* Create a variable to keep track of the payments.
~~~python
paymentStatus = None
~~~


2. Set Payment Status to True After Making the Transaction


* Access the global variables `receiverAddress, tnxAmount, paymentStatus` in the `makeTransaction` function definition.
~~~python
global myWallet, account, receiverAddress, tnxAmount, paymentStatus
~~~
* Reset the receiver address, transaction amount to `None`, and the payment status to `True` after the transaction is made.
~~~python
if(receiverAddress):
        receiverAddress = None
        tnxAmount = None
        paymentStatus = True


~~~


3. Send the Payment Confirmation
* Reset the payment status to `None` after the payment status respose is sent to the request.
* Access the global variable `paymentStatus` and `id` in the `checkPaymentStatus` function definition.
~~~python
global paymentStatus, id
~~~
* Check if the payment status is `True` and reset the payment status to `False`. Send the response as a list of status and id.
~~~python
    if paymentStatus == True:
        paymentStatus = False
        return jsonify([True, id])
~~~
* Send the payment status if the payment status is not `True`.
~~~python
return jsonify(paymentStatus)
~~~
* Open the file `wait.html`.
* Receive the response from the payment gateway and print it on the console.
~~~sh
var response = JSON.parse(xhr.responseText);
console.log(response,"hi", xhr.responseText)
~~~
* Update the order if the response received is `true`. Replace the wait page with the orders page.
~~~sh
if(response[0] == true){
updateOrder(response[1])
location.replace("orders.html");
~~~


* Save and run the code to check the output.