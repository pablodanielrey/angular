
app.config(['$routeProvider', function($routeProvider) { 
	$routeProvider. 
		when('/login', { 
			templateUrl: 'templates/login.html', 
			controller: 'LoginController'
		}). 
		when('/home', { 
			templateUrl: 'templates/home.html',
			controller: 'HomeController'
		}). 
		when('/logout', { 
			templateUrl: 'templates/logout.html',
			controller: 'LogoutController'
		}). 
		when('/start', { 
			templateUrl: 'templates/start.html',
		}). 
		when('/createAccount', { 
			templateUrl: 'templates/createAccount.html', 
			controller: 'CreateAccountController'
		}). 
		when('/adminUser', { 
			templateUrl: 'templates/adminUser.html', 
			//controller: 'CreateAccountController'
		}).
		otherwise({ 
			redirectTo: '/home' 
		}); 
		
}]);
