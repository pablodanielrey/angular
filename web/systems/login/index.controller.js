angular
  .module('mainApp')
  .controller('IndexLoginCtrl',IndexLoginCtrl);

IndexLoginCtrl.$inject = ['$rootScope','$scope'];

function IndexLoginCtrl($rootScope, $scope) {

    $rootScope.loaded = false;
    $scope.loaded = false;

    $rootScope.$on("$wamp.open", function (event, session) {
      $scope.$broadcast('wampOpenEvent', event);
    });

    $rootScope.$on("$wamp.close", function (event, session) {
      $scope.$broadcast('wampCloseEvent',event);
    });

    $scope.$on('$viewContentLoaded', function(event) {
      // nada
    });

};
