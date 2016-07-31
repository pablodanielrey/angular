angular
  .module('login')
  .controller('IndexLoginCtrl',IndexLoginCtrl)
  .run(function($wampPublic) {
    console.log('abriendo conexion');
    $wampPublic.open();
  });

IndexLoginCtrl.$inject = ['$rootScope','$scope'];

function IndexLoginCtrl($rootScope, $scope, $wampPublic) {

    $rootScope.loaded = false;
    $scope.loaded = false;

    /*
      no es disparado ya que no existe ningun ng-view en la vista.
    $scope.$on('$viewContentLoaded', function(event) {
      console.log('conectandose al wamp realm public');
      $wampPublic.open();
    });
    */

};
