(function() {
    'use strict';

    angular
        .module('mainApp')
        .controller('MyOrdersCtrl', MyOrdersCtrl);

    MyOrdersCtrl.$inject = ['$scope', 'Login', 'Issue', 'Users', 'Office'];

    /* @ngInject */
    function MyOrdersCtrl($scope, Login, Issue, Users, Office) {
        var vm = this;

        vm.model = {
          userId: '',
          users: [],
          issues: [],
          issue: null,
          description: '',
          subject: '',
          selectedOffice: null,
          searchOffice: {name:''},
          offices: [],
          office: null,
          userOffices: [],
          selectedFromOffice: null,
          searchArea: {name:''},
          selectedArea: null,
          areas: [],
          loaded: 0,
          issueSelected: null
        }

        vm.view = {
          style: '',
          styles : ['', 'pantallaNuevoPedido','pantallaDetallePedido', 'pantallaMensaje', 'buscarPedidos'],
          style2: '',
          styles2: ['', 'buscarOficina', 'buscarArea', 'buscarConsulta', 'verMisOficinas'],
          style3: '',
          styles3: ['','pantallaMensajeAlUsuario'],
          style4: '',
          styles4: ['', 'mensajeCargando', 'mensajeError', 'mensajeEnviado', 'mensajePedidoCreado'],
          status: ['','abierta', 'enProgreso', 'pausada', 'rechazada', 'cerrada']
        }


        // métodos
        vm.create = create;
        vm.save = save;
        vm.cancel = cancel;
        vm.addFile = addFile;

        vm.sortDate = sortDate;
        vm.sortStatus = sortStatus;

        vm.initializeModel = initializeModel;
        vm.getMyIssues = getMyIssues;
        vm.loadOffices = loadOffices;
        vm.loadOffice = loadOffice;
        vm.loadUserOffices = loadUserOffices;
        vm.loadAreas = loadAreas;
        vm.loadSubjects = loadSubjects;

        vm.selectOffice = selectOffice;
        vm.selectArea = selectArea;
        vm.selectSubject = selectSubject;
        vm.selectFromOffice = selectFromOffice;

        vm.getDate = getDate;
        vm.getDiffDay = getDiffDay;
        vm.getStatus = getStatus;
        vm.getFullName = getFullName;
        vm.viewDetail = viewDetail;
        vm.getOffice = getOffice;
        vm.getUserOffices = getUserOffices;
        vm.getName = getName;
        vm.getLastname = getLastname;
        vm.getUserPhoto = getUserPhoto;

        activate();

        function activate() {
          vm.model.userId = '';
          Login.getSessionData()
            .then(function(s) {
                vm.model.userId = s.user_id;
                vm.initializeModel();
            }, function(err) {
              console.log(err);
            });
        }

        function initializeModel() {
          vm.model.issues = [];
          vm.model.users = [];
          vm.getMyIssues();
          vm.loadOffices();
          vm.loadUserOffices(vm.model.userId);
        }


        /* ************************************************************************* */
        /* ***************************** ORDENACION ******************************** */
        /* ************************************************************************* */

        function sortDate() {

        }

        function sortStatus() {

        }

        /* ************************************************************************* */
        /* ***************************** CLEARS ************************************ */
        /* ************************************************************************* */

        function clearOffice() {
          vm.model.selectedOffice = null;
          vm.model.searchOffice = {name: ''};
          clearArea();
        }

        function clearArea() {
          vm.model.selectedArea = null;
          vm.model.searchArea = {name: ''};
          clearSubject();
        }

        function clearSubject() {
          vm.model.subject = '';
        }

        /* ************************************************************************* */
        /* ***************************** SELECCION ********************************* */
        /* ************************************************************************* */

        function selectOffice(office) {
          clearArea();
          vm.model.selectedOffice = office;
          vm.model.searchOffice = (office == null) ? {name:''} : {name: office.name};
          vm.view.style2 = '';
          vm.loadAreas(vm.model.selectedOffice);
          vm.loadSubjects(vm.model.selectedOffice);
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

        function selectFromOffice(office) {
          vm.view.style2 = '';
          vm.model.selectedFromOffice = office;
        }

        /* ************************************************************************* */
        /* ***************************** CREACION ********************************** */
        /* ************************************************************************* */

        function create() {
          vm.model.issue = {};
          vm.view.style = vm.view.styles[1];
          clearOffice();
          vm.model.description = '';
        }

        function addFile(fileName,fileContent, fileType) {
          console.log(fileName);
          console.log(fileType);
        }

        function save() {
          var office = (vm.model.selectedArea != null) ? vm.model.selectedArea : vm.model.selectedOffice;
          var subject = vm.model.subject;
          var description = vm.model.description;
          var parentId = null;
          var fromOfficeId = (vm.model.selectedFromOffice == null) ? null : vm.model.selectedFromOffice.id;
          var authorId = vm.model.authorId;


          if (office == null || vm.model.subjects.indexOf(subject) < 0) {
            window.alert('Complete los campos correctamente');
            return;
          }

          Issue.create(subject, description, parentId, office.id, fromOfficeId, authorId).then(
            function(data) {
              $scope.$apply(function() {
                vm.view.style = vm.view.styles[0];
                vm.getMyIssues();
              })
            }, function(error) {
              console.log(error);
            }
          );

        }


        function cancel() {
          vm.model.issue = {};
          vm.view.style = vm.view.styles[0];
        }

        /* ************************************************************************* */
        /* ************************ FORMATEO DE DATOS ****************************** */
        /* ************************************************************************* */
        function loadUser(userId) {
          if (vm.model.users[userId] == null) {
            Users.findById([userId]).then(
              function(users) {
                vm.model.users[userId] = users[0];
              }
            );
          }
        }

        function getDate(issue) {
          if (issue == null) {
            return '';
          }
          var date = ('date' in issue) ? issue.date : new Date(issue.start);
          return date;
        }

        function getDiffDay(issue) {
          if (issue == null) {
            return '';
          }
          var date = ('date' in issue) ? issue.date : new Date(issue.start);
          var now = new Date();
          var diff = now - date;
          var days = Math.floor(diff / (1000 * 60 * 60 * 24));
          return (days == 0) ? 'Hoy' : (days == 1) ? 'Ayer' : days + ' días'
        }

        function getStatus(issue) {
          if (issue == null) {
            return '';
          }
          return vm.view.status[issue.statusId];
        }

        function getFullName(issue) {
          if (issue == null) {
            return;
          }
          var user = vm.model.users[issue.userId];
          return (user == null) ? 'No tiene nombre' : user.name + ' ' + user.lastname;
        }

        function viewDetail(issue) {
          vm.model.loaded = (issue.children == undefined) ? 0 : issue.children.length;
          for (var i = 0; i < issue.children.length; i++) {
              var child = issue.children[i];
              if (child.user == undefined) {
                loadUser(child.userId);
              }
          }

          vm.model.issueSelected = issue;
          loadOffice(issue);
          vm.view.style = vm.view.styles[2];
        }

        function loadOffice(issue) {
          if (issue == null || issue.userId == null) {
            vm.model.office = null;
          }
          Office.getOfficesByUser(issue.userId, false).then(
            function(ids) {
              if (ids == null || ids.length <= 0) {
                return;
              }
              Office.findById(ids).then(
                function(offices){
                  vm.model.office = (offices == null || offices.length <= 0) ? null : offices[0];
                }, function(error) {
                  console.log(error);
                }
              )
            }, function(error) {
              console.log(error);
            }
          );
        }

        function loadUserOffices(userId) {
          vm.model.selectedFromOffice = null;
          vm.model.userOffices = [];
          Office.getOfficesByUser(userId, false).then(
            function(ids) {
              if (ids == null || ids.length <= 0) {
                return;
              }
              Office.findById(ids).then(
                function(offices) {
                  console.log(offices);
                  vm.model.userOffices = (offices == null || offices.length <= 0) ? [] : offices;
                  vm.model.selectedFromOffice = (offices.length > 0) ? offices[0] : null;
                }, function(error) {
                  console.log(error);
                }
              )
            }, function(error) {
              console.log(error);
            }
          );
        }

        function getUserOffices() {
          return vm.model.userOffices;
        }

        function getOffice() {
          return (vm.model.office == null) ? 'No posee' : vm.model.office.name;
        }

        function getName(issue) {
          if (issue == null) {
            return;
          }
          var user = vm.model.users[issue.userId];
          return (user == null) ? '' : user.name;
        }

        function getLastname(issue) {
          if (issue == null) {
            return;
          }
          var user = vm.model.users[issue.userId];
          return (user == null) ? '' : user.lastname;
        }

        function getUserPhoto(issue) {
          var user = (issue == null) ? null : vm.model.users[issue.userId];
          if (user == null || user.photo == null || user.photo == '') {
            return "../login/modules/img/imgUser.jpg";
          } else {
            return "/c/files.py?i=" + user.photo;
          }
        }


        /* ************************************************************************* */
        /* ************************ BUSQUEDA DE DATOS ****************************** */
        /* ************************************************************************* */

        function getMyIssues() {
          Issue.getMyIssues().then(
            function(issues) {
              $scope.$apply(function() {
                for (var i = 0; i < issues.length; i++) {
                  var dateStr = issues[i].start;
                  issues[i].date = new Date(dateStr);
                  loadUser(issues[i].userId);
                }
                vm.model.issues = issues;
                console.log(issues);
              });

            },
            function(err) {
              console.log('error')
            }
          );
        }

        function loadOffices() {
          vm.model.offices = [];
          Issue.getOffices().then(
            function(offices) {
              vm.model.offices = offices;
            },
            function(error) {
              console.log(error);
            }
          )
        }


      function loadAreas(office) {
        vm.model.areas = [];
        Issue.getAreas(office).then(
          function(offices) {
            vm.model.areas = offices;
          },
          function(error) {
            console.log(error);
          }
        )
      }

      function loadSubjects(office) {
        vm.model.subjects = ['Otro', 'Wifi'];
      }


    }
})();
