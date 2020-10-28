import time
import random
import hashlib
import requests
import datetime
import json
from datetime import timezone
from flask import Flask,render_template, request, redirect, url_for
from utils import get_random_string, to_encrypt
from flask_qrcode import QRcode
from models import db, Order,app


QRcode(app)
APP_ID = 'kpb67f5efda76b481998645ef28ca356'
APP_KEY = '1be73b08e9f3215020aa88d28a494b08'
merchant_url = 'https://246df2500385.ngrok.io'
db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    res = request.get_json()
    if request.method == 'POST':
        if res is not None and 'Request' in res:
            mm_order = res['Request']['mm_order_id']
            order = Order.query.filter_by(mm_order_id=mm_order).first()
            if order is None:
                order = Order(mm_order_id=mm_order, order_id='7783')
                db.session.add(order)
                db.session.commit()
            return 'success', 200
        # Getting the current date
        # and time
        dt = datetime.datetime.now()

        utc_time = dt.replace(tzinfo = timezone.utc)
        utc_timestamp = int(utc_time.timestamp())

        order_id = str(random.randint(1000, 9999))
        precreate = {
 "Request": {
 "timestamp": str(utc_timestamp),
 "notify_url": merchant_url,
 "nonce_str": get_random_string(16),
 "method": "kbz.payment.precreate",
 "sign_type": "",
 "sign": "",
 "version": "1.0",
 "biz_content": {
 "appid": APP_ID,
 "merch_code": "200106",
 "merch_order_id": order_id,
 "trade_type": "PAY_BY_QRCODE",
 "total_amount": "100",
 "trans_currency": "MMK",
 "timeout_express": "100m",
 }
}
}
        sign_value = hashlib.sha256(to_encrypt(precreate, APP_KEY)).hexdigest()
        precreate['Request']['sign_type'] = 'SHA256'
        precreate['Request']['sign'] = sign_value
        result = requests.post(url='http://api.kbzpay.com/payment/gateway/uat/precreate', json=precreate)
        js = result.json()
        # print(js)
        if js['Response']['result'] == 'SUCCESS':
            qrc = js['Response']['qrCode']
            return render_template('pay_now.html', qrc=qrc, order_id='7783')
    return render_template('checkout.html')


@app.route('/report', methods=['GET'])
def report():
    orders = Order.query.all()
    return render_template('report.html', orders=orders)

@app.route('/payment_status/<int:order_id>', methods=['GET'])
def payment_status(order_id):
    orders = Order.query.filter_by(order_id=order_id).first()
    if orders is None:
        return render_template('transaction.html', paymentStatus='Payment Unsuccessful', orders=None)
    db.session.delete(orders)
    db.session.commit()
    return render_template('transaction.html', paymentStatus='Payment Successful', orders=orders)


if __name__ == '__main__':
    app.run(debug=True, port=80)
