(function() {
    'use strict';

    angular
        .module('users')
        .service('Utils', Utils);

    Utils.$inject = ['Users', '$q'];

    /* @ngInject */
    function Utils(Users, $q) {

      //Buscar email alternativo y confirmado del usuario
      //@param id de usuario o null (si esta definido el id buscara el usuario en la base)
      this.findAlternativeAndConfirmedEmail = function(userId){
        return Users.findEmailsByUserId(userId).then(
          function(emails){
            for(var i =0; i < emails.length; i++){
              if(emails[i].confirmed){
                if(emails[i].email.indexOf("@econo") !== -1) continue;
                return emails[i].email;
              }
            }
            return null;
          }
        )
      }


    }
})();
