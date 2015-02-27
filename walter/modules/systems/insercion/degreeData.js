var app = angular.module('mainApp');


app.controller('DegreeLaboralInsertionCtrl', function($scope, $timeout, LaboralInsertion) {

  $scope.$on('UpdateUserDataEvent',function(event,data) {
    $scope.loadData();
  });



  /*
    para implementar el chequeo que quiere lucas de las ofertas.
  */
  $scope.onCoursesChange = function(degree) {
    if (degree.courses > 29) {
      $scope.showDegree = degree;
    } else {
      $scope.showDegree = null;
      degree.offerYoungProfessionals = false;
    }
  }

  $scope.showOffer = function(degree) {
    if ($scope.showDegree == degree) {
      return true;
    }
    return false;
  }





  $scope.addDegree = function() {
    var degree = {
      id: null,
      user_id: $scope.model.selectedUser,
      name: '',
      curses: '0',
      average1: '0',
      average2: '0'
    }
    $scope.model.degrees.push(degree);
  }

  $scope.deleteDegree = function($index) {
		$scope.model.degrees.splice($index, 1);
		if ($scope.model.degrees.length == 0) {
      $scope.addDegree()
    }
	}

  $scope.loadData = function() {

    LaboralInsertion.findDegreeData($scope.model.selectedUser,
      function(data) {
        if ((data != undefined) && (data != null) && (data.length > 0)) {
          $scope.model.degrees = data;
        }
        if ($scope.model.degrees.length == 0) {
          $scope.addDegree()
        }
      },
      function(err) {
        alert(err);
      });

  }

  $timeout(function() {
    $scope.loadData();
  });


});
