angular
  .module('mainApp')
  .controller('AddExtensionCtrl', AddExtensionCtrl);

AddOriginalCtrl.inject = ['$location', '$rootScope', '$scope', '$timeout', '$wamp', '$q', 'Designation', 'Position', 'Place', 'User']

function AddOriginalCtrl($location, $rootScope, $scope, $timeout, $wamp, $q, Designation, Position, Place, User) {
   
   
    $scope.form = { disabled:true, message:"Iniciando"};
    $scope.designation = { start:null, end:null, resolution:null, record:null, placeId:null, replaceId:null, userId:null, positionId:null, description:"original"};


    $scope.selectUser = function(user){
      $scope.userSelected = user;
      $scope.designation.userId = user.id
    }
    
    
    $scope.submit = function(){
       $scope.form.message = "Procesando";
       $scope.form.disabled = true;
       
       if(!$scope.designation.start || !$scope.designation.placeId || !$scope.designation.userId  || !$scope.designation.positionId){
         $scope.form.message = "Verifique los datos ingresados";
         $scope.form.disabled = false;
       }
       
       Designation.persist($scope.designation).then(
         function(response){
           $scope.form.message = "Designacion agregada";
         },
         function(error){
          $scope.form.message = error;
          $scope.form.disabled = false;
         }
       );
    }
    
    
    //***** Evento de inicializacion de fieldset *****
    $scope.$on('$viewContentLoaded', function(event) {

      var p1 = Position.findAll();
      var p2 = Place.findAll();
      
      $q.all([p1, p2]).then(
        function(response){
          $scope.positions = response[0];
          $scope.places = response[1];

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
