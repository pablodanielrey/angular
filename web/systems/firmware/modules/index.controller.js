angular
    .module('mainApp')
    .controller('MainFirmwareController',MainFirmwareController);

MainFirmwareController.$inject = ['$rootScope','$scope','$timeout','$location','Notifications', 'Firmware'];

function MainFirmwareController($rootScope,$scope, $timeout, $location, Notifications, Firmware) {

  var vm = this;


  vm.view = {
    inputCode : false,
    codeContainer: false,
    inputPassword: false,
    infoContainer: true,
    keyboard: {},
    date: {
      day:'',
      hours:'',
      seconds:''
    }
  }

  vm.model = {
    code: '',
    password: '',
    enabledCommit: false,
    enabledCommitPassowrd:false,
    date:new Date(),
    adminMode:false
  }


  vm.isDisplayInfoContainer = isDisplayInfoContainer;
  vm.isEnabledCommit = isEnabledCommit;
  vm.initialize = initialize;

  function initialize() {
    vm.updateDate();
    vm.updateDay();
    vm.view.codeContainer = false;
    vm.view.infoContainer = true;
    vm.model.enabledCommit = false;
    vm.model.code = '';
    vm.model.password = '';
    vm.view.inputCode = false;
    vm.view.inputPassword = false;

    vm.initializeKeyboard();

    vm.model.adminMode = false;

  }


  function isDisplayInfoContainer() {
    return vm.view.infoContainer;
  }

  function isEnabledCommit() {
    return vm.model.enabledCommit;
  }



  // //////////////////////////////////////////////////////
  // //////////////////// KEYBOARD ////////////////////////
  // //////////////////////////////////////////////////////

  vm.view.keyboard = {
    special:false,
    letters:false,
    extends:false,
    display:true,
    capitalize: false
  }

  vm.initializeKeyboard = initializeKeyboard;
  vm.displayKeyboard = displayKeyboard;
  vm.displayKeyboardExtends = displayKeyboardExtends;
  vm.displayKeyboardSpecial = displayKeyboardSpecial;
  vm.displayKeyboardLetters = displayKeyboardLetters;
  vm.changeKeyboardLetters = changeKeyboardLetters;
  vm.changeKeyboardSpecial = changeKeyboardSpecial;

  function changeKeyboardLetters() {
    vm.view.keyboard.special = false;
    vm.view.keyboard.letters = true;
  }

  function changeKeyboardSpecial() {
    vm.view.keyboard.letters = false;
    vm.view.keyboard.special = true;
  }

  // --------- inicializacion de los teclados -----------

  function initializeKeyboard() {
    vm.view.keyboard.extends = false;
    vm.view.keyboard.display = true;
    vm.view.keyboard.capitalize = false;

    vm.view.keyboard.special = false;
    vm.view.keyboard.letters = false;
    vm.view.enabledCommitPassowrd = false;
  }


  // -------------- getters ---------------------

  function displayKeyboard() {
    return vm.view.keyboard.display;
  }

  function displayKeyboardExtends() {
    return vm.view.keyboard.extends;
  }

  function displayKeyboardSpecial() {
    return vm.view.keyboard.special;
  }

  function displayKeyboardLetters() {
    return vm.view.keyboard.letters;
  }


  // //////////////////////////////////////////////////////
  // ////////////////// INPUT CODE ////////////////////////
  // //////////////////////////////////////////////////////


  vm.addNumber = addNumber;
  vm.enterCode = enterCode;
  vm.cancel = cancel;
  vm.deleteNumber = deleteNumber;
  vm.isDisplayCodeContainer = isDisplayCodeContainer;
  vm.isDisplayInputCode = isDisplayInputCode;


  function isDisplayCodeContainer() {
    return vm.view.codeContainer;
  }

  function isDisplayInputCode() {
    return vm.view.inputCode;
  }


  function enterCode() {
    vm.view.inputCode = false;
    vm.view.inputPassword = true;

    vm.view.keyboard.extends = true;
    vm.view.keyboard.display = false;
    vm.view.keyboard.capitalize = false;

    vm.view.keyboard.special = false;
    vm.view.keyboard.letters = true;
  }

  $scope.$watch('vm.model.code', function(newValue, oldValue) {

    var isZero = newValue == '0' && (oldValue == null || oldValue.trim() == '');
    var isNotNumber = isNaN(newValue);
    if (isZero || isNotNumber || newValue.indexOf('.') > -1) {
      vm.model.code = oldValue;
    }

    if (vm.model.code == null || vm.model.code.trim() == '') {
      vm.model.enabledCommit = false;
    } else {
      vm.model.enabledCommit = true;
    }
   });


  function addNumber(number) {
    if (vm.view.infoContainer) {
      vm.view.infoContainer = false;
      vm.view.codeContainer = true;
      vm.view.inputCode = true;
      vm.view.inputPassword = false;
      vm.model.enabledCommit = true;
    }

    if (vm.model.code == null) {
        vm.model.code = '';
    }

    vm.model.code += number;
  }

  function cancel() {
    vm.model.code = '';
    vm.view.codeContainer = false;
    vm.view.infoContainer = true;
    vm.model.enabledCommit = false;
    vm.view.inputCode = false;
    vm.view.inputPassword = false;
  }

  function deleteNumber() {
    vm.model.code = (vm.model.code == null || vm.model.code.trim() == '') ? null : vm.model.code.substring(0, vm.model.code.length-1);
  }


  // //////////////////////////////////////////////////////
  // //////////////////// PASSWORD ////////////////////////
  // //////////////////////////////////////////////////////


   vm.enterChar = enterChar;
   vm.deleteChar = deleteChar;
   vm.isEnabledCommitPassowrd = isEnabledCommitPassowrd;
   vm.cancelPassword = cancelPassword;
   vm.enterPassword = enterPassword;
   vm.isDisplayInputPassword = isDisplayInputPassword;

   function isDisplayInputPassword() {
     return vm.view.inputPassword;
   }

   $scope.$watch('vm.model.password', function(newValue, oldValue) {
     if (vm.model.password == null || vm.model.password.trim() == '') {
       vm.model.enabledCommitPassowrd = false;
     } else {
       vm.model.enabledCommitPassowrd = true;
     }
   });

   function enterChar(char, capitalize) {
     if (vm.model.password == null) {
       vm.model.password = '';
     }
     vm.model.password += (capitalize) ? char.toUpperCase() : char;
   }

   function deleteChar() {
     vm.model.password = (vm.model.password == null || vm.model.password.trim() == '') ? '' : vm.model.password.substring(0, vm.model.password.length-1);
   }

   function isEnabledCommitPassowrd() {
     return vm.model.enabledCommitPassowrd;
   }

   function cancelPassword() {
     vm.initialize();
   }

   function enterPassword() {
    Firmware.identify(vm.model.code,vm.model.password,
      function(response) {

      },
      function(error) {
        Notifications.message(error);
      }
    );
   }


   // //////////////////////////////////////////////////////
   // ////////////////////// RELOJ /////////////////////////
   // //////////////////////////////////////////////////////

   vm.updateDay = updateDay;
   vm.setHours = setHours;
   vm.updateDate = updateDate;

   function updateDay() {
     var options = {
         weekday: "long",
         year: "numeric",
         month: "2-digit",
         day: "numeric"
     };

     vm.view.date.day = vm.model.date.toLocaleDateString('es',options);
   }

   function setHours() {
     var hs = ('0' + vm.model.date.getHours()).slice(-2);
     var min = ('0' + vm.model.date.getMinutes()).slice(-2);
     var sec = ('0' + vm.model.date.getSeconds()).slice(-2);
     vm.view.date.hours = hs + ":" + min;
     vm.view.date.seconds = sec;
   }

   function updateDate() {
     var day = vm.model.date.getDay();

     vm.model.date = new Date();
     vm.setHours();

     if (day != vm.model.date.getDay()) {
         vm.updateDay();
     }


     $timeout(function() {
       vm.updateDate();
     }, 1000);
   }



  // //////////////////////////////////////////////////////
  // //////////////////// EVENTOS /////////////////////////
  // //////////////////////////////////////////////////////

   $scope.$on('HomeEvent', function(event, data) {
     vm.initialize();
   });


   $scope.$on('IdentifiedEvent', function(event, data) {

     console.log(data);

     if (vm.model.adminMode) {
       if (data.profile == 'admin') {
         $location.path("/enroll");
       } else {
         Notifications.message('Error, usted no tiene permisos de administrador');
         vm.initialize();
       }
     } else {
       $scope.$parent.logData = {
          date:data.log.log,
          user:data.user
       }

       $location.path('/log');
     }
   });

   $scope.$on('$viewContentLoaded', function(event) {
     vm.initialize();
   });

};
