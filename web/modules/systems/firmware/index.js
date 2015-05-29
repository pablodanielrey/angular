var app = angular.module('mainApp');

app.controller("IndexCtrl", ['$scope','$timeout','$location','Notifications', 'Firmware',function($scope, $timeout, $location, Notifications, Firmware) {

  $scope.model = {
    date:new Date(),
    day:'',
    hours:'',
    displayCodeContainer: false,
    displayInfoContainer: true,
    enabledCommit: false,
    code: '',
    displayInputCode: false,
    displayPassword: false
  }

  $scope.initialize = function() {
    $scope.updateDate();
    $scope.updateDay();
    $scope.model.displayCodeContainer = false;
    $scope.model.displayInfoContainer = true;
    $scope.model.enabledCommit = false;
    $scope.model.code = '';
    $scope.model.displayInputCode = false;
    $scope.model.displayPassword = false;
  }

  /* ----------------------------------------------------------
   * ------------- ACTUALIZACION DEL RELOJ --------------------
   * ----------------------------------------------------------
   */

  $scope.updateDay = function() {
    var options = {
        weekday: "long",
        year: "numeric",
        month: "2-digit",
        day: "numeric"
    };

    $scope.model.day = $scope.model.date.toLocaleDateString('es',options);
  }

  $scope.setHours = function() {
    var hs = ('0' + $scope.model.date.getHours()).slice(-2);
    var min = ('0' + $scope.model.date.getMinutes()).slice(-2);
    var sec = ('0' + $scope.model.date.getSeconds()).slice(-2);
    $scope.model.hours = hs + ":" + min + ":" + sec;
  }

  $scope.updateDate = function() {
    var day = $scope.model.date.getDay();

    $scope.model.date = new Date();
    $scope.setHours();

    if (day != $scope.model.date.getDay()) {
        $scope.updateDay();
    }


    $timeout(function() {
      $scope.updateDate();
    }, 1000);
  }


  /* ----------------------------------------------------------
   * ---------------- Ingreso del codigo ----------------------
   * ----------------------------------------------------------
   */

  $scope.redirect = function() {
    $location.path('/enroll')
  }


  $scope.enterCode = function() {
    $scope.model.displayInputCode = false;
    $scope.model.displayPassword = true;
  }

  $scope.$watch('model.code', function(newValue, oldValue) {

    var isZero = newValue == '0' && (oldValue == null || oldValue.trim() == '');
    var isNotNumber = isNaN(newValue);
    if (isZero || isNotNumber || newValue.indexOf('.') > -1) {
      $scope.model.code = oldValue;
    }

    if ($scope.model.code == null || $scope.model.code.trim() == '') {
      $scope.model.enabledCommit = false;
    } else {
      $scope.model.enabledCommit = true;
    }
   });

  $scope.addNumber = function(number) {
    if ($scope.model.displayInfoContainer) {
      $scope.model.displayInfoContainer = false;
      $scope.model.displayCodeContainer = true;
      $scope.model.enabledCommit = true;
      $scope.model.displayInputCode = true;
      $scope.model.displayPassword = false;
    }

    if ($scope.model.code == null) {
        $scope.model.code = '';
    }

    $scope.model.code += number;
  }

  $scope.cancel = function() {
    $scope.model.code = '';
    $scope.model.displayCodeContainer = false;
    $scope.model.displayInfoContainer = true;
    $scope.model.enabledCommit = false;
    $scope.model.displayInputCode = false;
    $scope.model.displayPassword = false;
  }

  $scope.deleteNumber = function() {
    $scope.model.code = ($scope.model.code == null || $scope.model.code.trim() == '') ? null : $scope.model.code.substring(0, $scope.model.code.length-1);
  }

  /* ----------------------------------------------------------
   * ------------- Manejo visual de la pantalla ---------------
   * ----------------------------------------------------------
   */

  $scope.isDisplayCodeContainer = function() {
    return $scope.model.displayCodeContainer;
  }

  $scope.isDisplayInputCode = function() {
    return $scope.model.displayInputCode;
  }

  $scope.isDisplayInputPassword = function() {
    return $scope.model.displayPassword;
  }

  $scope.isDisplayInfoContainer = function() {
    return $scope.model.displayInfoContainer;
  }

  $scope.isEnabledCommit = function() {
    return $scope.model.enabledCommit;
  }


  $scope.initialize();

}]);
