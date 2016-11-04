(function() {
    'use strict';

    angular
        .module('assistance')
        .controller('EditSpecialSchCtrl', EditSpecialSchCtrl);

    EditSpecialSchCtrl.$inject = ['$scope', '$routeParams', 'Login', '$q', 'Users', '$timeout', '$location'];

    /* @ngInject */
    function EditSpecialSchCtrl($scope, $routeParams, Login, $q, Users, $timeout, $location) {
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

        loadProfile().then(function() {
            vm.displayEditSpecialSch()
        });

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

      /* **************************************************************************************************
                                          GUARDAR
      * ************************************************************************************************ */
      function save() {
        vm.view.style = displayMessageLoading();
        $timeout(function () {
          vm.view.style = displayMessageSave();
          $timeout(function () {
            $location.path("/schedules/" + vm.model.selectedPerson);
          }, 2000);
        }, 2000);
      }
    }
})();
