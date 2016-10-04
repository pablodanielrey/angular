angular
    .module('mainApp')
    .controller('IndexController',IndexController)

IndexController.$inject = ['$rootScope','$scope','$location','$timeout','$wamp'];

function IndexController($rootScope,$scope,$location,$timeout,$wamp) {

  $scope.$on('$viewContentLoaded', function(event) {
    $wamp.open();
  });


}
