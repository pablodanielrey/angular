var app = angular.module('mainApp');

app.controller('AssistanceOptionCtrl', function($scope, $rootScope, Profiles, Assistance, $location, Session, Notifications) {

        $scope.visible = false;

        $scope.isVisible = function() {
            return $scope.visible;
        };

        $scope.$on('MenuOptionSelectedEvent', function(event,data) {
                $scope.visible = false;
                if (data == 'AssistanceOption') {
                    $scope.visible = true;
                    $scope.itemSelected = null;

                    $scope.generateItems();
                }
        });

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


        $scope.items = [];

        $scope.generateItems = function() {


          Profiles.checkAccess(Session.getSessionId(),["ADMIN-ASSISTANCE","USER-ASSISTANCE"],
            function(ok) {
              if (ok) {
                  $scope.items = [];
                  $scope.items.push({ label:'Inicio', img:'fa-tachometer', function: $scope.summary});
                  $scope.items.push({ label:'Solicitudes', img:'fa-ticket', function: $scope.requestAssistance});
                  $scope.items.push({ label:'Control de Horario', img:'fa-clock-o', function: $scope.showAssistance});
                  $scope.items.push({ label:'Incumplimientos', img:'fa-ticket', function: $scope.assistanceFails});
                  //$scope.items.push({ label:'Filtro de Fallas (testing todavía no terminado)', img:'fa-ticket', function: $scope.assistanceFailsFilters});
                  // hasta que no este terminado en producción no va
                  $scope.items.push({ label:'Mi Horario', img:'fa-clock-o', function: $scope.mySchedule});

                  Assistance.getUserOfficeRoles(
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
                          $scope.items.push({ label:'Adm. Solicitudes ', img:'fa-ticket', function: $scope.adminRequestAssistance});
                          $scope.items.push({ label:'Horas Extras ', img:'fa-plus', function: $scope.requestAuthority});
                          $scope.items.push({ label:'Solicitudes a Empleados', img:'fa-plus', function: $scope.userAssistanceManagementMediator});
                        }

                        if (hasOvertime) {
                          //$scope.items.push({ label:'Licencias Médicas', img:'fa-stethoscope', function: $scope.medicalLicenses});
                          $scope.items.push({ label:'Admin Horas Extras ', img:'fa-plus', function: $scope.adminRequestOverTime});
                        }

                        if (hasJustification) {
                          $scope.items.push({ label:'Solicitudes Especiales ', img:'fa-plus', function: $scope.userAssistanceManagement});
                          $scope.items.push({ label:'Solicitudes Generales ', img:'fa-plus', function: $scope.requestGeneralJustifications});
                          $scope.items.push({ label:'Stock de Solicitudes ', img:'fa-plus', function: $scope.manageJustificationsStock});
                        }

                        if (hasPositions) {
                          $scope.items.push({ label:'Administrar Cargos', img:'fa-plus', function: $scope.managePositions});
                        }

                      },
                      function(err) {
                        Notifications.message(error);
                      }
                  );

                  $scope.selectItem($scope.items[0]);
              }
            },
            function (error) {
                Notifications.message(error);
            }
          );

        }

        $scope.itemSelected = null;

        $scope.selectItem = function(i) {
            $scope.itemSelected = i;
            i.function();
        }

        $scope.isItemSelected = function(i) {
            return ($scope.itemSelecter == i);
        }
});
