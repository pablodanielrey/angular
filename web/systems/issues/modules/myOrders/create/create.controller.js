(function() {
    'use strict';

    angular
        .module('issues')
        .controller('MyOrdersCreateCtrl', MyOrdersCreateCtrl);

    MyOrdersCreateCtrl.$inject = ['$scope', '$timeout', '$filter', '$location', 'Login', 'Issues', 'Users', 'Offices', 'Files'];

    /* @ngInject */
    function MyOrdersCreateCtrl($scope, $timeout, $filter, $location, Login, Issues, Users, Offices, Files) {
        var vm = this;

        vm.model = {
          issue: null, //datos del issue a crear
          description: '',
          files: [],
          selectedOffice: null,
          selectedArea: null,
          searchArea: {name:''},
          selectedFromOffice: null,
          searchOffice: {name: ''},
          subject: '',
          userOffices: [], //oficinas del usuario logueado (origen)
          privateTransport: null
        };

        vm.view = {
          style3: '',
          styles3: ['','pantallaMensajeAlUsuario'],
          style4: '',
          styles4: ['', 'mensajeError', 'mensajePedidoCreado'],
          status: ['','abierta', 'enProgreso', 'cerrada', 'comentarios', 'cerrada', 'rechazada', 'pausada'],
        };

        vm.selectOffice = selectOffice;
        vm.selectArea = selectArea;
        vm.selectSubject = selectSubject;
        vm.addFile = addFile;
        vm.removeFile = removeFile;
        vm.save = save;



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
          loadOffices();
          loadUserOffices(vm.model.userId);
        }

        //***** cargar oficinas (destino) *****
        function loadOffices() {
          vm.model.offices = [];
          Issues.getOffices().then(
            function(offices) {
              $scope.$apply(function() {
                vm.model.offices = offices;
              });
            },
            function(error) {
              messageError(error);
            }
          )
        }

        //***** cargar oficinas del usuario (origen) *****
        function loadUserOffices(userId) {
          Offices.getOfficesByUser(userId, false).then(
            function(ids) {
              if (!ids || ids.length <= 0) return;

              Offices.findById(ids).then(
                function(offices) {
                  $scope.$apply(function() {
                    vm.model.userOffices = (!offices || offices.length <= 0) ? [] : offices;
                    vm.model.selectedFromOffice = (offices.length > 0) ? offices[0] : null;
                  });
                }, function(error) {
                  messageError(error);
                }
              )
            }, function(error) {
              messageError(error);
            }
          );
        }


        function selectOffice(office) {
          vm.model.selectedArea = null;
          vm.model.searchArea = {name: ''};
          vm.model.subject = '';
          vm.model.selectedOffice = office;
          vm.model.searchOffice = (office == null) ? {name:''} : {name: office.name};
          vm.view.style2 = '';
          loadAreas(vm.model.selectedOffice);
          loadSubjects(vm.model.selectedOffice);
        }


        function selectArea(area) {
          clearSubject();
          vm.model.selectedArea = area;
          vm.model.searchArea = (area == null) ? {name:''} : {name: area.name};
          vm.view.style2 = '';
          vm.loadSubjects(vm.model.selectedArea);
        }

        function selectSubject(subject) {
          vm.model.subject = subject;
          vm.view.style2 = '';
        }

        function loadAreas(office) {
          vm.model.areas = [];
          Issues.getAreas(office.id).then(
            function(offices) {
              $scope.$apply(function() {
                vm.model.areas = offices;
              });
            },
            function(error) {
              messageError(error);
            }
          )
        }

        function loadSubjects(office) {
          Issues.getOfficeSubjects(office.id).then(function(subjects) {
            $scope.$apply(function() {
              vm.model.subjects = subjects;
            });
          });
        }


        function messageError(error) {
          vm.view.style3 = vm.view.styles3[1];
          vm.view.style4 = vm.view.styles4[1];
          $timeout(function() {
            closeMessage();
          }, 2000);
        }

        function messageCreated() {
          vm.view.style3 = vm.view.styles3[1];
          vm.view.style4 = vm.view.styles4[2];
        }

        function closeMessage() {
          vm.view.style3 = vm.view.styles3[0];
          vm.view.style4 = vm.view.styles4[0];
        }


        function addFile(fileName,fileContent, fileType, fileSize) {
          var file = {};
          file.name = fileName;
          file.content = window.btoa(fileContent);
          file.type = fileType;
          file.size = fileSize;
          file.codec = Files.BASE64;
          vm.model.files.push(file);
        }

        function removeFile(file) {
          var index = vm.model.files.indexOf(file);
          if (index >= 0) {
            vm.model.files.splice(index, 1);
          }
        }


        function save() {

          var office = (vm.model.selectedArea != null) ? vm.model.selectedArea : vm.model.selectedOffice;
          var subject = vm.model.subject;
          var description = vm.model.description;
          var parentId = null;
          var fromOfficeId = (vm.model.selectedFromOffice == null) ? null : vm.model.selectedFromOffice.id;

          if (office == null || vm.model.subjects.indexOf(subject) < 0) {
            messageError('Complete los campos correctamente');
            return;
          }

          // vm.messageLoading();
          Issues.create(subject, description, parentId, office.id, fromOfficeId, null, vm.model.files).then(
            function(data) {
              $scope.$apply(function() {
                messageCreated();
              });
              $timeout(function () {
                closeMessage();
                $location.path("myOrders");
              }, 2500);
            }, function(error) {
              messageError(error);
            }
          );
        }



    }
})();
