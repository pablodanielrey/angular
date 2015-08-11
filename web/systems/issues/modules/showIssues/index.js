


app.controller('ShowRequestsCtrl', ["$scope", "$timeout", "$window", "Module", "Notifications", "Issue", function ($scope, $timeout, $window, Module, Notifications, Issue) {
 
 
  $scope.requests = [];
    

  /******************
   * INICIALIZACION *
   ******************/
  $timeout(function() {
    Module.authorize('ADMIN-ASSISTANCE,USER-ASSISTANCE',
      function(response){
        if (response !== 'granted') {
          Notifications.message("Acceso no autorizado");
          $window.location.href = "/#/logout";
        }
        $scope.global.sessionUserId = Module.getSessionUserId();
      },
      function(error){
        Notifications.message(error);
        $window.location.href = "/#/logout";
      }
    );
  }, 0);
  
}]);
