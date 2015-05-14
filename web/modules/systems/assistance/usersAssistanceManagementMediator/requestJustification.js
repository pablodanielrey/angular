var app = angular.module('mainApp');

app.controller('UsersAssistanceManagementMediatorRequestJustificationCtrl', ["$scope", "Assistance", "Notifications", "Utils", function($scope, Assistance, Notifications, Utils) {

  if(!$scope.model) Notifications.message("No esta definido el modelo");
  

  
  
  //***** METODOS DE SELECCION DE LA SECCION *****
  /**
   * Esta seleccionada la seccion correspondiente a la justificacion?
   * @returns {Boolean}
   */
  $scope.isSelectedJustification = function() {
    return ($scope.model.justificationSelectedId === $scope.justificationId);
  };


  /**
   * Modificar seleccion de opcion desplegable correspondiente a salidas eventuales
   * @returns {Boolean}
   */
	$scope.selectJustification = function() {
    if($scope.model.selectedUser === null){
      $scope.model.justificationSelectedId = null;
      Notifications.message("Debe seleccionar usuario");
      return;
    }
    if($scope.model.justificationSelectedId === $scope.justification.id){
      $scope.model.justificationSelectedId = null;
    } else {
      $scope.model.justificationSelectedId = $scope.justification.id;
    }
	};
  



  //***** INICIALIZACION *****
  $scope.init = function(justificationId){

    //***** inicializar datos de la justificacion *****
    $scope.justification = {
       id: justificationId,
       name: Utils.getJustificationName(justificationId),
       requestMode: Utils.getJustificationRequestMode(justificationId),
       stockMode: Utils.getJustificationStockMode(justificationId),
       mode:  Utils.getJustificationRequestMode(justificationId) + "," + Utils.getJustificationStockMode(justificationId),
    };
    
    $scope.justification.stock = null;
    if($scope.justification.stockMode === "year") $scope.justification.yearlyStock = null;
      
  };
   
   
  $scope.loadStockTotal = function(){
    Assistance.getJustificationStock($scope.model.selectedUser.id, $scope.justification.id, null, null,
      function(justification) {
        $scope.justification.stock = justification.stock;
      },
      function(error) {
        Notifications.message(error);
      }
    );
  };
  
  $scope.loadStockYear = function(){

    Assistance.getJustificationStock($scope.model.selectedUser.id, $scope.justification.id, null, 'YEAR',
      function(justification) {
        $scope.justification.yearlyStock = justification.stock;
      },
      function(error) {
        Notifications.message(error);
      }
    );
  };
  
  $scope.$watch('model.selectedUser', function() {
    if($scope.model.selectedUser){
      $scope.loadStockTotal();
      if($scope.justification.stockMode === "year") $scope.loadStockYear();
    }
  }); 
   
  
  
  
  




}]);
