#AP-Feed

A basic wrapper around the AssociatedPress's XML feed.  Included are some sample feed files

###Spec:
A simple python library that does the following, given the XML feed for a category:

Return a list of each story in the feed, where the story (can be Class or Dict, doesn't matter) has the following fields:

* Unique ID
* Title: Plain text, no HTML
* Summary: Use the plain text (no HTML) from the first paragraph, without the location and author information (e.g. NEW YORK (AP) --)
* Date
* Images: List of images in the article, with each having:
  * Caption (not including any credit information, like AP Photo)
  * Credit information
  * URL to the image
* Content: The HTML content of the article. Strip the surrounding `<div>` such that it's just a sequence of `<p>` tags. Also:
  * Add class='first' to the first paragraph
  * Add class='last' to the final paragraph

###Notes:
Returns a Class

###Usage (provide XML):
    from associatedpress import ap
    ap = parse(xml = feed_xml)
    stories = ap.parse()

###Usage (provide URL):
    from associatedpress import ap
    ap = parse(url = "http://example.com/feed.xml")
    stories = ap.parse()