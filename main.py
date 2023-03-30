#!/usr/bin/env python3
import shopify
import json
from typing import Any, Dict, List
from datetime import datetime, timedelta
import pytz


# Load authentication function
authenticate = __import__('config').authentication


# Define custom encoder to handle non-serializable attributes
class CustomEncoder(json.JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return super().default(obj)
    

authenticate()


# Get a product by its id.
def get_products_by_id(id: int) -> Dict:
    """Get a product
    
    Args:
        id (int): The product id.

    Returns:
        (Dict) - The products attributes.
    """
    product = shopify.Product.find(id)
    return product


# get an order by its id.
def get_orders_by_id(id: int) -> Dict:
    """
    Get a order
    
    Args:
        id (int): The order id.
        
    Returns:
        The order attributes.
    """
    order = shopify.Order.find(id)
    return order.attributes


# Get fulfilled orders
def get_fulfilled_orders() -> List:
    """
    Get a list of fultilled orders
    
    Returns:
        (List) - Fulfilled orders
    """
    orders = shopify.Order.find()

    for order in orders():
        print(get_orders_by_id(order))
        print('')


# # Get Customers information
# def get_customer(id):
#     c = shopify.Customer.find(id)
#     print(json.dumps(c.attributes, cls=CustomEncoder, indent=4))


# authenticate()

# get_customer(6047592251611)
# product = get_products_by_id(7533145915611)
# print(json.dumps(product, cls=CustomEncoder, indent=4))

# order = get_orders_by_id(5199006925019)
# print(json.dumps(order, cls=CustomEncoder, indent=4))

# fulfilled_orders = get_fulfilled_orders()
# fulfilled_orders

def get_all_orders_from_miniApp():
    """ Allowed querry limit is 250 
    Find a better way to get more records in the query
    
    """
    LIMIT = 250
    CREATED_AT_MIN = datetime(2023, 3, 22, 7, 0, 0, 0, tzinfo=pytz.UTC)
    NOW = datetime.now(pytz.UTC)
    saf_orders = []

    fact = 'I AM AWESOME'
    since_id = 0

    while fact == 'I AM AWESOME':
        print('created_at: ', CREATED_AT_MIN)
        orders = shopify.Order.find(limit=LIMIT, since_id=since_id, created_at_min=CREATED_AT_MIN)
        search_string = '/?utm_source=&utm_medium=&utm_content=&tid=iOhuQl1ykP'

        for order in orders:
            since_id = order.id
            if order.attributes.get('landing_site') == search_string:
                print(order.id)
                saf_orders.append(order)
                
            if order.attributes.get('landing_site') == '/?tid=iOhuQl1ykP':
                print(order.id)
                saf_orders.append(order)

        if len(orders) == 0:
            break
        # print(orders)
        
        # Latest order
        latest = orders[0]
        date_string = latest.attributes.get('created_at')
        print('last_order create_at: ', date_string)
        
        date_format = "%Y-%m-%dT%H:%M:%S%z"
        CREATED_AT_MIN = datetime.strptime(date_string, date_format)

        if NOW < CREATED_AT_MIN + timedelta(minutes=5):
            fact = 'I LOVE CODING'

    print(saf_orders)
    print(len(saf_orders))

get_all_orders_from_miniApp()
