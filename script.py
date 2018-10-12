import os

with open('products/data/products.json', 'rb') as f:
    data = f.read()
newdata = open('products.json', 'wb')
newdata.write(data)
newdata.close
exit()