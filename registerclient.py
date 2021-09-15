from eoepca_scim import EOEPCA_Scim, ENDPOINT_AUTH_CLIENT_POST
from WellKnownHandler import TYPE_OIDC, KEY_OIDC_SUPPORTED_AUTH_METHODS_TOKEN_ENDPOINT
from jwkest.jwk import RSAKey, import_rsa_key
import base64
import sys
import secrets

class CustomEOEPCA_SCIM(EOEPCA_Scim):
    def clientPayloadCreation(self, clientName, grantTypes, redirectURIs, logoutURI, responseTypes, scopes, sectorIdentifier, token_endpoint_auth_method, useJWT=0):
        # Check the auth method is allowed by Auth Server.
        # Since this value can change dynamically, we check it each time this function is called.
        allowed_auth_methods = self.wkh.get(TYPE_OIDC, KEY_OIDC_SUPPORTED_AUTH_METHODS_TOKEN_ENDPOINT)
        if token_endpoint_auth_method not in allowed_auth_methods:
            raise Exception("Auth method '"+token_endpoint_auth_method+"' is not currently allowed by Auth Server: "+str(allowed_auth_methods))

        payload = "{ \"client_name\": \"" + clientName + "\", \"subject_type\":\"public\", \"grant_types\":["
        for grant in grantTypes:
            payload += "\"" + grant.strip() + "\", "
        payload = payload[:-2] + "], \"redirect_uris\" : ["
        for uri in redirectURIs:
            payload += "\"" + uri.strip() + "\", "
        payload = payload[:-2] + "], \"post_logout_redirect_uris\": [\""+ logoutURI +"\"], \"scope\": \""
        for scope in scopes:
            payload += scope.strip() + " "
        payload = payload[:-1] + "\", "
        if sectorIdentifier is not None:
            payload += "\"sector_identifier_uri\": "
            payload += "\"" + sectorIdentifier.strip() + "\", "
            payload = payload[:-2] + ", "
        payload += "\"response_types\": [  "
        for response in responseTypes:
            payload += "\"" + response.strip() + "\",  "
        payload = payload[:-2] + "]"
        if useJWT == 1:
            payload += ", \"jwks\": {\"keys\": [ " + str(RSAKey(kid=self._kid, key=import_rsa_key(self.__getRSAPublicKey()))) + "]}"
        payload += ", \"token_endpoint_auth_method\": \""+token_endpoint_auth_method+"\""
        payload += "}"
        return payload

def main(hostname, sector):
    print("Registering new client in : {hostname}".format(hostname=hostname))
    scim_client = CustomEOEPCA_SCIM("https://test.{hostname}".format(hostname=hostname))
    client = scim_client.registerClient(
        "Django-portal",
        grantTypes = ["client_credentials", "password", "urn:ietf:params:oauth:grant-type:uma-ticket"],
        redirectURIs = ["https://portal.{hostname}/oidc/callback/".format(hostname=hostname)],
        logoutURI = "",
        responseTypes = ["code","token","id_token"],
        scopes = ['openid',  'email', 'user_name ','uma_protection', 'permission'],
        token_endpoint_auth_method = ENDPOINT_AUTH_CLIENT_POST,
        sectorIdentifier='https://test.{hostname}/oxauth/sectoridentifier/{sector}'.format(hostname=hostname, sector=sector))
    django_secret = base64.b64encode(secrets.token_urlsafe().encode('utf-8')).decode('utf-8')
    client_id= base64.b64encode(client["client_id"].encode('utf-8')).decode('utf-8')
    client_secret= base64.b64encode(client["client_secret"].encode('utf-8')).decode('utf-8')

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
