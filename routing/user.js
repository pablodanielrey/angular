
app.config(['$routeProvider', 
  function($routeProvider) { 
    $routeProvider. 
      when('/login', { 
        templateUrl: 'templates/login.html', 
        controller: 'LoginController'
      }). 
      when('/createAccount', { 
        templateUrl: 'templates/createAccount.html', 
		controller: 'CreateAccountController'
      }). 
      otherwise({ 
        redirectTo: '/createAccount' 
      }); 
  }]);
