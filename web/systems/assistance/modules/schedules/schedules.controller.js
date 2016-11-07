(function() {
    'use strict'
    angular
      .module('assistance')
      .controller('SchedulesCtrl', SchedulesCtrl);

    SchedulesCtrl.$inject = ['$scope', 'Assistance', 'Users', 'Login', '$routeParams', '$location', '$timeout'];

    function SchedulesCtrl($scope, Assistance, Users, Login, $routeParams, $location, $timeout) {
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
          displayQuestions: 'pantallaEdicion verPreguntaDeHorario',
          loadingMessage: 'pantallaEdicion verHorario mensajes mensajeCargando',
          errorMessage: 'pantallaEdicion verHorario mensajes mensajeError',
          profile: 'user',
          activate: false,
          error: ''
        }

        vm.selectUser = selectUser;
        vm.getUserPhoto = getUserPhoto;
        vm.displayEditQuestions = displayEditQuestions;
        vm.displaySchedule = displaySchedule;
        vm.displayUsers = displayUsers;
        vm.displayEditWeekSch = displayEditWeekSch;
        vm.displayEditHoursSch = displayEditHoursSch;
        vm.displayEditSpecialSch = displayEditSpecialSch;

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

    function displayEditQuestions() {
      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      vm.view.style = style + ' ' + vm.view.displayQuestions;
    }

    function displayEditWeekSch() {
      $location.path("/weekSchedules/" + vm.model.selectedPerson);
    }

    function displayEditHoursSch()  {
      $location.path("/hoursSchedules/" + vm.model.selectedPerson);
    }

    function displayEditSpecialSch()  {
      $location.path("/specialSchedules/" + vm.model.selectedPerson);
    }

    function getUserPhoto() {
      return (vm.model.user == null || !'photoSrc' in vm.model.user) ? 'img/avatarMan.jpg' : vm.model.user.photoSrc
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


    /* **************************************************************************************************
                                        MANEJO DE PERFIL DE USUARIO
    * ************************************************************************************************ */

    function loadProfile() {
      Assistance.loadProfile().then(function(profile) {
        _loadProfile(profile);
      }, function(error) {
        displayMessageError(error);
        $timeout(function() {
          _loadProfile(null);
        }, 1500);

      })
    }

    function _loadProfile(profile) {
      vm.view.profile = (profile == null) ? 'user' : profile;
      var style = (vm.view.profile == 'admin') ? vm.view.profileAdmin : vm.view.profileUser;
      vm.view.style = style + ' ' + vm.view.displayListUsers;

      if ('personId' in $routeParams) {
        displaySchedule();
      } else {
        displayUsers();
      }
    }

    function loadUser() {
      vm.model.user = null;
      Users.findById([vm.model.selectedPerson]).then(Users.findPhotos).then(Users.photoToDataUri).then(function(users) {
        $timeout(function() {
          vm.model.user = (users.length <= 0) ? null : users[0];
        },0);
      }, function(err) {
        displayMessageError(error);
        $timeout(function() {
            _loadProfile(vm.view.profile)
        }, 1500);
      })
    }

    /* **************************************************************************************************
                                        MANEJO DE PERSONAS
    * ************************************************************************************************ */


      function selectUser(user) {
        if (user.id == vm.model.selectedPerson) {
          vm.displaySchedule();
        } else {
          $location.path("/schedules/" + user.id);
        }
      }


    }
})();
