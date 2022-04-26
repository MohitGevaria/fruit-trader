
# Fruit Trader API

The apis allows you to buy and sell differnet fruits and get overall profit margins for Trader.
There are three endpoints as described in Endpoints section which can be use to perform the trade operations.

# Installation and Usage Guide

For running the application on windows make sure python 3.6 or higher is installed. 
Then Follow the following: steps 
- Clone the repository: git clone https://github.com/MohitGevaria/fruit-trader.git or unzip the folder provided.
- Change the directory as follow: cd fruit-trader
- Run command : pip install -r requirements.txt
- Run command : python3 run.py
- The api is now accessible at localhost:5000

# Endpoints accessible and Usage

- Buy Endpoint
    * Available at : /fruittrader/buy [POST]
    `Sample body: {
    "fruit":"Name",
    "price": 10,
    "quantity": 10
    } `

- Sell Endpoint
    * Available at : /fruittrader/sell [POST]
    `Sample body: {
    "fruit":"Name",
    "price": 10,
    "quantity": 10
    } `

- Profit Endpoint
    * Available at : /fruittrader/profit [GET] 
    
- Available Quantity Endpoint
    * Available at : /fruittrader/<fruit_name> [GET]
     
**Note** : Fruit name are case-insensitive. And content-type supported are Json and Formdata.

# Development Information

Folder Structure

```
├── app
│   ├── __init__
│   ├── routes.py
├── utils
│   ├── routes_utility.py
│   ├── utility.py
├── requirements.txt
├── run.py 
└── .gitignore
```

Developed Using Flask Framework.

