# django-portal
For this portal to connect with the login service you need to create a client and generate a secret with this information.
- Login into the login service with a admin account and create a sector identifier, set the **Redirect Login URIs** to ***https://{portalHost}.{domain}/oidc/callback/*** example: ***https://portal.demo.eoepca.org/oidc/callback/*** it is very important to put the last ***/***
Leave the **Clients** blank
- Copy the **id** of this new sector identifier
- Execute the script registerclient.sh
You can set up the environment variables **portalHost** (default=portal) and **authHost** (default=auth) before executing the script.
You will need two arguments: The **domain** and the **sector identifier id**
like this: ***./registerclient.sh {domain} {sectorIdentifierID}***

example: 

```
export portalHost=portal
export authHost=auth
./registerclient.sh demo.eoepca.org f1eb6aa8-2b01-4992-8dbe-780148d0c238
```

This will create the file **django-secrets.yaml** with the secrets the portal needs to deploy.
