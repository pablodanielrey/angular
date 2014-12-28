
var app = angular.module('mainApp');


app.controller('CreateAccountRequestCtrl', function($scope, Messages, Utils, Session) {

  $scope.request = {
          name:'',
          lastname:'',
          dni:'',
          email:'',
          reason:''
  };

  $scope.ids = [];

  $scope.createRequest = function() {

    var msg = {
        id: Utils.getId(),
        action: 'createAccountRequest',
        session: Session.getSessionId(),
        request: $scope.request
    };

    Messages.send(msg, function(response) {
      alert('groso');
    });

    clearRequest();
  };

  clearRequest = function() {
    $scope.request.name = '';
    $scope.request.lastname = '';
    $scope.request.dni = '';
    $scope.request.email = '';
    $scope.request.reason = '';
  }

});
