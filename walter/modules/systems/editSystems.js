var app = angular.module('mainApp');

app.controller('EditSystemsCtrl', function($scope, $timeout, Student, Session) {


    $scope.systems = [];

    $scope.loadSystemsData = function() {
        $scope.systems = [];
        $scope.systems.push({name:'dominio',value:true,label:"Dominio"});
        $scope.systems.push({name:'correo',value:false,label:"Correo"});
    }


    $scope.save = function() {

        var s = Session.getCurrentSession();
        if (s == null) {
            return;
        }

        if (s.selectedUser == undefined || s.selectedUser == null) {
            return;
        }

        for (var $i=0; $i<$scope.systems.length; $i++) {
            var $item = $scope.systems[$i];

            if ($item.name == 'dominio') {
                var $user = {id:s.selectedUser};
                if ($item.value) {
                    alert("Agregando al dominio el usuario:" + $user.id);
                    Domain.updateData($user);
                } else {
                    alert("Eliminando del dominio el usuario:" + $user.id);
                }
                continue;
            }

            if ($item.name == 'correo') {
                var $user = {id:s.selectedUser};
                if ($item.value) {
                    alert("Agregando al correo el usuario:" + $user.id);
                } else {
                    alert("Eliminando del correo el usuario:" + $user.id);
                }
                continue;
            }
        }
  }

  $timeout(function() {
    $scope.loadSystemsData();
  },0);

});
