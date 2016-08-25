angular
  .module('mainApp')
  .controller('TeacherCtrl', TeacherCtrl);

TeacherCtrl.inject = ['$rootScope', '$scope', '$timeout', '$wamp', 'Sileg']

function TeacherCtrl($rootScope, $scope, $timeout, $wamp, Sileg) {

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
                    $scope.users.push(response[i]);
                }
            },
            function(error){ console.log(error); }
        );


        Sileg.getCathedras().then(
            function(response){
                for(i in response){
                    $scope.cathedras.push(response[i]);
                }
            },
            function(error){ console.log(error); }
        );
    },0);



}
