
app.config(['$routeProvider', 
  function($routeProvider) { 
    $routeProvider. 
      when('/login', { 
        templateUrl: 'templates/login.html', 
        controller: 'LoginController'
      }). 
      when('/listCreateAccount', { 
        templateUrl: 'templates/listCreateAccount.html', 
		controller: 'ListCreateAccountController'
      }). 
      when('/adminUser', { 
        templateUrl: 'templates/adminUser.html', 
		//controller: 'AdminUser'
      }). 
      otherwise({ 
        redirectTo: '/listCreateAccount' 
      }); 
  }]);
