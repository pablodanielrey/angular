
app.config(['$routeProvider', function($routeProvider) {

  $routeProvider

  .when('/gridDestino', {
     templateUrl: '/systems/expedientes/modules/grid/destino/Destino.html'
  })

  .when('/gridExpediente', {
     templateUrl: '/systems/expedientes/modules/grid/expediente/Expediente.html'
  })

  .when('/gridLugar', {
     templateUrl: '/systems/expedientes/modules/grid/lugar/Lugar.html'
  })

  .when('/gridNota', {
     templateUrl: '/systems/expedientes/modules/grid/nota/Nota.html'
  })

  .when('/gridParticipacion', {
     templateUrl: '/systems/expedientes/modules/grid/participacion/Participacion.html'
  })

  .when('/gridPersona', {
     templateUrl: '/systems/expedientes/modules/grid/persona/Persona.html'
  })

  .when('/gridTema', {
     templateUrl: '/systems/expedientes/modules/grid/tema/Tema.html'
  })

}]);
