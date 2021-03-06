angular
  .module('mainApp')
  .controller('ShowTeacherCtrl', TeacherCtrl);

ShowTeacherCtrl.inject = ['$rootScope', '$scope', '$timeout', '$wamp', 'Sileg']

function ShowTeacherCtrl($rootScope, $scope, $timeout, $wamp, Sileg) {

    $scope.users = [];



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
    },0);



}
