(function() {
    'use strict'
    angular
      .module('offices.admin')
      .service('OfficesAdmin',OfficesAdmin);

    OfficesAdmin.inject = ['$rootScope', 'Login', '$q', 'Files'];

    function OfficesAdmin($rootScope, Login, $q, Files) {

      //Buscar usuarios a partir de un string
      //@param search Busqueda
      this.getOffices = function (){ return Login.getPrivateTransport().call('offices.admin.get_offices', []); }

      //Administrar oficina
      //@param id Identificador de oficina, si es nulo, devolvera una instancia de oficina vacia
      this.admin = function (id){ return Login.getPrivateTransport().call('offices.admin.admin', [id]); }

      //Persistir oficina
      //@param office Oficina a persistir
      this.persist = function (office){ return Login.getPrivateTransport().call('offices.admin.persist', [office]); }


      //Buscar usuarios
      //@param id Identificador de oficina, si es nulo, devolvera una instancia de oficina vacia
      this.searchUsers = function (search){ return Login.getPrivateTransport().call('offices.admin.search_users', [search]); }

      //Buscar usuarios de una determinada oficina
      //@param officeId Identificador de oficina
      this.getUsers = function (officeId){ return Login.getPrivateTransport().call('offices.admin.get_users', [officeId]); }


      //Agregar usuario a una oficina
      //@param officeId Identificador de oficina
      //@param userId Identificador de usuario
      this.addUser = function (officeId, userId){ return Login.getPrivateTransport().call('offices.admin.add_user', [officeId, userId]); }

      //Eliminar usuario de una oficina
      //@param officeId Identificador de oficina
      //@param userId Identificador de usuario
      this.deleteUser = function (officeId, userId){ return Login.getPrivateTransport().call('offices.admin.delete_user', [officeId, userId]); }


  }
})();
