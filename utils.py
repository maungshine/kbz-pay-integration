import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def to_encrypt(json_obj, app_key):
    key_list = []
    str_to_encrypt = b''
    for key in json_obj['Request']:
        if key == 'biz_content':
            for key_item in json_obj['Request'][key]:
                if json_obj['Request'][key][key_item]:
                    key_list.append(key_item)
        else:
            if json_obj['Request'][key]:
                key_list.append(key)
    
    sorted_key_list = sorted(key_list)
    for item in sorted_key_list:
        if item == sorted_key_list[0] and item in json_obj['Request']:
            str_to_encrypt = str_to_encrypt + str.encode(item) + b'=' + str.encode(json_obj['Request'][item])
        elif item == sorted_key_list[0] and item in json_obj['Request']['biz_content']:
            str_to_encrypt = str_to_encrypt + str.encode(item) + b'=' + str.encode(json_obj['Request']["biz_content"][item])
        elif item in json_obj['Request']['biz_content']:
            str_to_encrypt = str_to_encrypt + b'&' + str.encode(item) + b'=' + str.encode(json_obj['Request']['biz_content'][item])
        else:
            str_to_encrypt = str_to_encrypt + b'&' + str.encode(item) + b'=' + str.encode(json_obj['Request'][item])

        sign_string = str_to_encrypt + b'&key=' + str.encode(app_key)
    return sign_string

# precreate = {
# "timestamp": '29200202',
# "notify_url": "https://32fad2e5ccaf.ngrok.io",
# "nonce_str": get_random_string(16),
# "method": "kbz.payment.precreate",
# "sign_type": "SHA256",
# "sign": '2727328839',
# "version": "1.0",
# "biz_content": {
# "appid": '292828292',
# "merch_code": "200106",
# "merch_order_id": '3738383',
# "trade_type": "PAY_BY_QRCODE",
# "title": "iPhone X",
# "total_amount": "50",
# "trans_currency": "MMK",
# "timeout_express": "100m",
# "callback_info": ""
# }
# }
#
#
# to_encrypt(precreate)
