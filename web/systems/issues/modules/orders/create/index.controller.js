(function() {
    'use strict';

    angular
        .module('issues')
        .controller('OrdersCreateCtrl', OrdersCreateCtrl);

    OrdersCreateCtrl.$inject = ['$scope', '$location', 'Login', 'Issues', 'Files', 'Offices', '$timeout'];

    /* @ngInject */
    function OrdersCreateCtrl($scope, $location,  Login, Issues, Files, Offices, $timeout) {
        var vm = this;

        // variables del modelo
        vm.model = {
          user: {name: '-'},
          search: '',
          users: [],
          offices: [],
          areas: [],
          subjects: [],
          searchOffice: {name:''},
          selectedFromOffice: {name:'-'},
          officesUser: [],
          searchFromOffice: {name:""},
          selectedArea: null,
          searchArea: {name:''},
          subject: '',
          description: '',
          files: [],
          privateTransport: null
        }

        vm.aux = {
          searchTimer: null
        }


        // variables de la vista
        vm.view = {
          searching: false,
          style3: '',
          styles3: ['','pantallaMensajeAlUsuario'],
          style4: '',
          styles4: ['', 'mensajeCargando', 'mensajeError', 'mensajeEnviado', 'mensajePedidoCreado'],
          status: ['','abierta', 'enProgreso', 'cerrada', 'comentarios', 'cerrada', 'rechazada', 'pausada']
        }

        // métodos
        vm.cancel = cancel;
        vm.searchUsers = searchUsers;
        vm.getUserPhoto = getUserPhoto;
        vm.selectUser = selectUser;
        vm.loadUserOffices = loadUserOffices;
        vm.selectOffice = selectOffice;
        vm.selectFromOffice = selectFromOffice;
        vm.selectArea = selectArea;
        vm.loadOffices = loadOffices;
        vm.addFile = addFile;
        vm.removeFile = removeFile;
        vm.selectSubject = selectSubject;
        vm.save = save;
        vm.displaySearchOffice = displaySearchOffice;
        vm.displaySearchArea = displaySearchArea;

        $scope.$on('wamp.open', function(event, args) {
          vm.model.privateTransport = Login.getPrivateTransport();
          activate();
        });

        activate();


        function activate() {
          if (Login.getPrivateTransport() == null) {
            return;
          }
          vm.model.userId = Login.getCredentials()['userId'];
          vm.model.user = {name:'-'};
          vm.model.search = '';
          vm.model.users = [];
          vm.model.selectedFromOffice = {name: '-'};
          vm.model.searchOffice = {name:''};
          vm.model.officesUser = [];
          loadOffices();
          vm.model.description = '';

          vm.view.searching = false;
          vm.model.files = [];
        }

        //***** cargar oficinas (destino) *****
        function loadOffices() {
          vm.model.offices = [];
          Issues.getOffices().then(
            function(offices) {
              $timeout(function() {
                vm.model.offices = offices;
              });
            },
            function(error) {
              $timeout(function() {
                messageError(error);
              });
            }
          )
        }

        function cancel() {
          $location.path('/orders');
        }

        function getUserPhoto(user) {
          if (user == null || user.photo == null) {
            var img = user != null && "genre" in user && user.genre != null && (user.genre.toLowerCase() == 'femenino' || user.genre.toLowerCase() == 'mujer') ? "img/avatarWoman.jpg" : "img/avatarMan.jpg";
            return img;
          } else {
            return Files.toDataUri(user.photo);
          }
        }


        function searchUsers() {
          if (vm.view.searching) {
            return
          }
          if (vm.model.search.length < 1) {
            vm.view.searching = false;
            return;
          }

          if (vm.aux.searchTimer != null) {
            $timeout.cancel(vm.aux.searchTimer);
            vm.aux.searchTimer = null;
          }

          vm.aux.searchTimer = $timeout(function() {
            vm.aux.searchTimer = null;
            vm.view.searching = true;
            Issues.searchUsers(vm.model.search).then(
              function(users) {
                $timeout(function() {
                  vm.view.searching = false;
                  vm.model.users = users;
                });
              }, function(error) {
                $timeout(function() {
                  messageError(error);
                });
              }
            );
          }, 1000);
        }

        function selectUser(user) {
          vm.view.style2 = '';
          vm.model.user = user;
          vm.loadUserOffices(user.id);
        }

        //***** cargar oficinas del usuario (origen) *****
        function loadUserOffices(userId) {
          vm.model.searchFromOffice = {name:""};
          vm.model.userOffices = [];
          vm.model.selectedFromOffice = null;

          Offices.runAndConcat([
            Offices.findByUser(userId, false),
            Offices.findByUserAndTypes(userId, ['area'], true)])
            .then(Offices.findById).then(
              function(offices) {
                $timeout(function() {
                  vm.model.userOffices = offices;
                  vm.model.selectedFromOffice = (offices.length > 0) ? offices[0] : null;
                });
              }, function(error) {
                $timeout(function() {
                  messageError(error);
                });
              });
        }

        function selectFromOffice(office) {
          vm.model.selectedFromOffice = office;
          vm.view.style2 = '';
        }

        function selectSubject(subject) {
          vm.model.subject = subject;
          vm.view.style2 = '';
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
          vm.model.selectedArea = area;
          vm.model.searchArea = (area == null) ? {name:''} : {name: area.name};
          vm.view.style2 = '';
          vm.model.subject = "";
          loadSubjects(vm.model.selectedArea);
        }

        function displaySearchOffice() {
          vm.view.style2 = (vm.view.style2 == 'buscarOficina') ? '' : 'buscarOficina';
          vm.model.searchOffice = '';
        }

        function displaySearchArea() {
          vm.view.style2 = (vm.view.style2 == 'buscarArea') ? '' : 'buscarArea';
          vm.model.searchArea = '';
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
            vm.model.subjects = subjects;
          });
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
          var subject = vm.model.subject;
          var description = vm.model.description;
          var parentId = null;
          var office = (vm.model.selectedArea != null) ? vm.model.selectedArea : vm.model.selectedOffice
          var author = vm.model.user;
          var fromOfficeId = (vm.model.selectedFromOffice == null || vm.model.selectedFromOffice.id == undefined) ? null : vm.model.selectedFromOffice.id;

          if ((subject == null || subject == '') || (office == null || office.id == undefined) || (author == null || author.id == undefined)) {
            window.alert("Debe completar los campos");
          }
          messageLoading();
          Issues.create(subject, description, parentId, office.id, fromOfficeId, author.id, vm.model.files).then(
            function(data) {
              $scope.$apply(function() {
                messageCreated();
              });
              $timeout(function () {
                closeMessage();
                $location.path("orders");
              }, 2500);
            }, function(error) {
              messageError(error);
            }
          );
        }

    /* ************************************************************************ */
    /* ************************** MENSAJES ************************************ */
    /* ************************************************************************ */
      function messageError(error) {
        vm.view.style3 = vm.view.styles3[1];
        vm.view.style4 = vm.view.styles4[2];
        $timeout(function() {
          closeMessage();
        }, 3000);
      }

      function closeMessage() {
        vm.view.style3 = vm.view.styles3[0];
        vm.view.style4 = vm.view.styles4[0];
      }

      function messageLoading() {
        vm.view.style3 = vm.view.styles3[1];
        vm.view.style4 = vm.view.styles4[1];
      }

      function messageSending() {
        vm.view.style3 = vm.view.styles3[1];
        vm.view.style4 = vm.view.styles4[3];
      }

      function messageCreated() {
        vm.view.style3 = vm.view.styles3[1];
        vm.view.style4 = vm.view.styles4[4];
      }

  }

})();
