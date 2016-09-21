angular
  .module('mainApp')
  .controller('MyFirstModuleCtrl', MyFirstModuleCtrl);

MyFirstModuleCtrl.inject = ['MyFirstSystem']


//controlador del modulo MyFirstModule
function MyFirstModuleCtrl(MyFirstSystem) {
   
   //***** inicializar *****
    $scope.$on('$viewContentLoaded', function(event) {
      $scope.isMessage = false;
      $scope.message = null;
    });
    
    
    
    //***** LLamar a metodo del servicio de acceso para obtener un mensaje *****
    $scope.getMessage = function(){
      MyFirstSystem.getMessage().then(
        function(message){
          $scope.isMessage = true
          $scope.message = message.data;
        },
        function(error){
          alert(error);
        }
      )
    };
     
}
