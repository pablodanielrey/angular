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

    this.approveAccountsRequest = function(accounts, callbackOk, callbackError) {
        var msg = {
			"id" : Utils.getId(),
			"requests" : accounts,
			"session" : Session.getSessionId(),
			"action" : "approveAccountRequest",
		};

        Messages.send(msg,function(response) {
            callbackOk(response);
        },
        function(error) {
            callbackError(error);
        });
    }

    this.removeAccountsRequest = function(accounts, callbackOk, callbackError) {
        var msg = {
			"id" : Utils.getId(),
			"requests" : accounts,
			"session" : Session.getSessionId(),
			"action" : "removeAccountRequest",
		};

        Messages.send(msg,function(response) {
            callbackOk(response);
        },
        function(error) {
            callbackError(error);
        });
    }

    this.rejectAccountRequest = function(accountId,description,callbackOk, callbackError) {
        var msg = {
			"id" : Utils.getId(),
			"reqId" : accountId,
			"session" : Session.getSessionId(),
			"description" : description,
			"action" : "rejectAccountRequest",
		};

        Messages.send(msg,function(response) {
            callbackOk(response);
        },
        function(error) {
            alert(error);
        });
    }
});
