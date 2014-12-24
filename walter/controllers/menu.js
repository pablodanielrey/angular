
var app = angular.module('mainApp');

app.controller('MenuCtrl', function($rootScope, $scope, Session) {


  $scope.applyVisibility = function() {
    var sid = Session.getSessionId();
    if ((sid == undefined) || (sid == '') || (sid == false)) {
      $scope.menuDisplay = 'none';
    } else {
      $scope.menuDisplay = 'inline';
    }
  }


  $rootScope.$on('loginOk', function(event,data) {
    $scope.applyVisibility();
  });

  $rootScope.$on('logoutOk', function(event,data) {
    $scope.applyVisibility();
  });


  $scope.applyVisibility();

});
