var app = angular.module('mainApp');

app.controller('HeaderCtrl', function($rootScope, $scope, $location, Login, Session, Notifications) {

  $scope.goHome = function() {
    $location.path('/main');
    //$rootScope.$broadcast("MenuOptionSelectedEvent",'Home');
  }

  $scope.logout = function() {
    var sid = Session.getCurrentSession();
    Login.logout(sid,
      function() {
        $location.path('/main');
      }, function(err) {
        Notifications.message(err);
      }
    );
    //$rootScope.$broadcast("MenuOptionSelectedEvent",'Logout');
  }

});
