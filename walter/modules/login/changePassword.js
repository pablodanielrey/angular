
var app = angular.module('mainApp');


app.controller('ChangePasswordCtrl', function($scope, $routeParams, Messages, Utils, Session) {

  $scope.user = {};
  $scope.cp = {};

  $scope.clear = function() {
    $scope.user.username = '';
    $scope.user.newPassword = '';
    $scope.user.newPasswordRepeat = '';
  }

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


  $scope.changePassword = function() {
    var msg = {
      id: Utils.getId(),
      action: 'changePassword',
      username: $scope.user.username,
      password: $scope.user.newPassword
    };

    if (($scope.cp.hash != undefined) && ($scope.cp.hash != null)) {
      msg.hash = $scope.cp.hash;
    }

    var sid = Session.getSessionId();
    if (sid != null) {
      msg.session = sid;
    }

    Messages.send(msg,
      function(ok){
        alert(ok);
      },
      function(error) {
        alert(error);
      });
  }


});
