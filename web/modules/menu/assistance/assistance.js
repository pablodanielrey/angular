var app = angular.module('mainApp');

app.controller('AssistanceOptionCtrl', function($scope, $rootScope, Profiles, Assistance, $location, Session) {

        $scope.visible = false;

        $scope.isVisible = function() {
            return $scope.visible;
        }

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
        }

        $scope.requestAssistance = function() {
            $location.path('/requestAssistance')
        }

        $scope.adminRequestAssistance = function() {
            $location.path('/adminRequestAssistance')
        }

        $scope.medicalLicenses = function() {
            $location.path('/medicalLicenses')
        }

        $scope.requestAuthority = function() {
            $location.path('/requestAuthority')
        }
        $scope.adminRequestOverTime = function() {
            $location.path('/adminRequestOverTime')
        }

        $scope.assistanceFails = function() {
          $location.path('/assistanceFails')
        }



        $scope.items = [];

        $scope.generateItems = function() {
            Profiles.checkAccess(Session.getSessionId(),'ADMIN-ASSISTANCE,USER-ASSISTANCE', function(ok) {
                if (ok == 'granted') {
                    $scope.items = [];
                    $scope.items.push({ label:'Inicio', img:'fa-tachometer', function: $scope.summary});
                    $scope.items.push({ label:'Solicitudes', img:'fa-ticket', function: $scope.requestAssistance});

                    Assistance.getUserOfficeRoles(
                      function(roles) {
                        if (roles.length > 0) {
                          //$scope.items.push({ label:'Licencias Médicas', img:'fa-stethoscope', function: $scope.medicalLicenses});
                          $scope.items.push({ label:'Adm. Solicitudes ', img:'fa-ticket', function: $scope.adminRequestAssistance});
                          $scope.items.push({ label:'Horas Extras ', img:'fa-plus', function: $scope.requestAuthority});
                          $scope.items.push({ label:'Admin Horas Extras ', img:'fa-plus', function: $scope.adminRequestOverTime});
                        }
                      },
                      function(err) {
                        alert(error);
                    })

                    $scope.selectItem($scope.items[0]);
                }
            },
            function (error) {
                alert(error);
            });
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
