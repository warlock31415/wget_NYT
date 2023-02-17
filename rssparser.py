import feedparser
import webbrowser
from subprocess import Popen,PIPE


class RSSParser:   
    def __init__(self,max_feeds):
        self.feeds = []
        self.prev_links = [0,0,0]
        self.max_feeds = max_feeds

        self.categories = ['ALL']

        self.index_state = self.categories[0]

    
        
    def parserss(self,urllist,key='*'):
        res = []
        seen = []
        for url in urllist:
            feed = feedparser.parse(url)
            entries = feed.entries
            for entry in entries:
                #self.feeds['Title'].append(entry.title)
                #self.feeds['URL'].append(entry.link)

                category = url.split("/")[-1].split(".")[0]
                if category not in self.categories:
                    self.categories.append(category)
                
                self.feeds.append({'Title':entry.title,
                    'URL':entry.link,
                    'Date':entry.published,
                    'Topic':category})

        # Sort the feeds based on publish time with latest at the top
        self.feeds = sorted(self.feeds,key=lambda x:x['Date'],reverse=True)

        # Remove any duplicate feeds from similar categories
        for x in self.feeds:
            title = x['Title']
            if title not in seen:
                seen.append(title)
                res.append(x)

        # Store all feeds
        self.feeds = res
        res = self.update_topic_feed(key)


        # Only use the top max_feeds number of feeds
        if len(res) > self.max_feeds:
            res = res[:self.max_feeds]
        
        return res,self.categories

    
    def __set_to_0(self,elements):
        for i in range(0,len(elements)):
                if elements[i] == None:
                        elements[i] = 0
        return elements

    def __check_disimilarity(self,l1,l2):
        for i in range(0,len(l1)):
            if l1[i] != l2[i]:
                return i

    def __get_html_filename(self,url):
        # Get the last part of the URL (the filename)
        filename = url.split("/")[-1]
        # Remove any query string or fragment identifier
        filename = filename.split("?")[0].split("#")[0]
        # Return just the filename (without any directory path)
        return filename

    def process_click(self,n_clicks,id_list,style_list, root_dir):
        # Convert all None's to 0s
        n_clicks = self.__set_to_0(n_clicks)

        if all(count == 0 for count in n_clicks):
            self.prev_links = n_clicks
            return style_list
        
        # Find the index of the link that was clicked
        index = self.__check_disimilarity(n_clicks,self.prev_links)
        # Get the dictionary containing the ID of the clicked link
        id_dict = id_list[index]
        # Get the URL and title from the dictionary
        clicked_feed = self.update_topic_feed(self.index_state)
        url = clicked_feed[id_dict['index']]['URL']

        # Download the URL using wget
        process = Popen(['wget','-P',root_dir,url],stdout=PIPE,stderr=PIPE)
        stdout,stderr = process.communicate()
        filename = 'file://'+root_dir+self.__get_html_filename(url)
        self.prev_links = n_clicks
        # Open the downloaded file in a web browser
        webbrowser.open(filename)

        return style_list

    def update_topic_feed(self,key='*'):
        new_feed = []

        if key =='*' or key == 'ALL':
            return self.feeds[:self.max_feeds]

        for feed in self.feeds:
            if feed['Topic'] == key:
                new_feed.append(feed)
        
        return new_feed








        




        

if __name__ == '__main__':
    exit
