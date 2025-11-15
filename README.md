# vulnapi
Intentionaly very vulnerable API with bonus extremely bad coding practices

*NOTE: This is by design a vulnerable application. It's primary use is to demonstrate bad coding practices (in python3) and in operations (docker, etc) and to show off specific vulnerabilities that are not well presented in some other projects. Another use if to have an application that can be used as a demo for various devsecops methods*

*DO NOT USE _ANY_ PIECE OF THIS CODE IN PRODUCTION! Really.*
*This code is vulnerable to remote code execution, don't leave it in the open*

Current implemented vulns:
* Couple of cases of data exposure (by triggering logic issues)
* Mass assignment vulnerabilities
* Broken object level autorization
* Broken authentication
* RCE via deserialization
* SQL injection
* File inclusion / path traversal
* Server Side Template Injection

[For solutions, please see the SOLUTION.md file](SOLUTION.md) 

Usage
:
```
docker build --tag vulnapi .
docker run -it --rm -p8000:8000 vulnapi
```
open `http://IP_OF_HOST:8000/docs` in a webbrowser.

Pull requests, especially for cool, subtle bugs or bad practices are welcome. At least FastAPI makes it easy to implement examples.
