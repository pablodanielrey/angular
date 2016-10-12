angular
  .module('fce')
  .controller('HeaderCtrl', HeaderCtrl)

HeaderCtrl.$inject = ['$rootScope', '$scope', '$window', 'Login', 'Users', 'Files','$timeout'];

function HeaderCtrl($rootScope, $scope, $window, Login, Users, Files, $timeout) {
  var vm = this;

  vm.model = {
    privateTransport: null,
    userId: null,
    user: null
  }

  vm.view = {
      style: ''
  }

  vm.getFullName = getFullName;
  vm.logout = logout;
  vm.getUserPhoto = getUserPhoto;

  $rootScope.$on("wamp.open", function (event, session) {
    // TODO: aca debe actualizar el ícono para que diga que esta conectado
    vm.view.style = '';

    vm.model.privateTransport = Login.getPrivateTransport();
    activate();


  });

  $rootScope.$on("wamp.close", function (event, session) {
    // TODO: aca debe actualizar el ícono para que diga que esta desconectado
    vm.view.style = 'serverDesconectado';
  });

  $scope.$on('$viewContentLoaded', function(event) {
    // si hay que obtener datos para cargar en el header en este método es el momento de hacerlo.
  });

  function logout() {
    Login.logout();
  }

  activate();

  function activate() {
    if (Login.getPrivateTransport() == null) {
      return;
    }

    vm.model.userId = Login.getCredentials().userId;
    loadUser(vm.model.userId);
  }

  function loadUser(userId) {
    vm.model.user = null;
    if (userId == null || userId == '') {
      return;
    }
    Users.findById([userId]).then(Users.findPhotos).then(
      function(users) {
        if (users.length <= 0) {
          return;
        }

        $timeout(function() {
          var user = users[0];
          vm.model.user = user;
          vm.model.user.photoSrc = (user.photo == null) ? '' : Files.toDataUri(user.photo);
        });
      },
      function(error) {
        console.log(error);
      }
    );
  }

  function getFullName() {
    if (vm.model.user == null) {
      return '';
    }
    return vm.model.user.name + ' ' + vm.model.user.lastname;
  }

  function getUserPhoto(issue) {
    if (vm.model.user == null || vm.model.user.photo == null || vm.model.user.photoSrc == '') {
      var img = (vm.model.user == null || vm.model.user.genre == undefined || vm.model.user.genre == 'Masculino' || vm.model.user.genre == 'Hombre') ? "/systems/fce/img/avatar.jpg" : "img/avatarWoman.jpg";
      return img;
    } else {
      return vm.model.user.photoSrc;
    }
  }

}
