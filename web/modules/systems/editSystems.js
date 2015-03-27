var app = angular.module('mainApp');

app.controller('EditSystemsCtrl', function($scope, $timeout, Domain, Mail, Session) {




    $scope.systems = [];

    $scope.loadSystemsData = function() {
        $scope.systems = [];

        var s = Session.getCurrentSession();
        if (s == null) {
            return;
        }

        if (s.selectedUser == undefined || s.selectedUser == null) {
            return;
        }

        var user_id = s.selectedUser;

        Domain.findDomainData(user_id,
            function(domain) {
                var value = false;
                if (domain != null) {
                    value = true;
                }
                $scope.systems.push({name:'dominio',img:'fa fa-laptop',value:value,label:"Dominio"});
            },
            function(error) {
                $scope.systems.push({name:'dominio',img:'fa fa-laptop',value:false,label:"Dominio"});
            }
        );

        Mail.findMailData(user_id,
            function(mail) {
                var value = false;
                if (mail != null) {
                    value = true;
                }

                $scope.systems.push({name:'correo',img:'fa fa-envelope-o', value:value,label:"Correo"});
            },
            function(error) {
                $scope.systems.push({name:'correo',img:'fa fa-envelope-o', value:false,label:"Correo"});
            }
        );
    }


    $scope.save = function() {

        var s = Session.getCurrentSession();
        if (s == null) {
            return;
        }

        if (s.selectedUser == undefined || s.selectedUser == null) {
            return;
        }

        for (var $i=0; $i<$scope.systems.length; $i++) {
            var $item = $scope.systems[$i];

            if ($item.name == 'dominio') {
                var $user = {id:s.selectedUser};
                if ($item.value) {
                    Domain.updateData($user,
                        function(domain) {

                        },
                        function(error) {
                            alert(error);
                        }
                    );
                } else {
                    Domain.deleteDomainData($user.id,
                        function(domain) {

                        },
                        function(error) {
                            alert(error)
                        }
                    );
                }
                continue;
            }

            if ($item.name == 'correo') {
                var $user = {id:s.selectedUser};
                if ($item.value) {
                    Mail.updateData($user,
                        function(mail) {

                        },
                        function(error) {
                            alert(error);
                        }
                    );
                } else {
                    Mail.daleteMailData($user.id,
                        function(mail) {

                        },
                        function(error) {
                            alert(error)
                        }
                    );
                }
                continue;
            }
        }
  }

  $timeout(function() {
    $scope.loadSystemsData();
  },0);

});
