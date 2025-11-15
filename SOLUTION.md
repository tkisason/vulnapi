**Spoilers ahead, if you want to solve this on your own, stop reading :)**


Here is a list of vulnerabilities in the project:

- Hardcoded JWT signing key (`SECRET_KEY`) in source code
- Weak JWT signing key (`SECRET_KEY`). The key can be cracked by an attacker and an arbitrary JWT can be generated.
- Hardcoded Bcrypt2 salt when hashpw is used, all hashed password have the same salt and no benefit from salting is obtained.
- Mass assignment vulnerability in `/me/notifications` endpoint in (`users_db[i] = {**user, **email}`)
- Insecure yaml deserialization (RCE) in `/bulk`
- SQL injection via format strings in `/bank/codes`
- IDOR / Data exposure in `/bank_codes/`
- LFI in `/exchangerate/`
- SSRF in `/currentexchangerate/`
- SSTI (RCE) via Jinja2 in `/greeter/`
- Data exposure by issuing TRACE request to `/vulnapi/inmemory/usersdb` or `/vulnapi/inmemory/accounts`. You can't find those endpoints in the swagger file, only by code review or by manually discovering paths with the help of a dirbusting. Idea is that sometimes devs leave debugging endpoints in the application that you can find and exploit.
- Some endpoints are missing authentication (easiest way to find them is to look at the Swagger spec and see endpoints without a lock icon, but you should try and use Autorize / Autorepeater or other automations to find those)
