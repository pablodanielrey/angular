angular
  .module('mainApp')
  .service('Registration',Registration);

Registration.inject = ['$rootScope','$wamp','Session']


function Registration($rootScope,$wamp,Session) {

  $scope.status = {

  };


  $scope.initialize = function(){


  };

  $scope.submit = function(){
  };

  $scope.process = function(){
  };


  $scope.$on('$viewContentLoaded', function(event) {
		$scope.initialize();
	});



};
