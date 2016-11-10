angular
  .module('mainApp')
  .controller('AddExtensionCtrl', AddExtensionCtrl);

AddExtensionCtrl.inject = ['$location', '$rootScope', '$scope', '$timeout', '$wamp', '$q', 'Designation', 'Position']

function AddExtensionCtrl($location, $rootScope, $scope, $timeout, $wamp, $q, Designation, Position, Place) {
   
   
    $scope.form = { disabled:true, message:"Iniciando"};
    $scope.extension = { start:null, end:null, resolution:null, record:null, placeId:null, replaceId:null, userId:null, positionId:null, description:"extension"};


    $scope.submit = function(){
       $scope.form.message = "Procesando";
       $scope.form.disabled = true;
       
       if(!$scope.extension.start || !$scope.extension.placeId || !$scope.extension.userId  || !$scope.extension.positionId || !$scope.extension.replaceId){
         $scope.form.message = "Verifique los datos ingresados";
         $scope.form.disabled = false;
       }
       
       Designation.persist($scope.extension).then(
         function(response){
           $scope.form.message = "Extension agregada";
         },
         function(error){
          $scope.form.message = error;
          $scope.form.disabled = false;
         }
       );
    
    }
    
    
    //***** Evento de inicializacion de fieldset *****
    $scope.$on('$viewContentLoaded', function(event) {
      var urlParams = $location.search();
      var id = ("id" in urlParams) ? urlParams["id"] : null;
      if(id == null) { $scope.form.message = "Id no definido"; return ; }

      var p1 = Designation.findById([id]);
      var p2 = Position.findAll();
      var p3 = Place.findAll();
      
      $q.all([p1, p2, p3]).then(
        function(response){
          $scope.designation = response[0][0];
          $scope.extension.replaceId = $scope.designation.id
          $scope.extension.userId = $scope.designation.userId;
          
          $scope.positions = response[1];
          $scope.places = response[2];

          $scope.form.disabled = false;
          $scope.form.message = null;
        },
        function(error){
          $scope.form.disabled = true;
          $scope.form.message = error;
        }
      );
    });
    
    
    
  
  
}
