var app = angular.module('mainApp');

app.service('Account', function(Messages, Utils, Session, Cache) {

    var self = this;
    this.prefix = 'account_'; //prefijo de identificacion de la cache

    this.listAccounts = function(callbackOk, callbackError) {
        var msg = {
			id: Utils.getId(),
			session : Session.getSessionId(),
			action : "listAccountRequests"
		}

        Messages.send(msg,function(response) {
                callbackOk(response.requests);
            },
            function(error) {
                callbackError(error);
            })
    }
});
