angular
  .module('mainApp')
  .controller('TeacherCtrl', TeacherCtrl);

TeacherCtrl.inject = ['$rootScope', '$scope', '$timeout', '$wamp', 'Sileg', 'UserFormat', 'PlaceFormat']

function TeacherCtrl($rootScope, $scope, $timeout, $wamp, Sileg, UserFormat, PlaceFormat) {

    $scope.users = [];
    $scope.cathedras = [];
    
    $scope.selectUser = function(user){
        $scope.data = [];
        $scope.user = user;
        $scope.view.style2 = 'verInfoDocente';
        

        Sileg.getEconoPageDataUser($scope.user.id).then(
            function(response){
                $scope.data = response;
            },
            function(error){ console.log(error); }
        );
    };
    
    
    $scope.selectCathedra = function(cathedra){

        $scope.data = [];
        $scope.cathedra = cathedra;
        $scope.view.style2 = 'verInfoCatedra';
        

        Sileg.getEconoPageDataPlace($scope.cathedra.id).then(
            function(response){
                console.log(response);
                $scope.data = response;
            },
            function(error){ console.log(error); }
        );
    };
            
           
    //***** inicializar (probe con $viewContentLoaded pero no funciono) *****
    $timeout(function() {
        Sileg.getUsers().then(
            function(response){
                for(i in response){
                    var user = UserFormat.format(response[i]);
                    $scope.users.push(user);
                }
            },
            function(error){ console.log(error); }
        );
        
        
        Sileg.getCathedras().then(
            function(response){
                for(i in response){
                    var cathedra = PlaceFormat.format(response[i]);
                    $scope.cathedras.push(cathedra);
                }
            },
            function(error){ console.log(error); }
        );
    },0);
  
    

}
