# vulnapi
Intentionaly very vulnerable API with bonus extremely bad coding practices

**Work in progress... Don't expect this to work or be stable**

*NOTE: This is by design a vulnerable application. It's use is to demonstrate bad coding practices (in python3) and to show off specific vulnerabilities that are not well presented in some other projects, especially some fickle and subtile things.*

*DO NOT USE _ANY_ PIECE OF THIS CODE IN PRODUCTION! Really.*
*Keep in mind, this code is vulnerable to remote code execution, so someone can literally execute arbitrary code on your server with this.*


Current vulns:
* Couple of cases of data exposure (by triggering logic issues)
* Mass assignment
* Broken object level autorization
* Broken authentication
* RCE via deserialization


To-Do:
* BOLA on a simpler example (OWASP ZAP fuzzer playground)
* SQL injection (prolly on both examples)
    - Get prefix?




Running:

`uvicorn main:app --reload`

