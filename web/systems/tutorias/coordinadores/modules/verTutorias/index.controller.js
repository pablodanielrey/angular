 (function() {
    'use strict';

    angular
        .module('tutorias.coordinadores')
        .controller('VerTutoriasCtrl', VerTutoriasCtrl);

    VerTutoriasCtrl.$inject = ['$scope', 'TutoriasCoordinadores'];

    function VerTutoriasCtrl($scope, TutoriasCoordinadores) {

      $scope.component = { disabled: false, message: null };
      $scope.tutorias = [];
       
      //Inicializar tutorias
      $scope.init = function() {
        var urlParams = $location.search();

        return TutoriasCoordinadores.getTutorias(urlParams[id]).then(
          function(response){ return $scope.tutorias = response; },
          function(error){ console.log(error); }
        )
      };


      //Inicializar
      $timeout(init, 500); //TODO reemplazar por evento de inicializacion de Login

    }
})();
