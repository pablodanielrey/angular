
angular
  .module('mainApp')
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


LoginCtrl.$inject = ['$scope','$window','Notifications','Login','Users'];

function LoginCtrl($scope, $window, Notifications, Login, Users) {

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
    const classNoError = 'ocultarError';
    const classError = ''

    $scope.view = {
      focus: 'inputUser',
      classConnection: classNameConnected, // classNameDisconnected classNameConnected
      classScreen: classNameViewUser, // classNameViewUser classNameViewPassword
      classError: classNoError
    }


    /* ---------------------------------------------------
     * ---------------- INICIALIZACION -------------------
     * ---------------------------------------------------
     */

    $scope.initialize = initialize;

    function initialize() {
      $scope.view.classConnection = classNameConnected;
      $scope.view.classScreen = classNameViewUser;
      $scope.view.classError = classNoError;
      $scope.view.focus = 'inputUser';
    }


    /* ---------------------------------------------------
     * ----------------------- EVENTOS -------------------
     * ---------------------------------------------------
     */

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });

    $scope.$on('wampOpenEvent', function(event) {
      $scope.connectServer();
    });

    $scope.$on('wampCloseEvent', function(event) {
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

     function connectServer() {
       $scope.model.openConnection = true;
       $scope.changeClassConnection(classNameConnected);
     }

     function disconnectServer() {
       $scope.model.openConnection = false;
       $scope.changeClassConnection(classNameDisconnected);
     }

     function sendUsername() {
       Users.findByDni($scope.model.username,
         function(user) {
           console.log(user);
           $scope.model.user = user;
           $scope.viewPassword();
           $scope.view.focus = 'inputPassword';
         },
         function(error) {
           $scope.viewUserError();
         }
       );

     }

     function sendPassword() {
       Login.login($scope.model.username,$scope.model.password,
         function(data) {
           $window.location.href = "/index.html";
         },
         function(error) {
           $scope.viewPasswordError();
         }
       );
     }

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
      }

      function viewPasswordError() {
        $scope.view.classScreen = classNameViewPasswordError;
      }

      function viewUserError() {
        $scope.view.classScreen = classNameViewUserError;
      }

      function viewUser() {
        $scope.view.classScreen = classNameViewUser;
      }

     /* ---------------------------------------------------
      * ------------------ CODIGO VIEJO -------------------
      * ---------------------------------------------------
      */

    /*
		$scope.login = function() {

				// bug de angular.
				// http://stackoverflow.com/questions/14965968/angularjs-browser-autofill-workaround-by-using-a-directive

			$scope.$broadcast("autofill:update");

      Login.login($scope.model.username, $scope.model.password,
        function(sid) {
            // usuario logueado correctamente
            $window.location.href = "/index.html";

        }, function(err) {
            Notifications.message(err);
        });

		};*/

};
