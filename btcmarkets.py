import base64, hashlib, hmac, urllib2, time, urllib, json
from collections import OrderedDict

base_url = 'https://api.btcmarkets.net'

def request(action, key, signature, timestamp, path, data):
     
    header = {
        'accept': 'application/json', 
        'Content-Type': 'application/json',
        'User-Agent': 'btc markets python client',
        'accept-charset': 'utf-8',  
        'apikey': key,
        'signature': signature,
        'timestamp': timestamp,
    }
    
    request = urllib2.Request(base_url + path, data, header)
    if action == 'post':
        response = urllib2.urlopen(request, data)
    else:
        response = urllib2.urlopen(request) 
    return json.load(response)


def get_request(key, secret, path):
     
    nowInMilisecond = str(int(time.time() * 1000))
    stringToSign = path + "\n" + nowInMilisecond + "\n"  

    signature = base64.b64encode(hmac.new(secret, stringToSign, digestmod=hashlib.sha512).digest())

    return request('get', key, signature, nowInMilisecond, path, None)    


def post_request(key, secret, path, postData):
     
    nowInMilisecond = str(int(time.time() * 1000))
    stringToSign = path + "\n" + nowInMilisecond + "\n" + postData  

    signature = base64.b64encode(hmac.new(secret, stringToSign, digestmod=hashlib.sha512).digest())

    return request('post', key, signature, nowInMilisecond, path, postData) 


class BTCMarkets:

    def __init__(self, key, secret):
        self.key = key
        self.secret = base64.b64decode(secret)

    def trade_history(self, currency, instrument, limit, since):
     	
        data = OrderedDict([('currency', currency),('instrument', instrument),('limit', limit),('since', since)])
        postData = json.dumps(data, separators=(',', ':'))
        return post_request(self.key, self.secret, '/order/trade/history', postData) 

    def order_create(self, currency, instrument, price, volume, side, order_type, client_request_id):
     	
        data = OrderedDict([('currency', currency),('instrument', instrument),
            ('price', price),('volume', volume),('orderSide', side),('ordertype', order_type),
            ('clientRequestId', client_request_id)])
        postData = json.dumps(data, separators=(',', ':'))
        return post_request(self.key, self.secret, '/order/create', postData) 


    def order_history(self, currency, instrument, limit, since):
     	
        data = OrderedDict([('currency', currency),('instrument', instrument),('limit', limit),('since', since)])
        postData = json.dumps(data, separators=(',', ':'))
        return post_request(self.key, self.secret, '/order/history', postData) 

    def order_open(self, currency, instrument, limit, since):
     	
        data = OrderedDict([('currency', currency),('instrument', instrument),('limit', limit),('since', since)])
        postData = json.dumps(data, separators=(',', ':'))
        return post_request(self.key, self.secret, '/order/open', postData) 

    def order_detail(self, order_ids):
     	data_obj = {'orderIds':order_ids} 
        postData = json.dumps(data_obj, separators=(',', ':'))
        return post_request(self.key, self.secret, '/order/detail', postData) 

    def account_balance(self):

        return get_request(self.key, self.secret, '/account/balance') 

    def get_market_tick(self,currency_in,currency_out):
        
        return get_request(self.key, self.secret, '/market/%s/%s/tick' % (currency_in,currency_out))

    def get_market_orderbook(self,currency_in,currency_out):
        
        return get_request(self.key, self.secret, '/market/%s/%s/orderbook' % (currency_in,currency_out))

    def get_market_trades(self,currency_in,currency_out):

        return get_request(self.key, self.secret, '/market/%s/%s/trades' % (currency_in,currency_out))




