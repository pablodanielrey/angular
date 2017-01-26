(function() {
    'use strict'
    angular
      .module('users.profile')
      .service('UsersProfile',UsersProfile);

    UsersProfile.inject = ['$rootScope', 'Login', '$q', 'Files'];

    function UsersProfile($rootScope, Login, $q, Files) {

      //Buscar usuario
      //@param id de usuario o null (si esta definido el id buscara el usuario en la base)
      this.findById = function(id){ return Login.getPrivateTransport().call('users.profile.find_by_id', [id]); }

      //Persistir usuario
      //@param user User a persistir
      this.persist = function(user){ return Login.getPrivateTransport().call('users.profile.persist', [user]); }

      //Buscar emails de usuario
      //@param user User a persistir
      this.findEmailsByUserId = function(userId){ return Login.getPrivateTransport().call('users.profile.find_emails_by_user_id', [userId]); }

      //Agregar email
      //@param email Email a persistir
      this.addEmail = function(email){ return Login.getPrivateTransport().call('users.profile.add_email', [email]); }

      //Eliminar email
      //@param email Email a eliminar
      this.deleteEmail = function(email){ return Login.getPrivateTransport().call('users.profile.delete_email', [email]); }

      //Enviar codigo de confirmacion por email
      this.sendCode = function(userId){ return Login.getPrivateTransport().call('users.profile.send_code', [userId]); }

      //Procesar codigo de confirmacion
      this.processCode = function(code){ return Login.getPrivateTransport().call('users.profile.process_code', [code]); }

  }
})();
