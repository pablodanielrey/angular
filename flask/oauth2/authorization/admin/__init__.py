
import flask

from model.oauth.oauth import OAuth1Model
from model.oauth.entities.oauth import Client

def createAdminViews(app, ctx):

    @app.route('/clients', methods=['GET','POST'])
    def client_handler():
        ctx.getConn()
        clients = Client.find(ctx).fetch(ctx)
        print(clients)

        if flask.request.method == 'POST':
            c = OAuth1Model.createClient(ctx)
            clients.append(c)
            ctx.con.commit()

        ctx.closeConn()
        return flask.render_template('client_list.html', clients=clients)
