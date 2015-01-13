
var app = angular.module('mainApp');


app.controller('GroupMembersCtrl', function($rootScope, $scope, Groups, Users) {

  $scope.groupSelected = null;  // id del grupo seleccionado
  $scope.members = [];          // array de usuarios miembros
  $scope.selected = [];         // array de id de usuarios seleccionados


  // funcionalidad de agregar usuarios ////

  $scope.adding = false;        // se esta agregando usuarios a un grupo?
  $scope.usersToAdd = [];       // array de usuarios que no existen en el grupo
  $scope.selectedToAdd = [];    // array de ids de usuarios a agregar al grupo.

  $scope.isSelectedToAdd = function(id) {
    return ($scope.findSelectedToAdd(id) != -1);
  }

  $scope.selectToAdd = function(id) {
    if ($scope.findSelectedToAdd(id) == -1) {
      $scope.selectedToAdd.push(id);
    }
  }

  $scope.addToGroup = function() {
    if ($scope.adding == false) {
      return;
    }
    if ($scope.selectedToAdd.length <= 0) {
      alert('Debe seleccionar al menos una persona');
      return;
    }
    Groups.addMembers(
        $scope.groupSelected,
        $scope.selectedToAdd,
        function(ok) {
          $scope.adding = false;
          $scope.usersToAdd = [];
          $scope.selectedToAdd = [];

          setTimeout(function() {
            $rootScope.broadcast('GroupUpdatedEvent',$scope.groupSelected);
          },0);
        },
        function(err) {
          alert(err);
        });
  }

  $scope.showAdd = function() {
    $scope.adding = true;
    $scope.usersToAdd = [];
    $scope.selectedToAdd = [];

    Users.listUsers(
      function(users) {
          // retorno los que no existen en members.
          var uta = users.filter(function(elem,index,array) {
                var exist = $scope.members.reduce(function(previous,elem2,index2,array2) {
                                      return (previous || (elem.id == elem2.id));
                            },false);
                return !exist;
          });
          if (uta.length > 0) {
            $scope.usersToAdd = uta;
          }
      },
      function(error) {
        alert(error);
        $scope.adding = false;
      }
    );
  }

  $scope.cancelAddToGroup = function() {
    $scope.adding = false;
    $scope.usersToAdd = [];
    $scope.selectedToAdd = [];
  }

  $scope.findSelectedToAdd = function(id) {
    for (var i = 0; i < $scope.selectedToAdd.length; i++) {
      if ($scope.selectedToAdd[i] == id) {
        return i;
      }
    }
    return -1;
  }

  ////////////////


  $scope.remove = function() {
    Groups.removeMembers(
            $scope.groupSelected,
            $scope.selected,
            function(ok) {
              setTimeout(function() {
                $rootScope.broadcast('GroupUpdatedEvent',$scope.groupSelected);
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

    if ($scope.adding) {
      $scope.showAdd();
    }
  });



  $rootScope.$on('UserUpdatedEvent', function(e,id) {

    if ($scope.groupSelected == null) {
      return;
    }

    var i = $scope.findMember(id);
    if (i != -1) {
        // reemplazo los datos viejos por los nuevos
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
      };

      // busco el indice del usuario que tenga igual id.
      var a = $scope.usersToAdd.reduce(function(prev,elem,index,array) {
        if (prev != -1) {
          return prev;
        }
        if (elem.id == id) {
          return index;
        }
        return prev;
      },-1);

      if (a != -1) {
        // reemplazo los datos viejos por los viejos.
        Users.findUser(id,
          function(user) {
            $scope.usersToAdd[a] = user;
          }.bind(this),
          function(error) {
            var user = {
              id: id,
              name: 'error',
              lastname: 'error',
              dni: 'error'
            };
            $scope.members[a] = user;
          }.bind(this));
      }
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
