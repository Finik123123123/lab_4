from flask import Flask
app=Flask(__name__)
stores=[{"name":"My store",
         "utems":[
             {
                 "name":"chair",
                 'price':15.99
             }
         ]}]
@app.get("/store")
def get_stores():
    return {'stores':stores}