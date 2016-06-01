angular
  .module('mainApp')
  .controller('SystemsCtrl', SystemsCtrl);

SystemsCtrl.inject = ['$rootScope', '$scope', 'Systems', 'Login', '$window', '$location']

function SystemsCtrl($rootScope, $scope, Systems, Login, $window, $location) {

  $scope.initialize = initialize;
  $scope.listSystems = listSystems;

  $scope.openWebmail = openWebmail;
  $scope.openChat = openChat;
  $scope.openIngreso = openIngreso;
  $scope.openFceBox = openFceBox;
  $scope.openAu24 = openAu24;
  $scope.openAccount = openAccount;
  $scope.openAssistance = openAssistance;
  $scope.openCamera = openCamera;
  $scope.openLaboral = openLaboral;
  $scope.openIssues = openIssues;
  $scope.openDigesto = openDigesto;
  $scope.openTask = openTask;
  $scope.openLists = openLists;
  $scope.openAdscription = openAdscription;
  $scope.openSileg = openSileg;
  $scope.openTutors = openTutors;

  $scope.model = {
    systems: [],
    options: [
      {value:'webmail', style: 'c1', img: 'fa fa-envelope fa-3x', name:'Webmail', action: $scope.openWebmail},
      {value:'fcebox', style: 'c2', img: 'fa fa-cloud fa-3x', name:'fceBox', action: $scope.openFceBox},
      {value:'au24', style: 'c3', img: 'fa fa-graduation-cap fa-3x', name:'AU24', action: $scope.openAu24},
      // {value:'account', style: 'c4', img: 'fa fa-users fa-3x', name:'Cuentas FCE', action: $scope.openAccount},
      {value:'assistance', style: 'c5', img: 'fa fa-clock-o fa-3x', name:'Asistencia', action: $scope.openAssistance},
      // {value:'camera', style: 'c6', img: 'fa fa-video-camera fa-3x', name:'Cámaras', action: $scope.openCamera},
      {value:'laboralinsertion', style: 'c7', img: 'fa fa-suitcase fa-3x', name:'Inserción', action: $scope.openLaboral},
      // {value:'issues', style: 'c8', img: 'fa fa-ticket fa-3x', name:'Pedidos', action: $scope.openIssues},
      {value:'digesto', style: 'c9', img: 'fa fa-file-text fa-3x', name:'Digesto', action: $scope.openDigesto},
      // {value:'task', style: 'c10', img: 'fa fa-list fa-3x', name:'Tareas', action: $scope.openTask},
      {value:'lists', style: 'c11', img: 'fa fa-at fa-3x', name:'Listas', action: $scope.openLists},
      {value:'adscription', style: 'c12', img: 'fa fa-adn fa-3x', name:'Adscriptos', action: $scope.openAdscription},
      {value:'sileg', style: 'c13', img: 'fa fa-gavel fa-3x', name:'Sileg', action: $scope.openSileg},
      {value:'tutors', style: 'c14', img: 'fa fa-tumblr fa-3x', name:'Tutorías', action: $scope.openTutors},
      // {value:'chat', style: 'c15', img: 'fa fa-comments fa-3x', name:'fceChat', action: $scope.openChat},
      {value:'ingreso', style: 'c16', img: 'fa fa-linkedin fa-3x', name:'Ingreso FCE', action: $scope.openIngreso}
    ]
  }

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.model.userId = '';
    Login.getSessionData()
      .then(function(s) {
          $scope.model.userId = s.user_id;
          $scope.initialize();
      }, function(err) {
        console.log(err);
      });
  });

  function initialize() {
    $scope.listSystems();
  }

  function listSystems() {
    $scope.model.systems = [];
    Systems.listSystems().then(
        function(systems) {
          if (systems == null) {
            return
          }
          var sys = [];
          for (var i = 0; i < systems.length; i++) {
            var s = systems[i];
            for (var j = 0; j < $scope.model.options.length; j++) {
              var op = $scope.model.options[j]
              if (s == op.value) {
                sys.push(op);
                continue;
              }
            }
          }
          $scope.$apply(function() {
            $scope.model.systems = sys;
          });
        },
        function(err) {
          console.log('error')
        }
    );
  }

  function openChat() {
    console.log("chat");
  }

  function openIngreso() {
    $window.open('http://www.ingreso.econo.unlp.edu.ar', '_blank');
  }

  function openWebmail () {
    $window.open('http://correo.econo.unlp.edu.ar', '_blank');
  }

  function openFceBox() {
      $window.open('http://owncloud.econo.unlp.edu.ar', '_blank');
  }

  function openAu24() {
    $window.open('http://www.au24.econo.unlp.edu.ar', '_blank');
  }

  function openAccount() {
    console.log("accounts");
  }

  function openAssistance() {
    $window.open('/systems/assistance', '_blank');
  }

  function openCamera() {
    console.log("camaras");
  }

  function openLaboral() {
      $window.open('/systems/laboralInsertion', '_blank');
  }

  function openIssues() {
    console.log("pedidos");
  }

  function openDigesto() {
    $window.open('http://digesto.econo.unlp.edu.ar', '_blank');
  }

  function openTask() {
    console.log("tareas");
  }

  function openLists() {
    $window.open('http://mailman.econo.unlp.edu.ar', '_blank');
  }

  function openAdscription() {
    $window.open('http://adscriptos.econo.unlp.edu.ar/', '_blank');
  }

  function openSileg() {
    $window.open('http://sileg.econo.unlp.edu.ar', '_blank');
  }

  function openTutors() {
      $window.open('/systems/tutorias', '_blank');
  }

}
