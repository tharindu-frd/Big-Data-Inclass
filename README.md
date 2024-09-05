## Procedure

# (01) Created an API what it does is run continously and update the stock prices in to a mongodb database

```
docker build -t flask-stock-app .

docker run -p 5000:5000 flask-stock-app
```
