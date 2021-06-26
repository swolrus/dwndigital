from flask import current_app as app
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest

import sys

class PayPalClient:
    def init_app(self, app):
        self.client_id = app.config['PAYPAL_CLIENT_ID']
        self.client_secret = app.config['PAYPAL_CLIENT_SECRET']
        self.debug = app.config['DEBUG']
            

        """Set up and return PayPal Python SDK environment with PayPal access credentials.
           This sample uses SandboxEnvironment. In production, use LiveEnvironment."""

        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)

        """ Returns PayPal HTTP client instance with environment that has access
            credentials context. Use this instance to invoke PayPal APIs, provided the
            credentials have access. """
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        """
        Function to print all json data in an organized readable manner
        """
        result = {}
        itr = json_data.items()
        for key,value in itr:
            # Skip internal attributes.
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
                        self.object_to_json(value) if not self.is_primittive(value) else\
                         value
        return result
    def array_to_json_array(self, json_array):
        result =[]
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if  not self.is_primittive(item) \
                              else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, int)

    """ This is the sample function to create an order. It uses the
        JSON body returned by buildRequestBody() to create an order."""

    def create_order(self, body):
        request = OrdersCreateRequest()
        request.prefer('return=representation')
        #3. Call PayPal to set up a transaction
        request.request_body(body)
        response = self.client.execute(request)
        if self.debug:
            print('Status Code: ' + str(response.status_code))
            print('Status: ' + response.result.status)
            print('Order ID: ' + str(response.result.id))
            print('Intent: ' + response.result.intent)
            print('Links:')
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
            print('Total Amount: ' + response.result.purchase_units[0].amount.currency_code +
                                response.result.purchase_units[0].amount.value)

        return response

    """Setting up the JSON request body for creating the order. Set the intent in the
    request body to "CAPTURE" for capture intent flow."""
    def build_request(self, transaction):
        shipmethod = transaction.get('shipmethod') or "AusPost"
        shipping = transaction.get('shipping') or "0"
        handling = transaction.get('handling')  or "0"
        tax = transaction.get('tax') or "0"
        discount = transaction.get('discount') or "0"

        total = 0
        items = []
        for item in transaction['items']:
            from app.payments.models import Item
            dbitem = Item.objects().get(pk=item['id'])

            itemtotal = dbitem.price * item['quantity']
            total += int(itemtotal)
            anitem = {
                "name": dbitem.name,
                "description": dbitem.description,
                "unit_amount": {
                    "currency_code": "AUD",
                    "value": str(dbitem.price),
                },
                "quantity": str(item['quantity']),
                "category": "PHYSICAL_GOODS"
            }
            items.append(anitem)
        
        data = {
            "intent": "CAPTURE",
            "application_context": {
                "brand_name": "KAIMAN x POSTMAN",
                "landing_page": "BILLING",
                "shipping_preference": "SET_PROVIDED_ADDRESS",
                "user_action": "CONTINUE"
            },
            "purchase_units": [
            {
                "reference_id": "KPA",
                "description": "Apparal",
                "custom_id": "KPAFashions",
                "soft_descriptor": "Fashions",
                "amount": {
                    "currency_code": "AUD",
                    "value": str(total),
                    "breakdown": {
                        "item_total": {
                            "currency_code": "AUD",
                            "value": str(total)
                        },
                        "shipping": {
                            "currency_code": "AUD",
                            "value": str(shipping)
                        },
                        "handling": {
                            "currency_code": "AUD",
                            "value": str(handling)
                        },
                        "total_tax": {
                            "currency_code": "AUD",
                            "value": str(tax)
                        },
                        "shipping-discount": {
                            "currency_code": "AUD",
                            "value": str(discount)
                        }
                    }
                },
                "items": items,
                "shipping": { 
                    "method": shipmethod,
                    "address": {
                        "name": {
                            "full_name": transaction['firstname'],
                            "surname": transaction['lastname'],
                        },
                        "address_line_1": transaction['address'],
                        "admin_area_1": transaction['state'],
                        "admin_area_2": transaction['city'],
                        "postal_code": transaction['postcode'],
                        "country_code": "AU"
                    }
                }
            }
            ]
        }

        return data