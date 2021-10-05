from eoepca_scim import EOEPCA_Scim, ENDPOINT_AUTH_CLIENT_POST
import base64
import sys
import secrets

def main(hostname, sector):
    print("Registering new client in : {hostname}".format(hostname=hostname))
    scim_client = EOEPCA_Scim("https://test.{hostname}".format(hostname=hostname))
    client = scim_client.registerClient(
        "Django-portal",
        grantTypes = ["client_credentials", "password", "urn:ietf:params:oauth:grant-type:uma-ticket"],
        redirectURIs = ["https://portal.{hostname}/oidc/callback/".format(hostname=hostname)],
        logoutURI = "https://portal.{hostname}".format(hostname=hostname),
        responseTypes = ["code","token","id_token"],
        subject_type = 'public',
        scopes = ['openid',  'email', 'user_name ','uma_protection', 'permission', 'is_operator'],
        token_endpoint_auth_method = ENDPOINT_AUTH_CLIENT_POST,
        sectorIdentifier='https://test.{hostname}/oxauth/sectoridentifier/{sector}'.format(hostname=hostname, sector=sector))
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
    main(sys.argv[1], sys.argv[2])
