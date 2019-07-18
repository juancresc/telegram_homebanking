# telegram_homebanking
This is just a personal sunday project. 

## What?
A telegram bot to retrieve data from many REDLINK accounts from Banco de la Nación Argentina.


data.json should be like:
```
{
    "accounts": [
        {
            "username": "u1",
            "password": "p1"
        },
        {
            "username": "u2",
            "password": "p2"
        }
    ]
}
```
Also geckodriver should be in PATH

Then just run

`python bot.py`