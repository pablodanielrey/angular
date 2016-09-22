
var app = angular.module('mainApp');

app.service('Domain', function(Messages, Utils, Session, Cache) {

        var self = this;
        this.prefix = 'domain_'; //prefijo de identificacion de la cache


        this.updateData = function(data,callbackOk,callbackError) {
                var msg = {
                    id:Utils.getId(),
                    action:'persistDomainData',
                    session:Session.getSessionId(),
                    domain:data
                }

                Messages.send(msg,
                    function(data) {
                        callbackOk(data.domain);
                    },
                    function(error) {
                        callbackError(error);
                    }
                );

        }

        this.deleteDomainData = function(user_id,callbackOk,callbackError) {
            var msg = {
                    id:Utils.getId(),
                    session: Session.getSessionId(),
                    action:'deleteDomainData',
                    user_id:user_id
            };

            Messages.send(msg,
                function(response) {
                    callbackOk(response.domain);
                },
                function(error) {
                    callbackError(error);
                }
            );

        }

        this.findDomainData = function(user_id,callbackOk,callbackError) {
            var msg = {
                id:Utils.getId(),
                session:Session.getSessionId(),
                action:'findDomainData',
                user_id:user_id
            };

            Messages.send(msg,
                function(response) {
                    callbackOk(response.domain);
                },
                function(error) {
                    callbackError(error)
                }
            );
        }
});
