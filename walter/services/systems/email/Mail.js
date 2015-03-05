var app = angular.module('mainApp');

app.service('Mail', function(Messages, Utils, Session, Cache) {

        var self = this;
        this.prefix = 'mail_';//prefijo de identificacion de la cache

        this.updateData = function(data,callbackOk,callbackError) {
            var msg = {
                id:Utils.getId(),
                action:'persistUserMailEcono',
                session:Session.getSessionId(),
                user:data
            };

            Messages.send(msg,
                function(data) {
                    callbackOk(data);
                },
                function(error) {
                    callbackError(error);
                }
            );
        };

        this.daleteMailData = function(user_id,callbackOk,callbackError) {
                var msg = {
                    id:Utils.getId(),
                    session:Session.getSessionId(),
                    action:'daleteMailEcono',
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
