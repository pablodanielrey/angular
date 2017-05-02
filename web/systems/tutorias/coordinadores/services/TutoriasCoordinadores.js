(function() {
    'use strict'
    angular
      .module('tutorias.coordinadores')
      .service('TutoriasCoordinadores', TutoriasCoordinadores);

    TutoriasCoordinadores.inject = ['$rootScope', 'Login', '$q', 'Files', '$cookies'];

    function TutoriasCoordinadores($rootScope, Login, $q, Files, $cookies) {


      //Buscar todas las tutorias asociadas al coordinador logueado
      //@return List<Tutorias>
      this.getTutorias = function (){
         var auth = $cookies.getObject('authfce');
         console.log(auth);
         return Login.getPrivateTransport().call('tutorias.coordinadores.get_tutorias', [auth.user_id]);
       }

      //@return Tutorias
      this.detailTutoria = function (id){ return Login.getPrivateTransport().call('tutorias.coordinadores.detail_tutoria', [id]); }



  }
})();
