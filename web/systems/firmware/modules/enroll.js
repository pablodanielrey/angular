var app = angular.module('mainApp');

app.controller("EnrollCtrl", ['$rootScope','$scope','$location','$timeout','Notifications', 'Firmware',
  function($rootScope,$scope, $location, $timeout, Notifications, Firmware) {

    $scope.model = {
      dni:null,
      fingerNumber:0,
      msg:'',
      fingers:0,
      enabled : false,
      cancel : true
    }


    $scope.initialize = function() {
      $scope.model.dni = null;
      $scope.model.fingers = 0;
      $scope.model.fingerNumber = 0;
      $scope.model.msg = '';
      $scope.model.enabled = false;
      $scope.model.cancel = true;
    }

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });



    /* -------------------------------------------
     * ---------- TECLADO NUMERICO ---------------
     * -------------------------------------------
     */

    $scope.addNumber = function(n) {
      if (n == '0' && ($scope.model.dni == null || $scope.model.dni.length == 0)) {
          return;
      }

      $scope.model.dni = ($scope.model.dni == null) ? n : $scope.model.dni + n;
      $scope.model.enabled = !($scope.model.dni == null || $scope.model.dni.trim() == '');
    }

    $scope.deleteNumber = function() {
      $scope.model.dni = ($scope.model.dni == null || $scope.model.dni.length == 0) ? null : $scope.model.dni.substring(0, $scope.model.dni.length-1);
      $scope.model.enabled = !($scope.model.dni == null || $scope.model.dni.trim() == '');
    }





    $scope.addUser = function() {
      $scope.model.enabled = false;
      $scope.model.cancel = false;
      Firmware.enroll($scope.model.dni,
        function(response) {
           Notifications.message("Las huellas del usuario " + $scope.model.dni + " se han guardado exitosamente");
           //$scope.model.msg = "El usuario " + $scope.model.dni + " se ha creado exitosamente";
           $scope.initialize();
        },
        function(error) {
           Notifications.message(error);
           $scope.initialize();
        }
      );
    }



    $scope.$on('FingerRequestedEvent', function(event, data) {
      var t = '';
      if (data.fingerNumber == 1) {
        t = 'primera';
      }

      if (data.fingerNumber == 2) {
        t = 'segunda';
      }

      if (data.fingerNumber == 3) {
        t = 'tercera';
      }

      $scope.model.msg = 'Coloque el dedo en el lector de huellas por ' + t + ' vez';
    })

    $scope.$on('ErrorEvent', function(event, data) {
      Notifications.message(data.msg);
    })

    $scope.$on('MsgEvent', function(event, data) {
      if (data && data.msg) {
        //Notifications.message(data.msg);
        $scope.model.msg = data.msg;
        return;
      }
    })

    $scope.cancel = function() {
      $location.path('/firmware')
    }

  }
])
