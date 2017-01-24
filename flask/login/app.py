
import flask
import dflask

def configureRoutes(ctx, app):

    @app.route('/algo')
    @dflask.logged
    def algo():
        return flask.render_template('authorize.html')
