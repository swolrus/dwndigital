import requests

payload = {
    "name":"David",
    "email":"me@dwn.digital",
    "address":"BLVD",
    "items":[
        {
            "id":"0",
            "quantity":3
        },
        {
            "id":"0",
            "quantity":1
        }
    ]
}
url = 'http://127.0.0.1:5000/payments/create'
r = requests.post(url=url , json = payload)
print(r.text)