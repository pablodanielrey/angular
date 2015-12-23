

// Please note that $modalInstance represents a modal window (instance) dependency.
// It is not the same as the $modal service.
app.controller('ModalAlertCtrl', ["$scope", "$modalInstance", "newAlert", function ($scope, $modalInstance, newAlert) {
 
  $scope.title = newAlert.title;
  $scope.message = newAlert.message;
  $scope.type = newAlert.type; //alert (Default) , confirm

  $scope.ok = function () {
    $modalInstance.close($scope.newAlert); 
  }; 

  $scope.cancel = function () {
    $modalInstance.dismiss($scope.newAlert); 
  };

}]);