angular
  .module('mainApp')
  .controller('MenuCtrl', MenuCtrl);

MenuCtrl.inject = ['$rootScope', '$scope','$location', 'Login', '$window'];

function MenuCtrl($rootScope, $scope, $location, Login, $window) {

    $scope.selectProfile = function() {
      $location.path('/profile');
    }

    $scope.selectPassword = function() {
      $location.path('/password');
    }

    $scope.selectMails = function() {
      $location.path('/mails');
    }

    $scope.selectSystems = function() {
      $location.path('/systems');
    }

    $scope.logout = function() {
      Login.logout()
      .then(function(ok) {
        $window.location.href = "/systems/login/index.html";
      }, function(err) {
        console.log(err);
      });
    }

  }
