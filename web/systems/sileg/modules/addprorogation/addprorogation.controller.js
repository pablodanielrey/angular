angular
  .module('mainApp')
  .controller('AddProrogationCtrl', AddProrogationCtrl);

AddProrogationCtrl.inject = ['$location', '$rootScope', '$scope', '$timeout', '$wamp', '$q', 'Designation', 'Position']

function AddProrogationCtrl($location, $rootScope, $scope, $timeout, $wamp, $q, Designation, Position, Place) {
   
   
    $scope.form = {disabled:true, message:"Iniciando"};
    $scope.prorogation = {start:null, end:null, resolution:null, record:null, placeId:null, replaceId:null, userId:null, positionId:null, description:null};


    $scope.submit = function(){
       $scope.form.message = "Procesando";
       $scope.form.disabled = true;
       
       if(!$scope.prorogation.start || !$scope.prorogation.placeId || !$scope.prorogation.userId  || !$scope.prorogation.positionId || !$scope.prorogation.replaceId){
         $scope.form.message = "Verifique los datos ingresados";
         $scope.form.disabled = false;
       }
       
       Designation.persist($scope.prorogation).then(
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

      
      Designation.findById([id]).then(
        function(response){
          $scope.designation = response[0];
          
          switch($scope.designation.description){
            case "original": case "prorroga_original": $scope.prorogation.description = "prorroga_original"; break;
            case "extension": case "prorroga_extension": $scope.prorogation.description = "prorroga_extension"; break;
            default:
              $scope.form.message = "No se puede prorrogar";
              return;
          }

          $scope.prorogation.replaceId = $scope.designation.id
          $scope.prorogation.userId = $scope.designation.userId;
          $scope.prorogation.placeId = $scope.designation.placeId;
          $scope.prorogation.positionId = $scope.designation.positionId;
          



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
