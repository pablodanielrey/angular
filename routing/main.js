
app.config(['$routeProvider', 
  function($routeProvider) { 
    $routeProvider. 
      when('/login', { 
        templateUrl: 'templates/login.html', 
        controller: 'LoginController' 
      }). 
      when('/showOrders', { 
        templateUrl: 'templates/show-orders.html', 
        controller: 'ShowOrdersController' 
      }). 
      otherwise({ 
        redirectTo: '/addOrder' 
      }); 
  }]);

