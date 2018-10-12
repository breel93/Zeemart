import os


with open('products.json','rb') as f:
    contents = f.read()
newdata = open('products/products.json', 'wb')
newdata.write(contents)
newdata.close


