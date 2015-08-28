app.controller('IndexCtrl',IndexCtrl);

IndexCtrl.$inject = ['$rootScope','$scope','$wamp','$window', '$timeout', 'Notifications', 'Login', 'Assistance'];

function IndexCtrl($rootScope, $scope, $wamp, $window, $timeout, Notifications, Login, Assistance) {

  $scope.getUsers = function(){
    Assistance.getUserOfficeRoles(
      function(data){
        console.log(data);
      },
      function(error){
        console.log(error);
      }
    );
  };


  $timeout(function() {
    $scope.getUsers();
  },0);


};
