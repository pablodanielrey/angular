
app.config(['$routeProvider', function($routeProvider) { 
	$routeProvider. 
		when('/login', { 
			templateUrl: 'templates/login.html', 
			controller: 'LoginController'
		}). 
		when('/home', { 
			templateUrl: 'templates/menu/user.html',
			controller: 'HomeController'
		}). 
		when('/logout', { 
			templateUrl: 'templates/logout.html',
			controller: 'LogoutController'
		}). 
		when('/loading', { 
			templateUrl: 'templates/loading.html',
		}). 
		
		
		when('/createAccount', { 
			templateUrl: 'templates/createAccount.html', 
			controller: 'CreateAccountController'
		}). 
		when('/modifyUser', { 
			templateUrl: 'templates/modifyUser.html', 
			controller: 'ModifyUserController'
		}).
		otherwise({ 
			redirectTo: '/home' 
		}); 
		
}]);
