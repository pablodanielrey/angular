
var app = angular.module('library');

app.controller('LoginCtrl', ["$rootScope", '$scope', "$wamp", function ($rootScope, $scope, $wamp) {

  /*
    función que no depende de este scope si no que esta en el módulo principal.
    ya que aunque no este cargado la pantalla de logín el wamp reintenta la conexión usando las
    credenciales definidas.
  */
  $rootScope.getPassword = function() {
    console.log('retornando clave : ');
    console.log($rootScope.credentials.password);
    return $rootScope.credentials.password;
  }

  $rootScope.$on("$wamp.onchallenge", function (event, info) {
    // info.promise: promise to return to wamp,
    // info.session: wamp session,
    // info.method: auth method,
    // info.extra: extra
    //ie. wamp-cra
    console.log('onChallenge')
    return info.promise.resolve($rootScope.getPassword());
  });



  $scope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

  $scope.initialize = function() {
    $scope.message = 'pantalla inicial de login';
    $scope.sessions = [];
    $scope.open = $wamp.connection.isOpen;
    if ($scope.open) {
      $scope.username = $rootScope.credentials.username;
      $scope.password = $rootScope.credentials.password;
    }
  };

  $scope.addSession = function(s) {
    console.log('addsession');
    console.log(s[0]);
    var found = false;
    for (var i = 0; i < $scope.sessions.length; i++) {
      if ($scope.sessions[i].session == s[0].session) {
        found = true;
      }
    }
    if (!found) {
      $scope.sessions.push(s[0]);
    }
  }

  $scope.removeSession = function(s) {
    console.log('removeSession');
    console.log(s[0]);
    $scope.getSessions();
  }


  $scope.closeSession = function(sid) {
    $wamp.call("wamp.session.kill", [sid], {reason: '', message: ''}).then(function() {
      $scope.getSessions();
    });
  }

  $scope.getSessions = function() {
    $wamp.call("wamp.session.list").then(function(s) {
      console.log(s);
      var cc = [];
      for (var i = 0; i < s.length; i++) {
        cc.push($wamp.call('wamp.session.get', [s[i]]));
      }
      Promise.all(cc).then(function(arr) {
        console.log(arr);
        $scope.$apply(function() {
          $scope.sessions = arr;
        });
      })
    });
  }

  $scope.$on("$wamp.open", function(event, info) {
    console.log(info.session);
    console.log(info.details);

    $wamp.subscribe('wamp.session.on_join', $scope.addSession);
    $wamp.subscribe('wamp.session.on_leave', $scope.removeSession);
    $scope.getSessions();

    $scope.message = 'Conexión abierta';
    $scope.session = info.session._id;
    $scope.open = true;
  });

  $scope.$on("$wamp.close", function(event, info) {
    console.log(info.session);
    console.log(info.details);
    $scope.message = 'Conexión cerrada';
    $scope.sessions = [];
  });

  $scope.close = function() {
    $wamp.close();
  }

  $scope.login = function() {
    console.log('login llamando')
    console.log($scope.username);
    console.log($scope.password);

    console.log('seteando autentificación y abriendo conexión');
    $rootScope.credentials =  {
      username: $scope.username,
      password: $scope.password
    };

    $wamp.setAuthId($rootScope.credentials.username);
    $wamp.open();
  };


}]);
