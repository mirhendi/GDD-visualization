# Based on the answers found here:
# http://stackoverflow.com/questions/5368669/convert-base64-to-image-in-python

import base64
from html.parser import HTMLParser

def catch_image(base64data):
    
    base64img = base64.decodestring(base64data)
    with open('../acc_gdd.png','wb') as f:
        f.write(base64img)
    print ("Saved plot as 'acc_gdd.png' for you!")

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

        parser = MyHTMLParser()
        
        parser.feed('<html><head><title>Test</title></head>'
            '<body><h1>Parse me!</h1></body></html>')
