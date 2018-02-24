#!/usr/bin/python3

import cgitb
import getpass
cgitb.enable()

print("Content-Type: text/html;charset=utf-8")
print()

print("<!Doctype html>")
print("<html>")
print("    <head>")
print("        <title>CGI Apache httpd demo Python</title>")
print("    </head>")
print("    <body>")
print("        <h1>CGI Apache httpd demo Python</h1>")
print("        <p>Welcome " + getpass.getuser() + "</p>")
print("    </body>")
print("</html>")