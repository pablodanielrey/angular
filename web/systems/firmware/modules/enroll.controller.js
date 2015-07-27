angular
  .module('mainApp')
  .controller('EnrollCtrl',EnrollCtrl);

EnrollCtrl.$inject = ['$rootScope','$scope','$location','$timeout','Notifications', 'Firmware'];

function EnrollCtrl($rootScope, $scope, $location, $timeout, Notifications, Firmware) {

    var vm = this;

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

      if ($scope.$parent.logData == undefined || $scope.$parent.logData.sid == undefined) {
        Notifications.message('Error de Sistema');
        $scope.cancel()
      }

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



    $scope.fingerRequested = function(data) {
      var t = '';
      if (data == 1) {
        t = 'primera';
      }

      if (data == 2) {
        t = 'segunda';
      }

      if (data == 3) {
        t = 'tercera';
      }

      $scope.model.msg = 'Coloque el dedo en el lector de huellas por ' + t + ' vez';
    };

    $scope.templateEnrolled = function(data) {
      console.log(data);
      $scope.messageEvent(['Usuario correctamente enrolado']);
    }

    $scope.errorEvent = function(msg) {
      console.log(msg);
      Notifications.message(msg[0]);
    }

    $scope.messageEvent = function(msg) {
      console.log(msg);
      $scope.model.msg = msg[0];
    }


    // registro los eventos en el Firmware
    Firmware.onEnrollEvents($scope.fingerRequested, $scope.messageEvent, $scope.templateEnrolled, $scope.errorEvent, $scope.errorEvent);



    $scope.cancel = function() {
      if ($scope.$parent.logData) {
        $scope.$parent.logData = null;
      }
      $location.path('/firmware')
    }

};
