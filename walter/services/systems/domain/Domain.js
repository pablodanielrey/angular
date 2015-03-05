
var app = angular.module('mainApp');

app.service('Domain', function(Messages, Utils, Session, Cache) {

        var self = this;
        this.prefix = 'domain_'; //prefijo de identificacion de la cache


        this.updatetData = function(data,callbackOk,callbackError) {
                var msg = {
                    id:Utils.getId(),
                    action:'persistDomain',
                    session:Session.getSessionId(),
                    user:data
                }

                Messages.send(msg,
                    function(data) {
                        callbackOk(data);
                    },
                    function(error) {
                        callbackError(error);
                    }
                );

        };

        this.deleteDomainData = function(user_id,callbackOk,callbackError) {
            var msg = {
                    id:Utils.getId(),
                    session: Session.getSessionId(),
                    action:'deleteDomain',
                    user_id:user_id
            };

            Messages.send(msg,
                function(response) {
                    callbackOk(response);
                },
                function(error) {
                    callbackError(error);
                }
            );

        };
)};
