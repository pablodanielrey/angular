
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
      when('/adminAccount', { 
        templateUrl: 'templates/adminAccount.html', 
		controller: 'AdminAccountController'
      }). 
      otherwise({ 
        redirectTo: '/listCreateAccount' 
      }); 
  }]);
