
app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/gridDestino', {
     templateUrl: '/systems/expedientes/html/grid/destino/DestinoSmall.html'
  })

  .when('/gridExpediente', {
     templateUrl: '/systems/expedientes/html/grid/expediente/Expediente.html'
  })

  .when('/gridLugar', {
     templateUrl: '/systems/expedientes/html/grid/lugar/Lugar.html'
  })

  .when('/gridNota', {
     templateUrl: '/systems/expedientes/html/grid/nota/Nota.html'
  })

  .when('/gridParticipacion', {
     templateUrl: '/systems/expedientes/html/grid/participacion/Participacion.html'
  })

  .when('/gridPersona', {
     templateUrl: '/systems/expedientes/html/grid/persona/Persona.html'
  })

  .when('/gridTema', {
     templateUrl: '/systems/expedientes/html/grid/tema/Tema.html'
  })
  
  .when('/options', {
     templateUrl: '/systems/expedientes/html/menu/options.html'
  })
  
  .when('/logout', {
     templateUrl: '/systems/login/modules/logout.html',
     controller: 'LogoutCtrl'
  })
  
  .otherwise({
    redirectTo: '/options'
  });

}]);
