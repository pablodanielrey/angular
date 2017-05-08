 (function() {
    'use strict';

    angular
        .module('tutorias.coordinadores')
        .controller('DetalleTutoriaCtrl', DetalleTutoriaCtrl);

    DetalleTutoriaCtrl.$inject = ['$scope', '$timeout', '$location', 'TutoriasCoordinadores'];

    function DetalleTutoriaCtrl($scope, $timeout, $location, TutoriasCoordinadores) {

      $scope.component = { disabled: false, message: null };
      $scope.tutoria = [];
      $scope.sortVal = "user.lastname";


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

      $scope.setSort = function(sort){
         if($scope.sortVal == sort){
             $scope.sortDir = !$scope.sortDir;
         } else {
             $scope.sortVal = sort;
             $scope.sortDir = true;
         }
      }



      //Inicializar
      $timeout($scope.init, 500); //TODO reemplazar por evento de inicializacion de Login

    }
})();
