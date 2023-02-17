# wget_NYT
Essentially a python RSS bot that reads the URL to the NYT rss feed and downloads the html file locally. Thus bypassing the need for a subscription as of 2023

## Dependencies
- Python dash
- Python feedparser

### Install dependencies
 ```pip install dash feedparser```
 
 ## Usage
 Add your NYT RSS feed url obtained from the [NYT website](https://www.nytimes.com/rss). run `main.py`
```
python main.py
```
Dash will create a website at localhost:8050

## Known Issues
I'm not too sure how to keep track of links that you've read

## TODO
- Package everything in a docker container
- Add a user input field and button to grab any NYT page
- Add a way to load more feeds without having to change the code
 
