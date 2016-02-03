angular
  .module('mainApp')
  .controller('SearchCtrl', SearchCtrl);

SearchCtrl.$inject = ['$rootScope','$scope','$location', '$window', 'Notifications','LaboralInsertion', 'Login', 'Utils'];

function SearchCtrl($rootScope, $scope, $location, $window, Notifications, LaboralInsertion, Login, Utils) {

  $scope.model = {
    inscriptions = [];
  };

  $scope.initialize = function() {
    LaboralInsertion.findAllInscriptions().then(function(ins) {
      $scope.model.inscriptions = ins;
      console.log($scope.inscriptions);
    }, function(err) {
      console.log(err);
    });
  }

  $rootScope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

}
