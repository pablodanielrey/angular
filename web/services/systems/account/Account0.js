var app = angular.module('mainApp');

app.service('Account', function(Messages, Utils, Session, Cache) {

    var self = this;
    this.prefix = 'account_'; //prefijo de identificacion de la cache


    this.resendAccountRequest = function(accounts,ok,err) {
      var msg = {
        "id" : Utils.getId(),
        "requests" : accounts,
        "session" : Session.getSessionId(),
        "action" : "resendAccountRequest",
      };

      Messages.send(msg,
        function(response) {
          if (response.error != undefined) {
            err(response.error);
          } else {
            ok(response.requests);
          }
        });
    }


    this.listAccounts = function(callbackOk, callbackError) {
      var msg = {
  			id: Utils.getId(),
  			session : Session.getSessionId(),
  			action : "listAccountRequests"
		  }

      Messages.send(msg,
          function(response) {
              if (response.error != undefined) {
                callbackError(response.error);
              } else {
                callbackOk(response.requests);
              }
          });
    }

    this.approveAccountsRequest = function(accounts, callbackOk, callbackError) {
        var msg = {
    			"id" : Utils.getId(),
    			"requests" : accounts,
    			"session" : Session.getSessionId(),
    			"action" : "approveAccountRequest",
    		};

        Messages.send(msg,
          function(response) {
            if (response.error != undefined) {
              callbackError(response.error);
            } else {
              callbackOk(response.requests);
            }
          });
        }

    this.removeAccountsRequest = function(accounts, callbackOk, callbackError) {
        var msg = {
    			"id" : Utils.getId(),
    			"requests" : accounts,
    			"session" : Session.getSessionId(),
    			"action" : "removeAccountRequest",
    		};

        Messages.send(msg,
          function(response) {
            if (response.error != undefined) {
              callbackError(response.error);
            } else {
              callbackOk(response.requests);
            }
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

        Messages.send(msg,
          function(response) {
            if (response.error != undefined) {
              callbackError(response.error);
            } else {
              callbackOk(response.requests);
            }
          });
      }
});
