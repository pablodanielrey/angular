
app.config(['$routeProvider', function($routeProvider) { 
	$routeProvider. 
		when('/login', { 
			templateUrl: 'templates/login.html', 
			controller: 'LoginController'
		}). 
		when('/home', { 
			templateUrl: 'templates/menu/admin.html',
			controller: 'HomeController'
		}). 
		when('/logout', { 
			templateUrl: 'templates/logout.html',
			controller: 'LogoutController'
		}). 
		when('/loading', { 
			templateUrl: 'templates/loading.html',
		}). 
		when('/listCreateAccount', { 
			templateUrl: 'templates/listCreateAccount.html', 
			controller: 'ListCreateAccountController',
		}). 
		otherwise({ 
			redirectTo: '/home' 
		}); 
		
}]);
