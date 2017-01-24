
def configureRoutes(ctx, app):
    import flask
    from flask import Flask

    import dflask
    from model.users.entities.user import User
    from model.users.entities.userPassword import UserPassword

    @app.route('/', methods=['GET'])
    def index():
        if dflask.is_logged():
            user = dflask.current_user()
            return flask.render_template('login.html', user='{} {}'.format(user.name, user.lastname))
        else:
            return flask.render_template('login.html')

    @app.route('/login', methods=['GET','POST'])
    def login():
        if flask.request.method == 'POST':
            u = flask.request.form.get('u')
            p = flask.request.form.get('p')
            ctx.getConn()
            try:
                users = UserPassword.find(ctx, username=[u], password=[p]).fetch(ctx)
                print(users)
                for up in users:
                    user = User.find(ctx, id=[up.userId]).fetch(ctx)[0]
                    dflask.login(user)
                    return index()
            finally:
                ctx.closeConn()

            return flask.render_template('login.html', error='Usuario y/o Clave inválidos')

        return index()

    @app.route('/logout', methods=['GET','POST'])
    def logout():
        dflask.logout()
        return flask.redirect('/')
