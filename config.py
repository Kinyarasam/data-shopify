#!/usr/bin/env python3
import shopify
import os
import json
import binascii
from dotenv import load_dotenv
import requests
import time


load_dotenv() # take environment variables from .env


API_KEY = os.getenv("api_key")
API_SECRET = os.getenv("api_secret")
ACCESS_TOKEN = os.getenv("access_token")
SHOP_NAME = os.getenv("shop_name")
shop_url = "https://%s:%s@%s.myshopify.com/admin/api/%s" % (API_KEY, API_SECRET, SHOP_NAME, '2022-10')


def authentication():
    shopify.Session.setup(api_key=API_KEY, api_secret=API_SECRET)

    shop_url = f"{SHOP_NAME}.myshopify.com"
    api_version = '2022-10'
    state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
    redirect_uri = "http://myapp.com/auth/shopify/callback"
    scopes = []

    newSession = shopify.Session(shop_url, api_version)
    auth_url = newSession.create_permission_url(scopes, redirect_uri, state)
    # redirect to auth url

    session = shopify.Session(shop_url, api_version, ACCESS_TOKEN)
    shopify.ShopifyResource.activate_session(session)
    shop = shopify.Shop.current() # Get the current shop
    
    return shop
