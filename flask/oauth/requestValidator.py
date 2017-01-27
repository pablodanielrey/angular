
from oauthlib.common import to_unicode
from oauthlib.oauth1 import RequestValidator

class OAuth1MultipleValidator(RequestValidator):

    def get_realms(self, token, request):
        """
            AuthorizationEndpoint
            AccessTokenEndpoint
            obtiene las realms asociadas con un request token
        """
        ctx.getConn()
        try:
            tk = RequestToken.find(ctx, token=token).fetch(ctx)[0]
            return tk.scopes

        finally:
            ctx.closeConn()

    def validate_timestamp_and_nonce(self, client_key, timestamp, nonce, request_token=None, access_token=None):
        """
            ResourceEndpoint
            AccessTokenEndpoint
            RequestTokenEndpoint
            SignatureOnlyEndpoint
            valida que el nonce no hayan sido usados
        """
        ctx.getConn()
        try:
            ids = Nonce.find(ctx, clientKey=client_key, timestamp=timestamp, nonce=nonce, requestToken=request_token, accessToken=access_token)
            if len(ids.values) > 0:
                return False

            n = Nonce()
            n.clientKey = client_key
            n.timestamp = timestamp
            n.nonce = nonce
            n.requestToken = request_token
            n.accessToken = access_token
            n.persist(ctx)
            ctx.con.commit()
            return True

        finally:
            ctx.closeConn()

    def validate_client_key(self, client_key, request):
        """
            ResourceEndpoint
            AccessTokenEndpoint
            RequestTokenEndpoint
            SignatureOnlyEndpoint

            valida si existe un cliente con esa key
        """
        ctx.getConn()
        try:
            cs = Client.find(ctx, key=client_key).fetch(ctx)
            return True if len(cs) > 0 else False

        finally:
            ctx.closeConn()

    def get_client_secret(self, client_key, request):
        """
            ResourceEndpoint
            AccessTokenEndpoint
            RequestTokenEndpoint
            SignatureOnlyEndpoint

            retorna el secret del cliente
        """
        cs = Client.find(ctx, key=client_key).fetch(ctx)
        return cs[0].secret if len(cs) > 0 else None

    def get_rsa_key(self, client_key, request):
        """
            ResourceEndpoint
            AccessTokenEndpoint
            RequestTokenEndpoint
            SignatureOnlyEndpoint

            None ya que no se implementa rsa
        """
        return None


class OAuth1ResourceValidator(RequestValidator):

    def get_access_token_secret(self, client_key, token, request):
        """
            ResourceEndpoint
            obtiene el secret del access token
        """
        ctx.getConn()
        try:
            tks = AccessToken.find(ctx, clientKey=client_key, token=token).fetch(ctx)
            return tks[0].secret if len(tks) > 0 else None

        finally:
            ctx.closeConn()

    def validate_access_token(self, client_key, token, request):
        """
            ResourceEndpoint
            valida el access token
        """
        ctx.getConn()
        try:
            tks = AccessToken.find(ctx, clientKey=client_key, token=token).fetch(ctx)
            return True if len(tks) > 0 else False

        finally:
            ctx.closeConn()

    def validate_realms(self, client_key, token, request, uri=None, realms=None):
        """
            ResourceEndpoint

            valida que las realms accesibles por el token sean un superconfjunto de las realms a acceder
        """
        ctx.getConn()
        try:
            tks = AccessToken.find(ctx, clientKey=client_key, token=token).fetch(ctx)
            tk = None if len(tks) <= 0 else tks[0]
            if not tk:
                return False
            if realms:
                return set(tk.scopes).issuperset(set(realms))

            ''' si las realms a chequear es None o una lista vacía '''
            return True

        finally:
            ctx.closeConn()



class OAuth1AuthorizationValidator(RequestValidator)

    def save_verifier(self, token, verifier, request):
        """
            AuthorizationEndpoint
            asocia un verificador con un request token
        """
        ctx.getConn()
        try:
            tk = RequestToken.find(ctx, token=token).fetch(ctx)[0]
            tk.verifier = verifier['oauth_verifier']
            tk.persist(ctx)

        finally:
            ctx.closeConn()

    def verify_realms(self, token, realms, request):
        """
            AuthorizationEndpoint
            verifica que las realms que el cliente trata de acceder son las autorizadas para el access token
        """
        if not realms or len(realms) <= 0:
            return False

        ctx.getConn()
        try:
            tks = AccessToken.find(ctx, token=token).fetch(ctx)
            if len(tks) <= 0:
                return False
            if not tk.scopes:
                return False
            return set(tk.scopes).issuperset(set(realms))

        finally:
            ctx.closeConn()

    def verify_request_token(self, token, request):
        """
            AuthorizationEndpoint
            verifica que el request token exista, como este request no es firmado no se puede usar validate_request_token
        """
        ctx.getConn()
        try:
            tks = RequestToken.find(ctx, token=token)
            return len(tks.values) > 0

        finally:
            ctx.closeConn()

    def get_redirect_uri(self, token, request):
        """
            AuthorizationEndpoint
            retorna la uri de redireccion del request token.
            en el caso de ser "oob" se podría retornar una uri especial donde se indica muestra el verifier
        """
        ctx.getConn()
        try:
            tk = RequestToken.find(ctx, token=token).fetch(ctx)[0]
            if tk.redirectUri == 'oob':
                ''' uri de ejemplo '''
                return 'http://127.0.0.1/displayVerifier'
            return tk.redirectUri

        finally:
            ctx.closeConn()


class OAuth1AccessTokenValidator(RequestValidator):

    def invalidate_request_token(self, client_key, request_token, request):
        """
            AccessTokenEndpoint
            invalida el request token
        """
        ctx.getConn()
        try:
            tk = RequestToken.find(ctx, clientKey=client_key, token=request_token).fetch(ctx)[0]
            tk.remove(ctx)
            ctx.con.commit()

        finally:
            ctx.closeConn()

    def validate_request_token(self, client_key, token, request):
        """
            AccessTokenEndpoint
            chequea que el request token sea válido
        """
        ctx.getConn()
        try:
            return len(RequestToken.find(ctx, clientKey=client_key, token=token).values) > 0

        finally:
            ctx.closeConn()

    def validate_verifier(self, client_key, token, verifier, request):
        """
            AccessTokenEndpoint
            valida que el verificador del request token sea válido
        """
        ctx.getConn()
        try:
            ids = RequestToken.find(ctx, clientKey=client_key, token=token, verifier=verifier)
            return len(ids.values) > 0

        finally:
            ctx.closeConn()

    def get_request_token_secret(self, client_key, token, request):
        """
            AccessTokenEndpoint
            obtiene el secret del request token
        """
        ctx.getConn()
        try:
            tk = RequestToken.find(ctx, clientKey=client_key, token=token).fetch(ctx)[0]
            return tk.secret

        finally:
            ctx.closeConn()

    def save_access_token(self, token, request):
        """
            AccessTokenEndpoint
            persiste un access token
        """
        ctx.getConn()
        try:
            tk = AccessToken()
            tk.token = token['oauth_token']
            tk.secret = token['oauth_token_secret']
            tk.scopes = token['oauth_authorized_realms'].split()
            tk.clientKey = request.client_key
            tk.persist(ctx)
            ctx.con.commit()

        finally:
            ctx.closeConn()



class OAuth1RequestTokenValidator(RequestValidator):

    def validate_redirect_uri(self, client_key, redirect_uri, request):
        """
            RequestTokenEndpoint

            valida que la redirección enviada desde el cliente esté permitida
            en el caso de que sea un cliente offline entonces debe setearse en redirect_uri = 'oob'
        """
        ctx.getConn()
        try:
            cs = Client.find(ctx, key=client_key).fetch(ctx)
            c = cs[0] if len(cs) > 0 else None
            if not c:
                return False
            if 'oob' in c.redirectUris:
                return True
            return redirect_uri in c.redirectUris

        finally:
            ctx.closeConn()

    def validate_requested_realms(self, client_key, realms, request):
        """
            RequestTokenEndpoint
            valida que el cliente pueda acceder a las realms requeridas por el cliente
        """
        if not realms or len(realms) <= 0:
            return False

        ctx.getConn()
        try:
            cs = Client.find(ctx, key=client_key).fetch(ctx)
            c = cs[0] if len(cs) > 0 else None
            if not c:
                return False
            if not c.defaultScopes or len(c.defaultScopes) <= 0:
                request.scopes = realms
                return True
            return  set(c.defaultScopes).issuperset(set(realms))

        finally:
            ctx.closeConn()

    def get_default_realms(self, client_key, request):
        """
            RequestTokenEndpoint
            obtiene las realms por defecto para un cliente
        """
        cs = Client.find(ctx, key=client_key).fetch(ctx)
        return cs[0].defaultScopes if len(cs) > 0 else []

    def save_request_token(self, token, request):
        """
            RequestTokenEndpoint
            token = {
                oauth_token: token,
                oauth_token_secret: secret,
                oauth_callback_confirmed: 'true'
            }

            almacena el request token
        """
        ctx.getConn()
        try:
            tk = RequestToken()
            tk.token = token['oauth_token']
            tk.secret = token['oauth_secret']
            tk.clientKey = request.client_key
            tk.persist(ctx)
            ctx.con.commit()

        finally:
            ctx.closeConn()


class OAuth1RequestValidator(RequestValidator):

    @property
    def dummy_client(self):
        return to_unicode('dummy_client', 'utf-8')

    @property
    def dummy_request_token(self):
        return to_unicode('dummy_request_token', 'utf-8')

    @property
    def dummy_access_token(self):
        return to_unicode('dummy_access_token', 'utf-8')
