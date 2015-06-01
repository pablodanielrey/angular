var app = angular.module('mainApp');

app.controller("IndexCtrl", ['$rootScope','$scope','$timeout','$location','Notifications', 'Firmware',function($rootScope,$scope, $timeout, $location, Notifications, Firmware) {

  $scope.model = {
    date:new Date(),
    day:'',
    hours:'',
    seconds:'',
    displayCodeContainer: false,
    displayInfoContainer: true,
    enabledCommit: false,
    code: '',
    displayInputCode: false,
    displayPassword: false,
    capitalize: false,

    displayKeyboardSpecial:false,
    displayKeyboardLetters:false,
    displayKeyboardExtends:false,
    displayKeyboard:true,
    enabledCommitPassowrd:false
  }

  $scope.initialize = function() {
    $scope.updateDate();
    $scope.updateDay();
    $scope.model.displayCodeContainer = false;
    $scope.model.displayInfoContainer = true;
    $scope.model.enabledCommit = false;
    $scope.model.code = '';
    $scope.model.password = '';
    $scope.model.displayInputCode = false;
    $scope.model.displayPassword = false;
    $scope.initializeKeyboard();

  }

  $scope.initializeKeyboard = function() {
    $scope.model.displayKeyboardExtends = false;
    $scope.model.displayKeyboard = true;
    $scope.model.capitalize = false;

    $scope.model.displayKeyboardSpecial = false;
    $scope.model.displayKeyboardLetters = false;
    $scope.model.enabledCommitPassowrd = false;
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
    $scope.model.hours = hs + ":" + min;
    $scope.model.seconds = sec;
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


  $scope.enterCode = function() {
    $scope.model.displayInputCode = false;
    $scope.model.displayPassword = true;

    $scope.model.displayKeyboardExtends = true;
    $scope.model.displayKeyboard = false;
    $scope.model.capitalize = false;

    $scope.model.displayKeyboardSpecial = false;
    $scope.model.displayKeyboardLetters = true;
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
   * ------------------ PASSWORD ------------------------------
   * ----------------------------------------------------------
   */

   $scope.$watch('model.password', function(newValue, oldValue) {
     if ($scope.model.password == null || $scope.model.password.trim() == '') {
       $scope.model.enabledCommitPassowrd = false;
     } else {
       $scope.model.enabledCommitPassowrd = true;
     }
   });

   $scope.enterChar = function(char, capitalize) {
     if ($scope.model.password == null) {
       $scope.model.password = '';
     }
     $scope.model.password += (capitalize) ? char.toUpperCase() : char;
   }

   $scope.deleteChar = function() {
     $scope.model.password = ($scope.model.password == null || $scope.model.password.trim() == '') ? '' : $scope.model.password.substring(0, $scope.model.password.length-1);
   }

   $scope.isEnabledCommitPassowrd = function() {
     return $scope.model.enabledCommitPassowrd;
   }

   $scope.cancelPassword = function() {
     $scope.initialize();
   }

   $scope.enterPassword = function() {
    Firmware.sendCode($scope.model.code,$scope.model.password,
      function(response) {

      },
      function(error) {
        Notifications.message(error);
      }
    );
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

  $scope.displayKeyboard = function() {
    return $scope.model.displayKeyboard;
  }

  $scope.displayKeyboardExtends = function() {
    return $scope.model.displayKeyboardExtends;
  }

  $scope.displayKeyboardSpecial = function() {
    return $scope.model.displayKeyboardSpecial;
  }

  $scope.displayKeyboardLetters = function() {
    return $scope.model.displayKeyboardLetters;
  }

  $scope.changeKeyboardLetters = function() {
    $scope.model.displayKeyboardSpecial = false;
    $scope.model.displayKeyboardLetters = true;
  }

  $scope.changeKeyboardSpecial = function() {
    $scope.model.displayKeyboardLetters = false;
    $scope.model.displayKeyboardSpecial = true;
  }

  $timeout(function() {
    $scope.initialize();
  },0);


  /* ----------------------------------------------------------
   * ----------------------- EVENTOS --------------------------
   * ----------------------------------------------------------
   */

   $scope.$on('HomeEvent', function(event, data) {
     $scope.initialize();
   });

/*
   $scope.$on('identifiedEvent', function(event, data) {
     // si es admin le muestro la pantalla de enrollado
     if (data == 'admin') {
       $location.path("/enroll");
     } else {
       // sino es un log
       console.log('log');
     }
   });*/

}]);
