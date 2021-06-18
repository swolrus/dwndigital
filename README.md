# DWN Digital

## Payment API Structure
```json
data = {
            'id': 1,
            'buyer_id': 1,
            'buyer': 'David Norris',
            'adress': '10 The Boulevard Floreate Western Australia 6014',
            'item_id': 1,
            'item': 'Kaiman x POSTMAN Fleece Sweater',
            'quantity': 1,
  					'approved': 'False'
        }
```

| Route                        | HTTP Method | Function                        |
| ---------------------------- | ----------- | ------------------------------- |
| /payments/                   | POST        | Create a payment                |
| /payments/\<pid>             | GET         | Get the payment information     |
| /payments/setapproved/\<pid> | POST        | Set a payment as being approved |
| /payments/getapproved/\<pid> | GET         | Ask if a payment is approved    |
| /payments/items              | GET         | Return a collection of items    |



## DEV TIPS

### MIGRATIONS
When using sqlite you will find that upgrades/downgrades will not work as `ALTER` commands are not supported. To fix this set `render_as_batch=True` and this will mean alembic will delete, reconfigure, and repopulate the table. Must be done before a migration is generated so it actually contains the batch script. Here is a snippet from /migrations/env.py:
```python
context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True
            process_revision_directives=process_revision_directives,
            **current_app.extensions['migrate'].configure_args
        )
```

## DB Test Data Commands
```shell
flask shell
>>Buyer(id=1, name='David Norris', email='me@dwn.digital', address='10 The Boulevard Floreat WA 6014').commit()
>>Item(id=1, name='Kaiman x POSTMAN Fleece Hoody', price=70).commit()
>>Transaction(buyer_id=1, item_id=1, quantity=2).commit()
```

## Drop env Variables
Having lingering environment variables can stop configuration from working correctly, must unset each to ensure that the app will load the correct vars.
```shell
unset <VAR_NAME>
```