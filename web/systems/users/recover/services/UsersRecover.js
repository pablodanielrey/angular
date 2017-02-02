(function() {
    'use strict'
    angular
      .module('users.recover')
      .service('UsersRecover',UsersRecover);

    UsersRecover.inject = ['$rootScope', 'Login', '$q', 'Files'];

    function UsersRecover($rootScope, Login, $q, Files) {

      //Buscar usuario por DNI y enviar codigo
      //@param dni DNI a buscar
      this.sendCodeByDni = function (dni){ return Login.getPrivateTransport().call('users.recover.send_code_by_dni', [dni]); }


  }
})();
