var app = angular.module('library');

app.controller('TestCtrl', ["$rootScope", '$scope', "$wamp", function ($rootScope, $scope, $wamp) {

  $scope.message = '';

  $scope.test = function() {
    if (!$wamp.connection.isOpen) {
      $scope.message = 'debe loguearse antes';
      return;
    }
    o = {
      prueba: '1',
      prueba2: '2'
    };
    $wamp.call('test_serializer', [o]).then(function(data) {
      console.log(data);
      $scope.message = data;
    });
  };

}]);
