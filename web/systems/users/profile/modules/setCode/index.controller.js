 (function() {
    'use strict';

    angular
        .module('users.profile')
        .controller('SetCodeCtrl', SetCodeCtrl);

    SetCodeCtrl.$inject = ['$scope', '$timeout', '$q', '$routeParams', '$location', 'UsersProfile', 'Login'];


    function SetCodeCtrl($scope, $timeout, $q, $routeParams, $location, UsersProfile, Login) {

      //Inicializar componente
      var init = function(){
        $scope.component = {
          disabled: true, //flag para indicar si el formulario esta deshabilitado o no
          message: "Iniciando", //mensaje
          userId: null, //Identificacion de la entidad que esta siendo administrada
          error: false, //flag para indicar que existio un error
        };
        $scope.alerts = [];


      };

      $scope.closeAlert = function(index) {
        $scope.alerts.splice(index, 1);
      }

      $scope.closeAllAlerts = function() {
        $scope.alerts = [];
      }

      var initUser = function(){
        $scope.component.userId = Login.getCredentials()["userId"]
        $scope.component.message = null;
        $scope.component.disabled = false;

        var urlParams = $location.search();
        if("id" in urlParams) {
          $scope.emailId = urlParams["id"];
        } else {
          return;
        }
      }

      //Enviar formulario
      $scope.submit = function(){
        $scope.component.message = "Procesando";
        $scope.closeAllAlerts();

        UsersProfile.processCode($scope.emailId, $scope.code).then(
          function(response){
            $scope.alerts.push({type: 'success', msg: 'El email ha sido confirmado'});
            $scope.$apply();
            $timeout(function() {
              $location.path( "/listEmails");
            }, 2500)

          }, function(error) {
            $scope.alerts.push({type: 'danger', title: 'Error: ', msg:  error.args[0]})
            $scope.$apply();
          }
        )
      }




      //Inicializar
      init();
      $timeout(initUser, 500); //TODO REEMPLAZAR POR EVENTO DE INICIALIZACION DE LOGIN

    }
})();
