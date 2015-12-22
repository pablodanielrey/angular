angular
  .module('mainApp')
  .controller('IndexLoginCtrl',IndexLoginCtrl);

IndexLoginCtrl.$inject = ['$rootScope','$scope','$timeout','$location','Notifications'];

function IndexLoginCtrl($rootScope, $scope, $timeout, $location, Notifications) {

    var vm = this;

    $scope.model = {
    }

    $rootScope.$on("$wamp.open", function (event, session) {
      $scope.$broadcast('wampOpenEvent',event);
    });

    $rootScope.$on("$wamp.close", function (event, session) {
      $scope.$broadcast('wampCloseEvent',event);
    });

    $scope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });

};
