 (function() {
    'use strict';

    angular
        .module('users')
        .controller('ListEmailsCtrl', ListEmailsCtrl);

    ListEmailsCtrl.$inject = ['$scope', '$timeout', 'Users', 'Utils'];


    function ListEmailsCtrl($scope, $timeout, Users, Utils) {

      //Inicializar componente
      function init(){
        $scope.component = {
          disabled: true, //flag para indicar si el formulario esta deshabilitado o no
          message: "Inicializando", //mensaje
          userId: null //Identificacion del usuario que esta siendo administrado
        };

        var urlParams = $location.search();
        if("id" in urlParams) $scope.form.id = urlParams["id"];
      };

      function initUser(){
        $scope.user
        $scope.emails
      }

    }
})();
