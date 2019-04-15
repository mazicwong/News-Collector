## News Crawl & Comment Collect
A project to crawl news from different platforms, and use NLP & ML algorithm to do the classify, extract and generate messages.

### first: download news
```
cd news_crawl
python3 runspider.py
```

### second: do classification
```
cd segment
python3 runsegment.py
```

### third: show in the web
```
cd website
python3 server.py
```

### Deploy to server
```
cd website && python3 server.py
cd ../ && nohup python3 main.py
```