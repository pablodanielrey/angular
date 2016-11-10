  angular
  .module('mainApp')
  .controller('GridDesignationCtrl', GridDesignationCtrl);

GridDesignationCtrl.inject = ['$scope', 'Designation']
  
function GridDesignationCtrl($scope, Designation) {


  //***** inicializar grilla *****
  $scope.searchDesignations = function(){

    $scope.designations = []; //datos de la grilla

    Designation.findBySearch($scope.search).then(
      function(response){ $scope.designations = response; },
      function(error) { deferred.reject(error); }
    );
	};
	
	
    

  
}




