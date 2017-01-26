(function() {
    'use strict'
    angular
      .module('users.admin')
      .service('UsersAdmin',UsersAdmin);

    UsersAdmin.inject = ['$rootScope', 'Login', '$q', 'Files'];

    function UsersAdmin($rootScope, Login, $q, Files) {

      //Buscar usuarios a partir de un string
      //@param search Busqueda
      this.search = function (search){ return Login.getPrivateTransport().call('users.admin.search', [search]); }

      //Administrar (define un usuario para administracion)
      //@param id de usuario o null (si esta definido el id buscara el usuario en la base)
      this.admin = function(id){ return Login.getPrivateTransport().call('users.admin.admin', [id]); }

      //Persistir usuario
      //@param user User a persistir
      this.persist = function(user){ return Login.getPrivateTransport().call('users.admin.persist', [user]); }

      //Buscar emails de usuario
      //@param user User a persistir
      this.findEmailsByUserId = function(userId){ return Login.getPrivateTransport().call('users.admin.find_emails_by_user_id', [userId]); }

      //Agregar email
      //@param email Email a persistir
      this.addEmail = function(email){ return Login.getPrivateTransport().call('users.admin.add_email', [email]); }

      //Eliminar email
      //@param email Email a eliminar
      this.deleteEmail = function(email){ return Login.getPrivateTransport().call('users.admin.delete_email', [email]); }

      //Buscar por ids
      //@param ids Lista de ids a buscar
      this.findByIds = function(ids) {
        if (ids.length <= 0) return $q.when([]);
        return Login.getPrivateTransport().call('users.admin.find_by_ids', [ids]);
      }

  }
})();
