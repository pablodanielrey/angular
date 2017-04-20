 (function() {
    'use strict';

    angular
        .module('tutorias.coordinadores')
        .controller('VerTutoriasCtrl', VerTutoriasCtrl);

    VerTutoriasCtrl.$inject = ['$scope', '$location', '$timeout', 'TutoriasCoordinadores'];

    function VerTutoriasCtrl($scope, $location, $timeout,  TutoriasCoordinadores) {

      $scope.component = { disabled: false, message: null };
      $scope.tutorias = [];

      //Inicializar tutorias
      $scope.init = function() {
        var urlParams = $location.search();

        return TutoriasCoordinadores.getTutorias(urlParams["id"]).then(
          function(response){
            console.log(response);
            $scope.tutorias = response;
            $scope.$apply();
          },
          function(error){ console.log(error); }
        )
      };


      //Inicializar
      $timeout($scope.init, 500); //TODO reemplazar por evento de inicializacion de Login

    }
})();
