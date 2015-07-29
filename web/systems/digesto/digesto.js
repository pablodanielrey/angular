angular
    .module('mainApp')
    .controller('DigestoCtrl',DigestoCtrl)

DigestoCtrl.$inject = ['$rootScope','$scope','$location','$timeout','$wamp'];

function DigestoCtrl($rootScope,$scope,$location,$timeout,$wamp) {

  $scope.$on('$viewContentLoaded', function(event) {
    $wamp.open();
  });


}
