 (function() {
    'use strict';

    angular
        .module('tutorias.coordinadores')
        .controller('DetalleTutoriaCtrl', DetalleTutoriaCtrl);

    DetalleTutoriaCtrl.$inject = ['$scope', '$timeout', '$location', 'TutoriasCoordinadores'];

    function DetalleTutoriaCtrl($scope, $timeout, $location, TutoriasCoordinadores) {

      $scope.component = { disabled: false, message: null };
      $scope.tutoria = [];


      //Inicializar tutorias
      $scope.init = function() {
        var urlParams = $location.search();

        return TutoriasCoordinadores.detailTutoria(urlParams["id"]).then(
          function(response){
            $scope.situaciones = response;
            $scope.$apply();
          },
          function(error){ console.log(error); }
        )
      };


      //Inicializar
      $timeout($scope.init, 500); //TODO reemplazar por evento de inicializacion de Login

    }
})();
