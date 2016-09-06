(function() {
  'use strict';

  angular
    .module('login')
    .controller('LoginCtrl', LoginCtrl)
    .directive('mooFocusExpression', function($timeout) {
      return {
          link: function(scope, element, attrs) {
            scope.$watch(attrs.mooFocusExpression, function (value) {

                if (attrs.mooFocusExpression) {
                    if (scope.$eval(attrs.mooFocusExpression)) {
                        $timeout(function () {
                            element[0].focus();
                        }, 100); //need some delay to work with ng-disabled
                    }
                }
            });
          }
      };
    });


  LoginCtrl.$inject = ['$scope','$window', '$interval', '$location', 'Login', 'Files'];

  function LoginCtrl($scope, $window, $interval, $location, Login, Files) {

    /* ---------------------------------------------------
     * --------------------- VARIABLES -------------------
     * ---------------------------------------------------
     */
      var vm = this;

      $scope.model = {
  			username: '',
  			password: '',
        openConnection: false,
  	    user:null
      }

      const classNameViewUser = 'screenUser';
      const classNameViewPassword = 'screenPassword';
      const classNameDisconnected = 'verServerDesconectado';
      const classNameConnected = 'verServerConectado';
      const classNameNoError = 'ocultarError';
      const classNameError = ''

      $scope.view = {
        focus: 'inputUser',
        classConnection: classNameConnected, // classNameDisconnected classNameConnected
        classScreen: classNameViewUser, // classNameViewUser classNameViewPassword
        classError: classNameNoError
      }

      /* ---------------------------------------------------
       * ---------------- INICIALIZACION -------------------
       * ---------------------------------------------------
       */

      $scope.initialize = initialize;

      function initialize() {
        $scope.view.classConnection = classNameConnected;
        $scope.viewUser();
        $scope.view.focus = 'inputUser';
      }


      /* ---------------------------------------------------
       * ----------------------- EVENTOS -------------------
       * ---------------------------------------------------
       */

      $scope.$on('$viewContentLoaded', function(event) {
        $scope.initialize();
      });

      $scope.$on('wamp.open', function(event) {
        $scope.connectServer();
      });

      $scope.$on('wamp.close', function(event) {
        $scope.disconnectServer();
      });


      /* ---------------------------------------------------
       * ---------------------- ACCIONES -------------------
       * ---------------------------------------------------
       */
       $scope.connectServer = connectServer;
       $scope.disconnectServer = disconnectServer;
       $scope.sendUsername = sendUsername;
       $scope.sendPassword = sendPassword;
       $scope.clearUserNameField = clearUserNameField;
       $scope.clearPasswordField = clearPasswordField;

       function connectServer() {
         $scope.model.openConnection = true;
         $scope.changeClassConnection(classNameConnected);
       }

       function disconnectServer() {
         $scope.model.openConnection = false;
         $scope.changeClassConnection(classNameDisconnected);
       }

       function clearUserNameField() {
         $scope.model.username = '';
         $scope.view.classError = classNameNoError;
       }

       function clearPasswordField() {
         $scope.model.password = '';
         $scope.view.classError = classNameNoError;
       }

       function sendUsername() {
         Login.getPublicData($scope.model.username).then(
           function(publicData) {
             $scope.model.user = publicData;
             $scope.view.focus = 'inputPassword';
             $scope.viewPassword();
           },
           function(err) {
             $scope.viewUserError();
           });
       }

       $scope.getUserPhoto = function() {
         if ($scope.model.user == null || $scope.model.user.photo == null || $scope.model.user.photo == '') {
           return "modules/img/imgUser.jpg";
         } else {
           return Files.toDataUri($scope.model.user.photo);
         }
       }

       function sendPassword() {
         Login.login($scope.model.username, $scope.model.password).then(
           function(systems) {
             console.log(systems);
             for (var i = 0; i < systems['registered'].length; i++) {
                 if ($location.host() == systems['registered'][i].domain) {
                   $window.location.href = systems['registered'][i].relative;
                   return;
                 }
             }
             // si no lo encuentra usa la ultima (deberia ser la de sistema en mantenimiento o algo parecido)
             $window.location.href = systems['default'];
           },
           function(err) {
              $scope.viewPasswordError();
           });
       }

       /*
       $scope.processLogin = function() {
         Login.getRegisteredSystems().then(
           function(systems) {
             console.log(systems);
             for (var i = 0; i < systems['registered'].length; i++) {
                 if ($location.host() == systems['registered'][i].domain) {
                   $window.location.href = systems['registered'][i].relative;
                   return;
                 }
             }
             // si no lo encuentra usa la ultima (deberia ser la de sistema en mantenimiento o algo parecido)
             $window.location.href = systems['default'];
           },
           function(err) {
             console.log(err);
             alert('error de sistema');
           });
       }
       */

       /* ---------------------------------------------------
        * ----------------- MANEJO VISUAL -------------------
        * ---------------------------------------------------
        */

        $scope.changeClassConnection = changeClassConnection;

        $scope.viewUser = viewUser;
        $scope.viewUserError = viewUserError;
        $scope.viewPassword = viewPassword;
        $scope.viewPasswordError = viewPasswordError;

        function changeClassConnection(className) {
          $scope.view.classConnection = className;
        }

        function viewPassword() {
          $scope.view.classScreen = classNameViewPassword;
          $scope.view.classError = classNameNoError;
        }

        function viewPasswordError() {
          $scope.view.classScreen = classNameViewPassword;
          $scope.view.classError = classNameError;
          $scope.interval = $interval(function() {
              $scope.clearPasswordField();
          }, 5000, [1]);
        }

        function viewUserError() {
          $scope.view.classScreen = classNameViewUser;
          $scope.view.classError = classNameError;
          $scope.interval = $interval(function() {
              $scope.clearUserNameField();
          }, 5000, [1]);
        }

        function viewUser() {
          $scope.view.classScreen = classNameViewUser;
          $scope.view.classError = classNameNoError;
        }

  };

})();
