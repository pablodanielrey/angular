

var app = angular.module('digestoApp',[]);

app.controller('MenuCtrl', function($scope) {

  $scope.mv = false;

  $scope.menuVisible = function() {
    return $scope.mv;
  };

  $scope.toogleMenu = function() {
    $scope.mv = !$scope.mv;
  };

});

app.controller('DigestoCtrl',function($scope) {


});
