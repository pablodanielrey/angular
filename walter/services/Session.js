var app = angular.module('mainApp');

app.factory('Session', ["$rootScope", "$cookies", "$location", function($rootScope, $cookies, $location) {

	var factory = {};

	factory.create = function(session){
		$cookies.fceSession = session;
	}

	factory.destroy = function(){
		$cookies.fceSession = "";
	};

	factory.getSessionId = function(){
		return $cookies.fceSession;
	}

	return factory;
}]);
