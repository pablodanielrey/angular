(function() {
    'use strict';

    angular
        .module('assistance')
        .controller('EditSpecialSchCtrl', EditSpecialSchCtrl);

    EditSpecialSchCtrl.$inject = ['$scope', '$routeParams', 'Login', 'Users', 'Assistance', '$timeout', '$location'];

    /* @ngInject */
    function EditSpecialSchCtrl($scope, $routeParams, Login, Users, Assistance, $timeout, $location) {
      var vm = this;

      vm.model = {
        selectedPerson: null,
        schedules: [],

        users: [],
        user: null
      }

      vm.view = {
        style:'',
        profileAdmin: 'usuarioAdmin',
        profileUser: 'usuarioNormal',
        displayEdit: 'pantallaEdicion nuevoHorarioEspecial',
        saveMessage: 'pantallaEdicion nuevoHorarioEspecial mensajes mensajeGuardado',
        loadingMessage: 'pantallaEdicion nuevoHorarioEspecial mensajes mensajeCargando',
        errorMessage: 'pantallaEdicion nuevoHorarioEspecial mensajes mensajeError',
        profile: 'user',
        activate: false
      }

      vm.getUserPhoto = getUserPhoto;
      vm.selectUser = selectUser;
      vm.displayEditSpecialSch = displayEditSpecialSch;
      vm.back = back;
      vm.addSchedule = addSchedule;
      vm.removeSchedule = removeSchedule;
      vm.save = save;

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

        loadProfile();
        loadSchedules();
        loadUsers();
        loadUser();
      }

      /* **************************************************************************************************
                                          MANEJO VISUAL
      * ************************************************************************************************ */

      function displayEditSpecialSch() {
        var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
        vm.view.style = style + ' ' + vm.view.displayEdit;
      }

      function displayMessageSave() {
        var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
        $timeout(function () {
          vm.view.style = style + ' ' + vm.view.saveMessage;
        });
      }

      function displayMessageLoading() {
        var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
        $timeout(function () {
          vm.view.style = style + ' ' + vm.view.loadingMessage;
        });
      }

      function displayMessageError(error) {
        var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
        vm.view.error = error;
        vm.view.style = style + ' ' + vm.view.errorMessage;
      }

      function getUserPhoto() {
        return (vm.model.user == null || !'photoSrc' in vm.model.user) ? 'img/avatarMan.jpg' : vm.model.user.photoSrc
      }

      function back() {
        $location.path("/schedules/" + vm.model.selectedPerson);
      }

      /* **************************************************************************************************
                                          MANEJO DE PERFIL DE USUARIO
      * ************************************************************************************************ */

      function loadProfile() {
        Assistance.loadProfile().then(function(profile) {
          _loadProfile(profile);
        }, function(error) {
          displayMessageError(error);
          $timeout(function() {
              _loadProfile(null)
          }, 2500);
        })
      }



      function _loadProfile(profile) {
        vm.view.profile = profile;
        var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
        vm.view.style = style + ' ' + vm.view.displayListUsers;

        vm.displayEditSpecialSch();
      }

      function loadUser() {
        vm.model.user = null;
        Users.findById([vm.model.selectedPerson]).then(Users.findPhotos).then(Users.photoToDataUri).then(function(users) {
          $timeout(function() {
            vm.model.user = (users.length <= 0) ? null : users[0];
          },0);
        }, function(error) {
          displayMessageError(error);
          $timeout(function() {
              _loadProfile(vm.view.profile)
          }, 1500);
        })
      }

  /* **************************************************************************************************
                                      MANEJO DE PERSONAS
  * ************************************************************************************************ */

      function loadUsers() {
        Assistance.loadUsers().then(function(users) {
          vm.model.users = users;
        }, function(error) {
          displayMessageError(error);
          $timeout(function() {
              _loadProfile(vm.view.profile)
          }, 1500);
        })
      }

      function selectUser(user) {
        $location.path("/schedules/" + user.id);
      }

    /* **************************************************************************************************
                                        MANEJO DE SCHEDULES
    * ************************************************************************************************ */

      function loadSchedules() {
        vm.model.schedules = [];
        var start = new Date(); start.setHours(7); start.setMinutes(0); start.setSeconds(0); start.setMilliseconds(0);
        var end = new Date(); end.setHours(14); end.setMinutes(0); end.setSeconds(0); end.setMilliseconds(0);
        vm.model.schedules.push({start: start, end: end});
      }

      function addSchedule() {
        if (vm.model.schedules.length > 1) {
          return;
        }
        var start = new Date(vm.model.schedules[0].end.getTime());
        var end = new Date(start.getTime());
        vm.model.schedules.push({start: start, end: end});
      }

      function removeSchedule() {
        vm.model.schedules.splice(1,1);
      }

      /* **************************************************************************************************
                                          GUARDAR
      * ************************************************************************************************ */

      function _verify() {
        return true;
      }

      function save() {
        if (!_verify()) {
          return;
        }

        vm.view.style = displayMessageLoading();
        Assistance.saveSpecialSchedules(vm.model.schedules).then(function() {
          vm.view.style = displayMessageSave();
          $timeout(function () {
            $location.path("/schedules/" + vm.model.selectedPerson);
          }, 2000);
        }, function(error) {
          displayMessageError(error);
          $timeout(function() {
            vm.view.style = vm.view.displayEdit;
          }, 3000)
        });
      }
    }
})();
