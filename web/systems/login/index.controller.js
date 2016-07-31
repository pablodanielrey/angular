angular
  .module('mainApp')
  .controller('IndexLoginCtrl',IndexLoginCtrl);

IndexLoginCtrl.$inject = ['$rootScope','$scope','$wampPublic'];

function IndexLoginCtrl($rootScope, $scope) {

    $rootScope.loaded = false;
    $scope.loaded = false;

    $scope.$on('$viewContentLoaded', function(event) {
      conosle.log('conectandose al wamp realm public');
      $wampPublic.open();
    });

};
