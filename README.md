# backend-test

# How to setup locally
After cloning this repo, run the following commands locally to start the project (Linux/Ubuntu).
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8002 --reload --> now open http://0.0.0.0:8002/docs in browser
You will see all APIs.
First, run the seeder. Then, run the login API to get a token. Afterward, you will be able to run all other APIs using that access token.

# Apis

Seeder : To seed fake/random data into database.
Login : To get access token by providing credtionals.
Sales : To get Sales info along with time and different parameters.
Revenue : To get daily, weekly, monthly and annually revenue.
Inventory : To get ineventory status along with low stock flag. Also, to update inventory.
Product : To register new products.
