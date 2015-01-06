
var app = angular.module('mainApp');


app.controller('ChangePasswordCtrl', function($scope, $routeParams, Messages, Utils, Session, Credentials) {

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
          alert(ok);
        },
        function(error) {
          alert(error);
        });
    } else {
      Credentials.changePassword($scope.user,
        function(ok) {
          alert(ok);
        },
        function(error) {
          alert(error);
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
