var app = angular.module('mainApp');

app.controller('MenuCtrl', ["$rootScope", '$scope', '$location', 'Login', 'Session', 'Notifications', 'Assistance','Office',

  function ($rootScope, $scope, $location, Login, Session, Notifications, Assistance, Office) {

    $scope.model = {
      class:'',
      items: []
    }

    $scope.toggleMenu = function() {
      $scope.$parent.model.hideMenu = !$scope.$parent.model.hideMenu;
    }

    $scope.summary = function() {
        $location.path('/summaryAssistance');
    };

    $scope.requestAssistance = function() {
        $location.path('/requestAssistance');
    };

    $scope.adminRequestAssistance = function() {
        $location.path('/adminRequestAssistance');
    };

    $scope.medicalLicenses = function() {
        $location.path('/medicalLicenses');
    };

    $scope.requestAuthority = function() {
        $location.path('/requestAuthority');
    };

    $scope.adminRequestOverTime = function() {
        $location.path('/adminRequestOverTime');
    };

    $scope.assistanceFails = function() {
      $location.path('/assistanceFails');
    };

    $scope.assistanceFailsFilters = function() {
      $location.path('/assistanceFailsFilters');
    };

    $scope.showAssistance = function() {
      $location.path('/showAssistance');
    };

    $scope.mySchedule = function() {
      $location.path('/mySchedule');
    };

    $scope.userAssistanceManagement = function() {
      $location.path('/userAssistanceManagement');
    };

    $scope.userAssistanceManagementMediator = function() {
      $location.path('/usersAssistanceManagementMediator');
    };

    $scope.requestGeneralJustifications = function() {
      $location.path('/requestGeneralJustifications');
    };

    $scope.manageJustificationsStock = function() {
      $location.path('/manageJustificationsStock');
    };

    $scope.managePositions = function() {
      $location.path('/managePositions');
    };

    $scope.exit = function() {
  	    $location.path('/logout');
  	}

    $scope.initialize = function() {

      var sid = Session.getSessionId();
      if (sid == null) {
        return;
      }

      Login.hasOneRole(['ADMIN-ASSISTANCE','USER-ASSISTANCE'],
        function(ok) {
          if (ok) {
              $scope.model.items = [];
              $scope.model.items.push({ n:1, label:'Inicio', img:'fa fa-home', function: $scope.summary});
              $scope.model.items.push({ n:20, label:'Solicitudes', img:'fa fa-ticket', function: $scope.requestAssistance});
              $scope.model.items.push({ n:10, label:'Control de Horario', img:'fa fa-clock-o', function: $scope.showAssistance});
              $scope.model.items.push({ n:1, label:'Incumplimientos', img:'fa fa-exclamation-triangle', function: $scope.assistanceFails});
              //$scope.model.items.push({ label:'Filtro de Fallas (testing todavía no terminado)', img:'fa-ticket', function: $scope.assistanceFailsFilters});
              // hasta que no este terminado en producción no va
              $scope.model.items.push({ n:4, label:'Mi Horario', img:'fa fa-clock-o', function: $scope.mySchedule});
              $scope.model.items.push({ n:100, label:'Salir', img:'fa fa-sign-out', function: $scope.exit });

              /*
              *** Comentado porque todavia no esta dicha funcionalidad 14/3/2016
              Office.getUserOfficeRoles(null,
                  function(roles) {
                    var hasApprove = false;
                    var hasOvertime = false;
                    var hasJustification = false;
                    var hasPositions = false;

                    for (var i = 0; i < roles.length; i++) {
                      hasApprove = hasApprove || (roles[i].role == 'autoriza');
                      hasOvertime = hasOvertime || (roles[i].role == 'horas-extras');
                      hasJustification = hasJustification || (roles[i].role == 'realizar-solicitud') || (roles[i].role == 'realizar-solicitud-admin');
                      hasPositions = hasPositions || roles[i].role == 'manage-positions';
                    }

                    if (hasApprove) {
                      $scope.model.items.push({ n:22, label:'Adm. Solicitudes ', img:'fa fa-tags', function: $scope.adminRequestAssistance});
                      $scope.model.items.push({ n:30, label:'Horas Extras ', img:'fa fa-clock-o', function: $scope.requestAuthority});
                      $scope.model.items.push({ n:21, label:'Solicitudes a Empleados', img:'fa fa-tags', function: $scope.userAssistanceManagementMediator});
                    }

                    if (hasOvertime) {
                      //$scope.model.items.push({ label:'Licencias Médicas', img:'fa-stethoscope', function: $scope.medicalLicenses});
                      $scope.model.items.push({ n:31, label:'Admin Horas Extras ', img:'fa fa-clock-o', function: $scope.adminRequestOverTime});
                    }

                    if (hasJustification) {
                      $scope.model.items.push({ n:23, label:'Solicitudes Especiales ', img:'fa fa-tags', function: $scope.userAssistanceManagement});
                      $scope.model.items.push({ n:24, label:'Solicitudes Generales ', img:'fa fa-tags', function: $scope.requestGeneralJustifications});
                      $scope.model.items.push({ n:25, label:'Stock de Solicitudes ', img:'fa fa-stack-overflow', function: $scope.manageJustificationsStock});
                    }

                    if (hasPositions) {
                      $scope.model.items.push({ n:40, label:'Administrar Cargos', img:'fa fa-cogs', function: $scope.managePositions});
                    }

                  },
                  function(err) {
                    Notifications.message(error);
                  }
              );*/
          } else {
            $scope.model.items.push({ n:100, label:'Salir', img:'fa fa-sign-out', function: $scope.exit });
          }

        },
        function (error) {
            Notifications.message(error);
        }
      );

    }


  	$scope.exit = function() {
  		$location.path('/logout');
  	}

    var compare = function(a,b) {
      return a.n - b.n;
    }

    $rootScope.$on('$viewContentLoaded', function(event) {
      $scope.initialize();
    });


  }
]);
