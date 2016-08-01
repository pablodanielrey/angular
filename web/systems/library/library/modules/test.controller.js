var app = angular.module('library');

app.controller('TestCtrl', ["$rootScope", '$scope', "$location", "$wamp", function ($rootScope, $scope, $location, $wamp) {

  $scope.message = '';

  $scope.test = function() {
    if (!$wamp.connection.isOpen) {
      $scope.message = 'debe loguearse antes';
      $location.path('/');
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
