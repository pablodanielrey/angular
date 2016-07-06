angular
  .module('mainApp')
  .controller('AdminDesignationCtrl', AdminDesignationCtrl);

AdminDesignationCtrl.inject = ['$location', '$rootScope', '$scope', '$timeout', '$wamp', 'Designation', 'DesignationFormat']

function AdminDesignationCtrl($location, $rootScope, $scope, $timeout, $wamp, Designation, DesignationFormat) {
    /*
    $scope.form = {
      disabled: true,         //flag para indicar si el formulario esta deshabilitado o no
      status: "initializing", //estado del formulario
      id: null,               //identificador
      
      
      
    };
    
    
    
    $scope.findUser = function(){
      $scope.fields.userSelected = null;
      Users.findByDocumentNumber($scope.fields.userSearch).then(
        function(response){
          if(response != null) $scope.fields.userSelected = response;
        },
        function(error){ console.log(error) }      
      );

    }*/
    



    $scope.initializeForm = function(response){
        $scope.fields = DesignationFormat.initializeForm(response);
    }
    


    //***** Evento de inicializacion de fieldset *****
    $scope.$on('$viewContentLoaded', function(event) {
      var urlParams = $location.search();
      var id = ("id" in urlParams) ? urlParams["id"] : null;
      var ids = (id) ? [id] : [];

      Designation.findById(id).then(
        function(response){
          designation = (response) ? response[0] : null;
          $scope.initializeForm(designation);
        },
        
        function(error){
          console.log(error)
        }
      );
    });
  
  
}
