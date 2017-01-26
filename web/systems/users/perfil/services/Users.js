(function() {
    'use strict'
    angular
      .module('users')
      .service('Users',Users);

    Users.inject = ['$rootScope', 'Login', '$q', 'Files'];

    function Users($rootScope, Login, $q, Files) {

      //Administrar (define un usuario para administracion)
      //@param id de usuario o null (si esta definido el id buscara el usuario en la base)
      this.admin = function(id){ return Login.getPrivateTransport().call('users.admin', [id]); }

      //Persistir usuario
      //@param user User a persistir
      this.persist = function(user){ return Login.getPrivateTransport().call('users.persist', [user]); }

      //Buscar emails de usuario
      //@param user User a persistir
      this.findEmailsByUserId = function(userId){ return Login.getPrivateTransport().call('users.find_emails_by_user_id', [userId]); }

      //Agregar email
      //@param email Email a persistir
      this.addEmail = function(email){ return Login.getPrivateTransport().call('users.add_email', [email]); }

      //Eliminar email
      //@param email Email a eliminar
      this.deleteEmail = function(email){ return Login.getPrivateTransport().call('users.delete_email', [email]); }

      //Buscar usuarios por ids
      //@param ids Lista de ids
      this.findByIds = function(ids) {
        if (ids.length <= 0) return $q.when([]);
        return Login.getPrivateTransport().call('users.find_by_ids', [ids]);
      }

      //Enviar codigo de confirmacion por email
      this.sendCode = function(userId){ return Login.getPrivateTransport().call('users.send_code', [userId]); }

      //Procesar codigo de confirmacion
      this.processCode = function(code){ return Login.getPrivateTransport().call('users.process_code', [code]); }

  }
})();
