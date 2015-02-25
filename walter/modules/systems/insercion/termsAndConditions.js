var app = angular.module('mainApp');


app.controller('LaboralInsertionTermsAndConditionsCtrl',function($scope) {

  $scope.accepted = false;

  $scope.termsAndConditionsAccepted = function() {
    return $scope.accepted;
  }

  $scope.accept = function() {
    $scope.accepted = true;
  }

});
