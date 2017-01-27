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

      //Buscar usuarios
      //@param id Identificador de oficina, si es nulo, devolvera una instancia de oficina vacia
      this.searchUsers = function (search){ return Login.getPrivateTransport().call('offices.admin.search_users', [search]); }

      //Buscar designaciones de una determinada oficina
      //@param officeId Identificador de oficina
      this.getDesignations = function (officeId){ return Login.getPrivateTransport().call('offices.admin.get_designations', [officeId]); }


  }
})();
