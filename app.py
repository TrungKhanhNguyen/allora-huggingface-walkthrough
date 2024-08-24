from flask import Flask, Response
import requests
import json
import pandas as pd
import torch
import random

# create our Flask app
app = Flask(__name__)
        
def get_memecoin_token(blockheight):
    
    upshot_url = f"https://api.upshot.xyz/v2/allora/tokens-oracle/token/{blockheight}"
    headers = {
        "accept": "application/json",
        "x-api-key": "UP-ad6b5045c4b849afb08db09d" # replace with your API key
    }   
    
    response = requests.get(upshot_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        name_token = str(data["data"]["token_id"]) #return "boshi"
        return name_token
    else:
        raise ValueError("Unsupported token") 
    
def get_simple_price(token):
    base_url = "https://api.coingecko.com/api/v3/simple/price?ids="
    token_map = {
        'ETH': 'ethereum',
        'SOL': 'solana',
        'BTC': 'bitcoin',
        'BNB': 'binancecoin',
        'ARB': 'arbitrum'
    }
    headers = {
        "accept": "application/json",
        "x-cg-demo-api-key": "CG-fn5Dnv5ujTE8SoQvQP5APwDu" # replace with your API key
    }
    token = token.upper()
    if token in token_map:
        url = f"{base_url}{token_map[token]}&vs_currencies=usd"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return str(data[token_map[token]]["usd"])
        
    elif token not in token_map:
        token = token.lower()
        url = f"{base_url}{token}&vs_currencies=usd"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return str(data[token]["usd"])   
           
    else:
        raise ValueError("Unsupported token") 

def get_last_price(token, p):
    
    price_up = p
    price_down = p
    
    token = token.upper()

    if token == 'BTC':
        price_up = float(p)*1.0015
        price_down = float(p)*0.998
        return str(format(random.uniform(price_up, price_down), ".2f"))
    
    elif token == 'ETH':
        price_up = float(p)*1.0015
        price_down = float(p)*0.998
        return str(format(random.uniform(price_up, price_down), ".2f"))

    elif token == 'SOL':
        price_up = float(p)*1.0015
        price_down =float(p)*0.998
        return str(format(random.uniform(price_up, price_down), ".2f"))

    elif token == 'BNB':
        price_up = float(p)*1.0015
        price_down =float(p)*0.998  
        return str(format(random.uniform(price_up, price_down), ".2f"))

    elif token == 'ARB':
        price_up = float(p)*1.002
        price_down =float(p)*0.999   
        return str(format(random.uniform(price_up, price_down), ".4f"))
    else:
        return str(p)

# define our endpoint
@app.route("/inference/<string:tokenorblockheight>")
def get_inference(tokenorblockheight):
    
    if tokenorblockheight.isnumeric():
        namecoin = get_memecoin_token(tokenorblockheight)
    else:
        namecoin = tokenorblockheight 
    try:
        return get_last_price(namecoin, get_simple_price(namecoin))
        
    except Exception as e:
        return get_last_price(namecoin, get_simple_price(namecoin))

    
# run our Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8011, debug=True)
