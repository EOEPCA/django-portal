from eoepca_scim import EOEPCA_Scim, ENDPOINT_AUTH_CLIENT_POST
import base64
import sys
import secrets
import os

authHost = os.getenv('authHost','test')
portalHost = os.getenv('portalHost','portal')

def main(hostname, sector):
    print(f"Registering new client in : {hostname}")
    scim_client = EOEPCA_Scim(f"https://{authHost}.{hostname}")
    client = scim_client.registerClient(
        "Django-portal",
        grantTypes = ["client_credentials", "password", "urn:ietf:params:oauth:grant-type:uma-ticket"],
        redirectURIs = [f"https://{portalHost}.{hostname}/oidc/callback/"],
        logoutURI = f"https://{portalHost}.{hostname}",
        responseTypes = ["code","token","id_token"],
        subject_type = 'public',
        scopes = ['openid',  'email', 'user_name ','uma_protection', 'permission', 'is_operator'],
        token_endpoint_auth_method = ENDPOINT_AUTH_CLIENT_POST,
        sectorIdentifier=f'https://{authHost}.{hostname}/oxauth/sectoridentifier/{sector}')
    django_secret = base64.b64encode(secrets.token_urlsafe().encode('utf-8')).decode('utf-8')
    client_id= base64.b64encode(client["client_id"].encode('utf-8')).decode('utf-8')
    client_secret= base64.b64encode(client["client_secret"].encode('utf-8')).decode('utf-8')
    print('Client id: ' + client["client_id"])
    secret = '''
apiVersion: v1
kind: Secret
metadata:
  name: django-secrets
type: Opaque
data:
  DJANGO_SECRET: {django_secret}
  OIDC_RP_CLIENT_ID: {client_id}
  OIDC_RP_CLIENT_SECRET: {client_secret}
'''.format(django_secret=django_secret, client_id=client_id, client_secret=client_secret)
    f = open("django-secrets.yaml", "w")
    f.write(secret)
    f.close()
    print(secret)

if __name__ == "__main__":
    main(str(sys.argv[1]), str(sys.argv[2]))
