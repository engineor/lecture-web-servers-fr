#!/usr/bin/python3

import cgitb
import datetime
cgitb.enable()

currentTime = datetime.datetime.now()

print("Content-Type: text/html;charset=utf-8")
print()

print("<!Doctype html>")
print("<html>")
print("    <head>")
print("        <title>CGI Apache httpd demo Python</title>")
print("    </head>")
print("    <body>")
print("        <h1>CGI Apache httpd demo Python</h1>")
print("        <p>" + currentTime.strftime("We are the %d, %b %Y %I:%M:%S %p") + "</p>")
print("    </body>")
print("</html>")