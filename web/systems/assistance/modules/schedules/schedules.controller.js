(function() {
    'use strict'
    angular
      .module('assistance')
      .controller('SchedulesCtrl', SchedulesCtrl);

    SchedulesCtrl.$inject = ['$scope', 'Assistance', 'Users', 'Login', '$routeParams', '$location', '$q', '$timeout'];

    function SchedulesCtrl($scope, Assistance, Users, Login, $routeParams, $location, $q, $timeout) {
        var vm = this;
        vm.model = {
          users: [],
          selectedPerson: null,
          date: null,
          user: null
        }

        vm.view = {
          style:'',
          profileAdmin: 'usuarioAdmin',
          profileUser: 'usuarioNormal',
          displayListUsers: 'pantallaUsuarios verHorario',
          displayPerson: 'pantallaEdicion verHorario',
          profile: 'user',
          activate: false
        }

        vm.selectUser = selectUser;
        vm.getUserPhoto = getUserPhoto;


        $scope.$on('wamp.open', function(event, args) {
          activate();
        });

        activate();

        function activate() {
          if (vm.view.activate || Login.getPrivateTransport() == null) {
            return;
          }
          vm.view.activate = true;

          var params = $routeParams;
          if ('personId' in params) {
            vm.model.selectedPerson = params.personId;
          } else {
            vm.model.selectedPerson =  Login.getCredentials()['userId'];
          }
          loadProfile().then(function() {
            if ('personId' in params) {
              displaySchedule();
            } else {
              displayUsers();
            }
          });
          loadUsers();
          loadUser();
          vm.model.date = new Date();
        }

    /* **************************************************************************************************
                                        MANEJO VISUAL
    * ************************************************************************************************ */

    function displaySchedule() {
      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      vm.view.style = style + ' ' + vm.view.displayPerson;
    }

    function displayUsers() {
      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      vm.view.style = style + ' ' + vm.view.displayListUsers;
    }

    function getUserPhoto() {
      return (vm.model.user == null || !'photoSrc' in vm.model.user) ? 'img/avatarMan.jpg' : vm.model.user.photoSrc
    }

    /* **************************************************************************************************
                                        MANEJO DE PERFIL DE USUARIO
    * ************************************************************************************************ */

    function loadProfile() {
      var d = $q.defer();
      // aca deberia hacer la llamada al servidor
      vm.view.profile = "admin";

      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      vm.view.style = style + ' ' + vm.view.displayListUsers;
      d.resolve();

      return d.promise;
    }

    function loadUser() {
      vm.model.user = null;
      Users.findById([vm.model.selectedPerson]).then(Users.findPhotos).then(Users.photoToDataUri).then(function(users) {
        $timeout(function() {
          vm.model.user = (users.length <= 0) ? null : users[0];
        },0);
      }, function(err) {
        console.log(err);
      })
    }

    /* **************************************************************************************************
                                        MANEJO DE PERSONAS
    * ************************************************************************************************ */

        function loadUsers() {
            vm.model.users = [];
            vm.model.users.push({id:'1', dni: '31381082', name: 'Emanuel Joaquín', lastname: 'Pais', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'2', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'3', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'4', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'5', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'6', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'7', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'8', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'9', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'10', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'11', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'12', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'13', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'14', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'15', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'16', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'17', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
            vm.model.users.push({id:'18', dni: '30112124', name: 'Walter Roberto', lastname: 'Blanco', img: 'img/avatarMan.jpg'});
        }

        function selectUser(user) {
          $location.path("/schedules/" + user.id);
        }



    }


})();
