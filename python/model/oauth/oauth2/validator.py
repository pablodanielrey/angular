
from oauthlib.oauth2 import RequestValidator

class AuthorizationCodeGrantValidator(RequestValidator):

    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    def authenticate_client(request, *args, **kwargs):
        """
            Authorization Code Grant
            Resource Owner Password Credentials Grant (may be disabled)
            Client Credentials Grant
            Refresh Token Grant

            Retorna True|False
            headers accesible mediante : request.headers
            parámetros : request.client_id --> parámetro en la url client_id
        """

        ''' cache usado en otros lados '''
        request.client = Client()
        return True

    def authenticate_client_id(client_id, request, *args, **kwargs):
        """
            Authorization Code Grant
            cheqeua que el cliente sea un cliente "no confidencial"
            retorna True|False
        """
        self.ctx.getConn()
        try:
            c = Client.find(ctx, id=client_id).fetch(ctx)[0]
            return c.type == Client.TYPES[Client.PUBLIC]

        finally:
            self.ctx.closeConn()
        return True

    def client_authentication_required(request, *args, **kwargs):
        """
            Authorization Code Grant
            Resource Owner Password Credentials Grant
            Refresh Token Grant
            determina si es requerida autenticación para un determinado request (ver https://oauthlib.readthedocs.io/en/latest/oauth2/validator.html)

            According to the rfc6749, client authentication is required in the
            following cases:

            Resource Owner Password Credentials Grant: see `Section 4.3.2`_.
            Authorization Code Grant: see `Section 4.1.3`_.
            Refresh Token Grant: see `Section 6`_.

            .. _`Section 4.3.2`: http://tools.ietf.org/html/rfc6749#section-4.3.2
            .. _`Section 4.1.3`: http://tools.ietf.org/html/rfc6749#section-4.1.3
            .. _`Section 6`: http://tools.ietf.org/html/rfc6749#section-6
        """
        if request.grant_type not in ['autorization_code', 'password', 'refresh_token']:
            return False

        self.ctx.getConn()
        try:
            cs = Client.find(ctx, id=request.client_id).fetch(ctx)
            if len(cs) <= 0:
                return True
            return cs[0].type == Client.TYPES[Client.CONFIDENTIAL]

        finally:
            self.ctx.closeConn()

        return True

    def confirm_redirect_uri(client_id, code, redirect_uri, client, *args, **kwargs):
        """
            Authorization Code Grant (during token request)
            Asegura que el proceso de autorización representado por el codigo se inicia con la redirect_uri
        """
        return True

    def get_default_redirect_uri(client_id, request, *args, **kwargs):
        """
            Authorization Code Grant
            Implicit Grant
            Obtiene la url por defecto de redirección para un determinado cliente
        """
        self.ctx.getConn()
        try:
            c = Client.find(ctx, id=client_id).fetch(ctx)[0]
            return c.redirectUri

        finally:
            self.ctx.closeConn()

    def get_default_scopes(client_id, request, *args, **kwargs):
        """
            Authorization Code Grant
            Implicit Grant
            Resource Owner Password Credentials Grant
            Client Credentials grant
            obtiene los scopes por deefecto para un determinado cliente
        """
        self.ctx.getConn()
        try:
            c = Client.find(ctx, id=client_id).fetch(ctx)[0]
            return c.scopes

        finally:
            self.ctx.closeConn()

    def invalidate_authorization_code(client_id, code, request, *args, **kwargs):
        """
            Authorization Code Grant
            invalida un codigo de autorización
        """
        self.ctx.getConn()
        try:
            tk = AuthorizationToken.find(ctx, clientId=client_id, token=code).fetch(ctx)[0]
            tk.delete(ctx)
            self.ctx.con.commit()

        finally:
            self.ctx.closeConn()

    def save_authorization_code(client_id, code, request, *args, **kwargs):
        """
            Authorization Code Grant
            almacena el codigo de autorización
        """
        self.ctx.getConn()
        try:
            tk = AuthorizationToken()
            tk.clientId = client_id
            tk.redirectUri = request.redirect_uri
            tk.userId = request.user.id if resquest.user else None
            tk.scopes = request.scopes
            tk.state = code.get('state')
            tk.token = code.get('code')
            tk.persist(ctx)
            self.ctx.con.commit()

        finally:
            self.ctx.closeConn()

    def save_bearer_token(token, request, *args, **kwargs):
        """
            Authorization Code Grant
            Implicit Grant
            Resource Owner Password Credentials Grant (might not associate a client)
            Client Credentials grant
            almacena el bearer token
        """
        assert token.get('token_type') == 'Bearer'
        self.ctx.getConn()
        try:
            tk = BearerToken()
            tk.token = .get('access_token')
            tk.refreshToken = token.get('refresh_token')
            tk.userId = request.user.id if resquest.user else None
            tk.clientId = request.client_id
            tk.scopes = token.get('scope').split() if 'scope' in token else []
            tk.state = token.get('state')
            tk.expires = datetime.datetime.now() + datetime.timedelta(seconds=token.get('expires_in'))
            tk.persist(ctx)
            self.ctx.con.commit()

        finally:
            self.ctx.closeConn()

    def validate_bearer_token(token, scopes, request):
    """
        Authorization Code Grant
        Implicit Grant
        Resource Owner Password Credentials Grant
        Client Credentials Grant
        asegura que el token sea válido y autorice todos los scopes requeridos
    """
        self.ctx.getConn()
        try:
            tks = BearerToken.find(ctx, token=token).fetch(ctx)

            if len(tks) <= 0:
                return False

            tk = tks[0]
            if datetime.datetime.now() > tk.expires:
                tk.delete(ctx)
                self.ctx.con.commit()
                return False

            return set(tk.scopes).issuperset(set(scopes))

        finally:
            self.ctx.closeConn()

    def validate_client_id(client_id, request, *args, **kwargs):
        """
            Authorization Code Grant
            Implicit Grant
            chequea que el client_id perterenzca a un cliente válido
        """
        self.ctx.getConn()
        try:
            cs = Client.find(ctx, id=client_id).fetch(ctx)
            if len(cs) <= 0:
                return False

            request.client = cs[0]
            return True

        finally:
            self.ctx.closeConn()

    def validate_code(client_id, code, client, request, *args, **kwargs):
        """
            Authorization Code Grant
            verifica que el codigo de autorización sea válido y asignado al cliente
        """
        self.ctx.getConn()
        try:
            tks = AuthorizationToken.find(ctx, clientId=client_id, token=code).fetch(ctx)
            if len(tks) <= 0:
                return False

            ''' para chache '''
            tk = tks[0]
            request.user = User.find(ctx, id=tk.userId).fetch(ctx)[0]
            request.state = tk.state
            request.scopes = tk.scopes
            #request.claims = None
            return True

        finally:
            self.ctx.closeConn()

    def validate_grant_type(client_id, grant_type, client, request, *args, **kwargs):
        """
            Authorization Code Grant
            Resource Owner Password Credentials Grant
            Client Credentials Grant
            Refresh Token Grant
            chequea que el cliente tenga acceso al grant requerido
        """
        assert client_id == client.id
        return grant_type in client.grants

    def validate_redirect_uri(client_id, redirect_uri, request, *args, **kwargs):
        """
            Authorization Code Grant
            Implicit Grant
            asegura que el cliente tiene permitido la redireccion a redirect_uri
        """
        self.ctx.getConn()
        try:
            cs = Client.find(ctx, id=client_id).fetch(ctx)
            if len(cs) <= 0:
                return False
            return redirect_uri == cs[0].redirectUri

        finally:
            self.ctx.closeConn()

    def validate_refresh_token(refresh_token, client, request, *args, **kwargs):
        """
            Authorization Code Grant (indirectly by issuing refresh tokens)
            Resource Owner Password Credentials Grant (also indirectly)
            Refresh Token Grant
            asegura que el refresh_token sea valido y asignado al cliente
        """
        self.ctx.getConn()
        try:
            tks = BearerToken.find(ctx, clientId=client.id, refreshToken=refresh_token).fetch(ctx)
            if len(tks) <= 0:
                return False

            ''' para chache '''
            tk = tks[0]
            request.user = User.find(ctx, id=tk.userId).fetch(ctx)[0]
            return True

        finally:
            self.ctx.closeConn()

    def validate_response_type(client_id, response_type, client, request, *args, **kwargs):
        """
            Authorization Code Grant
            Implicit Grant
            asegura que el response type esta permitido
        """
        self.ctx.getConn()
        try:
            cs = Client.find(ctx, id=client_id).fetch(ctx)
            if len(cs) <= 0:
                return False
            return response_type in cs[0].responseTypes

        finally:
            self.ctx.closeConn()

    def validate_scopes(client_id, scopes, client, request, *args, **kwargs):
        """
            Authorization Code Grant
            Implicit Grant
            Resource Owner Password Credentials Grant
            Client Credentials Grant
            valida que el cliente tenga permiso para acceder a los scopes requeridos
        """
        assert client_id == client.id
        return set(client.scopes).issuperset(set(scopes))
