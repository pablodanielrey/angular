
var app = angular.module('mainApp');


app.controller('ChangePasswordCtrl', function($rootScope, $scope, $routeParams, Messages, Utils, Session, Credentials) {

  $scope.user = {};
  $scope.cp = {};

  $scope.clear = function() {
    $scope.user.username = '';
    $scope.user.newPassword = '';
    $scope.user.newPasswordRepeat = '';
  }

  $scope.changePassword = function() {

    if (($scope.cp.hash != undefined) && ($scope.cp.hash != null)) {
      Credentials.changePasswordWithHash($scope.user,$scope.cp.hash,
        function(ok) {
          $rootScope.$broadcast('ShowMessageEvent','Clave cambiada exitósamente');
        },
        function(error) {
          $rootScope.$broadcast('ShowMessageEvent',['Ocurrió un error cambiando su clave','Por favor reintente la operación']);
        });
    } else {
      Credentials.changePassword($scope.user,
        function(ok) {
          $rootScope.$broadcast('ShowMessageEvent','Clave cambiada exitósamente');
        },
        function(error) {
          $rootScope.$broadcast('ShowMessageEvent',['Ocurrió un error cambiando su clave','Por favor reintente la operación']);
        });
    }

  }

  $scope.$on('UserSelectedEvent', function(e,id) {
    Users.findUser(id,
    function(user) {

    },
    function(error) {

    })
  })

  $scope.clear();

  // obtengo los datos de la sesion o del hash
  if ($routeParams['hash'] != undefined) {

    $scope.user.username = $routeParams['username'];
    $scope.cp.hash = $routeParams['hash'];

  } else {

    var s = Session.getCurrentSession();
    $scope.user.username = s.login.username;
    $scope.cp.hash = null;

  }

});
