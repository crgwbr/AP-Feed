#!/usr/bin/python

## Craig Weber
## Started September 1, 2010
## AP-feed for Treesaver project

## Spec:
## A simple python library that does the following, given the XML feed for a category:
##  - Return a list of each story in the feed, where the story (can be Class or Dict, doesn't matter) has the following fields:
##    - Unique ID
##    - Title: Plain text, no HTML
##    - Summary: Use the plain text (no HTML) from the first paragraph,
##      without the location and author information (e.g. NEW YORK (AP) --)
##    - Date
##    - Images: List of images in the article, with each having:
##      - Caption (not including any credit information, like AP Photo)
##      - Credit information
##      - URL to the image
##    - Content: The HTML content of the article. Strip the surrounding <div>
##      such that it's just a sequence of <p> tags. Also:
##      - Add class='first' to the first paragraph
##      - Add class='last' to the final paragraph

## Notes:
##  Returns a Class

## Usage (provide XML):
##    from associatedpress import ap
##    ap = parse(xml = feed_xml)
##    stories = ap.parse()

## Usage (provide URL):
##    from associatedpress import ap
##    ap = parse(url = "http://example.com/feed.xml")
##    stories = ap.parse()


from BeautifulSoup import BeautifulSoup
import time
import urllib2

class story:
    # This class is the model that holds the data once a feed has been parsed.
    """
    >>> ob = story(unique_id = "123456789", title = "Title", summary = "Summary", date = "01 January 2010 08:00+00:00", images = [image(caption = "CAPTION", credit = "CREDIT", url = "URL")], content = "Content")
    >>> print ob.unique_id
    123456789
    >>> print ob.title
    Title
    >>> print ob.summary
    Summary
    >>> print ob.date
    01 January 2010 08:00+00:00
    >>> print ob.images[0].caption
    CAPTION
    >>> print ob.images[0].credit
    CREDIT
    >>> print ob.images[0].url
    URL
    >>> print ob.content
    Content
    """
    def __init__(self,
                 unique_id = 0,
                 title = "Title",
                 summary = "Summary",
                 date = time.strftime("%d %B %Y %H:%M+00:00"),
                 images = [],
                 content = "Content"):
        # Init the defaults
        self.unique_id = unique_id
        self.title = title
        self.summary = summary
        self.date = date
        self.images = images
        self.content = content

    def __str__(self):
        # Just to make things readable if you happen to run: "print feed"
        return str(self.date) + " " + self.title

class image:
    # Image data model
    """
    >>> ob = image(caption = "This is a caption", credit = "Photo Credit", url = "Uniform Resource Located")
    >>> print ob.caption
    This is a caption
    >>> print ob.credit
    Photo Credit
    >>> print ob.url
    Uniform Resource Located
    """
    def __init__(self,
                 caption = "",
                 credit = "",
                 url = ""):
        self.caption = caption
        self.credit = credit
        self.url = url
    def __str__(self):
        return self.url

class parse:
    # Takes either XML or a URL that points to XML and gets the important bits.
    # Stores the result in an instance of feed.
    """
    >>> ob = parse(xml = 'xml')
    >>> ob = parse(url = "http://www.example.com")
    >>> print ob.parse()
    []
    >>> ob.set_xml(xml = open('category.feed', 'r').read())
    >>> ob = ob.parse()[0]
    >>> print ob.title
    Couche Tard raises buyout offer for Casey's
    >>> print ob.unique_id
    242a5ef5-0dc9-4117-925e-f3992022c8bd
    >>> print ob.images
    []
    >>> print ob.date
    1 September 2010 13:21+00:00
    """
    def __init__(self, xml = "", url = ""):
        # You need to supply either xml or url
        # Preference goes to xml if you supply both
        # Raises XMLError if you supply neither.
        self.set_xml(xml, url)
        
    def set_xml(self, xml = "", url = ""):
        # You can reuse one instance of this by calling xml with new data
        if xml != "":
            self.xml = xml
        elif url != "":
            self.xml = urllib2.urlopen(url).read()
        else:
            raise XMLError('You need to supply either xml data or a url where xml is found.  You did neither.')

    def parse(self):
        # Do the actual parsing
        soup = BeautifulSoup(self.xml)
        entries = soup.findAll('entry')
        stories = []
        for entry in entries:
            temp = story()
            # UID
            temp.unique_id = str(entry.id.renderContents()).split(':')[2]
            # Title
            temp.title = entry.find('title', type="text").renderContents()
            # Date
            temp.date = entry.find('span', {'class' : 'updated dtstamp'}).renderContents()
            # Process story content
            content = entry.find('div', {'class' : 'entry-content'})
            content.find('abbr').extract()
            # Isolate Summary
            temp.summary = content.p.renderContents()[11:].strip()
            # Dump full content
            temp.content = []
            paragraphs = content.findAll('p')
            temp.content.append("<p class='first'>" + paragraphs[0].renderContents() + "</p>")                   # First Paragraph (append a css class)
            for i in paragraphs[1:-1]:                                                                           # Loop through the meat
                temp.content.append(str(i))
            temp.content.append("<p class='last'>" + paragraphs[len(paragraphs)-1].renderContents() + "</p>")    # Append another CSS clas to the last paragraph
            temp.content = ''.join(temp.content)                                                                 # Concat it all together
            # Get photos
            temp.images = []
            for photo in entry.findAll('a', {'rel' : 'enclosure'}):
                src = photo.img['src']
                alt = str(photo.img['alt']).split('(')
                desc = alt[0]
                try: credit = alt[1].strip(')')  # In case credit doesn't exist
                except: pass
                temp.images.append(image(desc, credit, src))
            # Save
            stories.append(temp)
        # Return all the nicely formated data
        return stories
                
        
class XMLError(Exception):
    # Basic Error Class
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

        
# Doctests
if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
