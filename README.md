# Order-Processing-System
Simple Microservices API using Python FastAPI. Made by RedisJSON as a Database and dispatch events with Redis Streams.

<pre>
Inventory ->
  
    * get all products : http://localhost:8000/products ( get )
  
    * add a new product : http://localhost:8000/products ( post ) {
                                                                    "name" : "product_name",
                                                                    "price" : 20,
                                                                    "quantity" : 100
                                                                }
  
    * get specific product by id : http://localhost:8000/products/{id} ( get )

    * delete specific product by id : http://localhost:8000/products/{id} ( delete )

Payment ->
  
    * get all orders : http://localhost:8001/orders ( get )

    * get specific order by id : http://localhost:8001/orders/{id} ( get )

    * add a new order : http://localhost:8001/orders ( post ) {
                                                                "id" : "product_id",
                                                                "quantity" : 3
                                                            }

  
</pre>
 
  
