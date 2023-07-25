from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[''], # Add your url for frontend
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="",  # your redis database credentials
    port=,
    password="",
    decode_responses=True
)

class Order(HashModel):
    product_id : str
    price: float
    fee : float
    total : float
    quantity : int
    status : str # pending, completed, refunded

    class Meta:
        database = redis

def format(pk : str):
    order = Order.get(pk)
    return {
        "product_id" : order.pk,
        "price" : order.price,
        "fee" : order.fee,
        "total" : order.total,
        "quantity" : order.quantity,
        "status" : order.status
    }

@app.get('/orders')
def all():
    return [format(pk) for pk in Order.all_pks()]

@app.get('/orders/{pk}')
def get(pk : str):
    return Order.get(pk)

@app.post('/orders')
async def create(request: Request, background_task : BackgroundTasks):  # id, quantity
    body = await request.json()

    req = requests.get('http://localhost:8000/products/%s' % body['id'])
    product = req.json()

    order = Order(
        product_id = body['id'],
        price = product['price'],
        fee = 0.2 * product['price'],
        total = 1.2 * product['price'],
        quantity = body['quantity'],
        status = "pending"
    )
    order.save()

    background_task.add_task(order_completed, order) # Executes in background

    return order

def order_completed(order: Order):
    time.sleep(5) # Considering payment process takes 5 seconds
    order.status = "completed"
    order.save()
    redis.xadd('order_completed', order.dict(), '*')
