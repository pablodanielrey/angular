
var app = angular.module('mainApp');


app.controller('GroupMembersCtrl', function($rootScope, $scope, Groups, Users) {

  $scope.members = [];

  $scope.findMember = function(id) {
    for (var i = 0; i < $scope.members.length; i++) {
      if ($scope.members[i].id == id) {
        return i;
      }
    }
    return -1;
  }

  $rootScope.$on('UserUpdatedEvent', function(e,id) {
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
      $scope.members = [];
      return;
    }
    $scope.members = [];
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
                id: id,
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
      });
    });



});
