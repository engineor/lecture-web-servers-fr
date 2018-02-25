#include <iostream>
#include <stdlib.h>
using namespace std;
 
int main()
{
	cout<<"Content-type: text/html"<<endl;
    cout<<endl;
    cout<<"<!Doctype>"<<endl;
	cout<<"<html>"<<endl;
    cout<<"    <head>"<<endl;
    cout<<"        <title>CGI Apache httpd demo C++</title>"<<endl;
    cout<<"    </head>"<<endl;
    cout<<"    <body>"<<endl;
    cout<<"        <h1>CGI Apache httpd demo C++</h1>"<<endl;
    cout << getenv("USER") << endl;
    cout<<"    </body>"<<endl;
    cout<<"</html>"<<endl;
 
	return 0;
}
