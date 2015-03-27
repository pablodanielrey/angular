var app = angular.module('mainApp');

app.service('Mail', function(Messages, Utils, Session, Cache) {

        var self = this;
        this.prefix = 'mail_';//prefijo de identificacion de la cache

        this.updateData = function(data,callbackOk,callbackError) {
            var msg = {
                id:Utils.getId(),
                action:'persistUserMailEcono',
                session:Session.getSessionId(),
                mail:data
            };

            Messages.send(msg,
                function(data) {
                    callbackOk(data.mail);
                },
                function(error) {
                    callbackError(error);
                }
            );
        };

        this.daleteMailData = function(user_id,callbackOk,callbackError) {
                console.log("Eliminando mail");
                var msg = {
                    id:Utils.getId(),
                    session:Session.getSessionId(),
                    action:'deleteInstitutionalMail',
                    user_id:user_id
                };

                Messages.send(msg,
                    function(response) {
                        callbackOk(response.mail);
                    },
                    function(error) {
                        callbackError(error);
                    }
                );
        };

        this.findMailData = function(user_id,callbackOk,callbackError) {
            var msg = {
                id:Utils.getId(),
                session:Session.getSessionId(),
                action:'findInstitutionalMailData',
                user_id:user_id
            };

            Messages.send(msg,
                function(response) {
                    callbackOk(response.mail);
                },
                function(error) {
                    callbackError(error)
                }
            );
        }
});
