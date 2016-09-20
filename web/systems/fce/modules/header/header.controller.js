angular
  .module('fce')
  .controller('HeaderCtrl', HeaderCtrl)

HeaderCtrl.$inject = ['$rootScope', '$scope', '$window', 'Login', 'Users', 'Files'];

function HeaderCtrl($rootScope, $scope, $window, Login, Users, Files) {
  var vm = this;

  vm.model = {
    privateTransport: null,
    userId: null,
    user: null
  }

  vm.getFullName = getFullName;
  vm.logout = logout;
  vm.getUserPhoto = getUserPhoto;


  $rootScope.$on("$wamp.open", function (event, session) {
    // TODO: aca debe actualizar el ícono para que diga que esta conectado
  });

  $rootScope.$on("$wamp.close", function (event, session) {
    // TODO: aca debe actualizar el ícono para que diga que esta desconectado
  });

  $scope.$on('$viewContentLoaded', function(event) {
    // si hay que obtener datos para cargar en el header en este método es el momento de hacerlo.
  });

  function logout() {
    Login.logout();
  }

  $scope.$on('openPrivateConnection', function(event, args) {
    vm.model.privateTransport = Login.getPrivateTransport();
    activate();
  });

  activate();


  function activate() {
    if (Login.getPrivateTransport().getConnection() == null) {
      return;
    }

    vm.model.userId = Login.getCredentials().userId;
    loadUser(vm.model.userId);
  }

  function loadUser(userId) {
    vm.model.user = null;
    if (userId == null || userId == '') {
      return
    }
    Users.findById([userId]).then(
      function(users) {
        if (users.length > 0) {
          $scope.$apply(function() {
              vm.model.user = users[0];
          });

          Users.findPhoto(vm.model.user.photo).then(function(photo) {
            $scope.$apply(function() {
              vm.model.user.photoSrc = (photo == null) ? '' : Files.toDataUri(photo);
            });
          });

        }
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
      var img = (vm.model.user == null || vm.model.user.genre == undefined || vm.model.user.genre == 'Masculino' || vm.model.user.genre == 'Hombre') ? "img/avatarMan.jpg" : "img/avatarWoman.jpg";
      return img;
    } else {
      return vm.model.user.photoSrc;
    }
  }

}
