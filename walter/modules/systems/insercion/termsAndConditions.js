var app = angular.module('mainApp');


app.controller('LaboralInsertionTermsAndConditionsCtrl',["$scope", "$location", "Session", "LaboralInsertion", function($scope, $location, Session, LaboralInsertion) {



  	/**
	 * procesar verificacion de terminos y condiciones
	 */
	$scope.accept = function(){

		var session = Session.getCurrentSession();
		if((session == null) || (session.selectedUser == null)){
			$location.path('/main');
		}


		LaboralInsertion.acceptTermsAndConditions(session.selectedUser,
      function(ok) {
        $location.path('/editInsertion');
      },
      function(error) {
        $location.path('/main');
      });
	}



}]);
