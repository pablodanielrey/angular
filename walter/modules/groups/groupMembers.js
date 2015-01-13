
var app = angular.module('mainApp');


app.controller('GroupMembersCtrl', function($rootScope, $scope, Groups, Users) {

  $scope.groupSelected = null;
  $scope.members = [];
  $scope.selected = [];

  $scope.remove = function() {
    Groups.removeMembers(
            $scope.groupSelected,
            $scope.selected,
            function(ok) {
              setTimeout(function() {
                $rootScope.broadcast('GroupSelectedEvent',$scope.groupSelected);
              },0);
            },
            function(err) {
              alert(err);
            });
  }


  $scope.findSelected = function(id) {
    for (var i = 0; i < $scope.selected.length; i++) {
      if ($scope.selected[i] == id) {
        return i;
      }
    }
    return -1;
  }


  $scope.select = function(id) {
    var s = $scope.findSelected(id);
    if (s == -1) {
      $scope.selected.push(id);
    } else {
      $scope.selected.splice(s,1);
    }
  }

  $scope.isSelected = function(id) {
    return ($scope.findSelected(id) != -1);
  }



  $scope.findMember = function(id) {
    for (var i = 0; i < $scope.members.length; i++) {
      if ($scope.members[i].id == id) {
        return i;
      }
    }
    return -1;
  }


  $rootScope.$on('GroupUpdatedEvent', function(e,id) {
    if ($scope.groupSelected != id) {
      return;
    }

    $scope.members = [];
    $scope.selected = [];
    $scope.findMembers(id);
  });

  $rootScope.$on('UserUpdatedEvent', function(e,id) {

    if ($scope.groupSelected == null) {
      return;
    }

    var i = $scope.findMember(id);
    if (i == -1) {
      // no esta dentro de los miembros asi que no actualizo nada.
      return;
    }

    // reemplazo los datos nuevos por los viejos.
    Users.findUser(id,
      function(user) {
        $scope.members[i] = user;
      }.bind(this),
      function(error) {
        var user = {
          id: id,
          name: 'error',
          lastname: 'error',
          dni: 'error'
        };
        $scope.members[i] = user;
      }.bind(this));

  });

  $rootScope.$on('GroupSelectedEvent', function(e,id) {
    if (id == null) {
      $scope.groupSelected = null;
      $scope.members = [];
      $scope.selected = [];
      return;
    }
    $scope.groupSelected = id;
    $scope.members = [];
    $scope.selected = [];
    $scope.findMembers(id);

  });


  $scope.findMembers = function(id) {
    Groups.findMembers(id,
      function(members) {
        for (var i = 0; i < members.length; i++) {
          var id = members[i];
          Users.findUser(id,
            function(user) {
              $scope.members.push(user);
            },
            function(error) {
              var user = {
                id: $scope.groupSelected,
                name: 'error',
                lastname: 'error',
                dni: 'error'
              };
              $scope.members.push(user);
            });
          }
        },
        function(error) {
          alert(error);
        }
      );
  }

});
