(function() {
    'use strict'
    angular
      .module('tutorias.coordinadores')
      .service('TutoriasCoordinadores', TutoriasCoordinadores);

    TutoriasCoordinadores.inject = ['$rootScope', 'Login', '$q', 'Files'];

    function TutoriasCoordinadores($rootScope, Login, $q, Files) {


      //Buscar todas las tutorias asociadas al coordinador logueado
      //@return List<Tutorias>
      this.getTutorias = function (userId){
         console.log(userId)
         return Login.getPrivateTransport().call('tutorias.coordinadores.get_tutorias', [userId]);
       }

      //@return Tutorias
      this.detailTutoria = function (id){ return Login.getPrivateTransport().call('tutorias.coordinadores.detail_tutoria', [id]); }



  }
})();
