#!/usr/bin/python

## Craig Weber
## September 6, 2010

## This file demonstrates using the associatedpress module (enclosed)

from associatedpress import ap

# Open a previously downloaded feed (XMl/ATOM data)
# Put data into a string
ap_file = open('category.feed', 'r')
ap_feed = ap_file.read()
ap_file.close()

# Pass XMl data to parser
parser = ap.parse(xml = ap_feed)
# The same could also be accomplished by providing a raw url
# data = ap.parse(url = "http://example.com/ap.feed")

# Extract data from feed
stories = parser.parse()

# Do something with the extracted data
for story in stories:
    print story
    print
    print story.unique_id
    print
    print story.title
    print
    print story.summary
    print
    print story.date
    print
    # print story.content
    # print
    for image in story.images:
        print image.caption
        print image.credit
        print image.url
        print
    print "\n\n\n\n"


# You can re-use the same parser object (with another feed) by calling ap.set_xml()
ap_file = open('category2.feed', 'r')
ap_feed = ap_file.read()
ap_file.close()

parser.set_xml(xml = ap_feed)
stories = parser.parse()


# Do something with the extracted data from te second feed
for story in stories:
    print story
    print
    print story.unique_id
    print
    print story.title
    print
    print story.summary
    print
    print story.date
    print
    # print story.content
    # print
    for image in story.images:
        print image.caption
        print image.credit
        print image.url
        print
    print "\n\n\n\n"

raw_input('Press Enter to Exit')
