angular
  .module('mainApp')
  .controller('CathedraCtrl', TeacherCtrl);

CathedraCtrl.inject = ['$rootScope', '$scope', '$timeout', '$wamp', 'Sileg', 'UserFormat']

function CathedraCtrl($rootScope, $scope, $timeout, $wamp, Sileg, UserFormat) {

    $scope.cathedras = [];
    

    
    $scope.selectCathedra = function(user){
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
            
           
    //***** inicializar (probe con $viewContentLoaded pero no funciono) *****
    $timeout(function() {
        Sileg.getUsers().then(
            function(response){
                for(i in response){
                    var user = UserFormat.basic(response[i]);
                    $scope.users.push(user);
                }
            },
            function(error){ console.log(error); }
        );
    },0);
  
    

}
