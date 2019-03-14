import os

def createPage():
    htmlFile='index.html'
    f=open(htmlFile, 'w')
    f.write("<html><body><p>Python has created this Page for the API Call. It can now be closed.</p></body></html>")
    f.close()
    return htmlFile
