(function() {
    'use strict';

    angular
        .module('issues')
        .controller('MyOrdersCtrl', MyOrdersCtrl);

    MyOrdersCtrl.$inject = ['$scope', '$timeout', '$filter', 'Login', 'Issues', 'Users', 'Offices', 'Files'];

    /* @ngInject */
    function MyOrdersCtrl($scope, $timeout, $filter, Login, Issues, Users, Offices, Files) {
        var vm = this;

        vm.model = {
          userId: '',
          users: [],
          issues: [],
          issue: null,
          replyDescription: '',
          description: '',
          subject: '',
          selectedOffice: null,
          searchOffice: {name:''},
          offices: [],
          office: null,
          files: [],
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
          styles2: ['', 'buscarOficina', 'buscarArea', 'buscarConsulta', 'verMisOficinas', 'pantallaMensaje'],
          style3: '',
          styles3: ['','pantallaMensajeAlUsuario'],
          style4: '',
          styles4: ['', 'mensajeCargando', 'mensajeError', 'mensajeEnviado', 'mensajePedidoCreado'],
          status: ['','abierta', 'enProgreso', 'cerrada', 'comentarios', 'cerrada', 'rechazada', 'pausada'],
          statusSort: ['','abierta', 'enProgreso', 'pausada', 'rechazada', 'cerrada'],
          reverseSortDate: false,
          reverseSortStatus: false
        }

        // métodos
        vm.create = create;
        vm.save = save;
        vm.cancel = cancel;
        vm.addFile = addFile;
        vm.removeFile = removeFile;
        vm.reply = reply;
        vm.cancelComment = cancelComment;
        vm.createComment = createComment;

        vm.sortDate = sortDate;
        vm.sortStatus = sortStatus;

        vm.closeMessage = closeMessage;
        vm.messageLoading = messageLoading;
        vm.messageError = messageError;
        vm.messageSending = messageSending;
        vm.messageCreated = messageCreated;

        vm.initializeModel = initializeModel;
        vm.initializeView = initializeView;
        vm.getMyIssues = getMyIssues;
        vm.loadOffices = loadOffices;
        vm.loadOffice = loadOffice;
        vm.loadUserOffices = loadUserOffices;
        vm.loadAreas = loadAreas;
        vm.loadSubjects = loadSubjects;
        vm.loadIssue = loadIssue;

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
        vm.getCreator = getCreator;
        vm.registerEventManagers = registerEventManagers;

        activate();

        function activate() {
          vm.model.userId = Login.getCredentials().userId;
          vm.initializeModel();
          vm.initializeView();
          vm.registerEventManagers();
        }

        function initializeView() {
          vm.view.reverseSortDate = false;
          vm.view.reverseSortStatus = false;
        }

        function initializeModel() {
          vm.model.issues = [];
          vm.model.users = [];
          vm.model.files = [];
          vm.getMyIssues();
          vm.loadOffices();
          vm.loadUserOffices(vm.model.userId);
        }


        /* ************************************************************************* */
        /* ***************************** ORDENACION ******************************** */
        /* ************************************************************************* */

        function sortDate() {
          vm.view.reverseSortStatus = false;
          vm.model.issues = $filter('orderBy')(vm.model.issues, ['start', 'statusPosition'], vm.view.reverseSortDate);
          vm.view.reverseSortDate = !vm.view.reverseSortDate;
        }

        function sortStatus() {
          vm.view.reverseSortDate = false;
          vm.model.issues = $filter('orderBy')(vm.model.issues, ['statusPosition', 'start'], vm.view.reverseSortStatus);
          vm.view.reverseSortStatus = !vm.view.reverseSortStatus;
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
          vm.model.files = [];

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
            window.alert('Complete los campos correctamente');
            return;
          }

          // vm.messageLoading();
          Issues.create(subject, description, parentId, office.id, fromOfficeId, null, vm.model.files).then(
            function(data) {
              vm.messageCreated();
              $timeout(function () {
                vm.closeMessage();
                vm.view.style = vm.view.styles[0];
              }, 2500);
            }, function(error) {
              vm.messageError(error);
            }
          );
        }

        function cancel() {
          vm.model.issue = {};
          vm.view.style = vm.view.styles[0];
        }

        function reply() {
          vm.model.replyDescription = '';
          vm.model.files = [];
          vm.view.style2 = vm.view.styles2[5];
        }

        function cancelComment() {
          vm.view.style2 = vm.view.styles2[0];
          vm.model.replyDescription = '';
          vm.model.files = [];
          vm.loadIssue(vm.model.issueSelected.id);
        }

        function createComment() {
          var subject = vm.model.issueSelected.subject;
          var parentId = vm.model.issueSelected.id;
          var officeId = vm.model.issueSelected.projectId;

          vm.messageLoading();
          Issues.createComment(subject, vm.model.replyDescription, parentId, officeId, vm.model.files).then(
            function(data) {

            }, function(error) {
              vm.messageError(error);
            }
          );
        }

        // TODO: manejador de eventos
        function registerEventManagers() {
          Issues.subscribe('issues.comment_created_event', function(params) {
            var parentId = params[0];
            var commentId = params[1];
            if (vm.model.issueSelected.id == parentId) {
              Issues.findById(commentId).then(
                function(comment) {
                    vm.messageSending();
                    $timeout(function () {
                      vm.view.style2 = vm.view.styles2[0];
                      vm.closeMessage();
                    }, 2500);

                    vm.model.issueSelected.children.push(comment);
                },
                function(error) {
                    vm.messageError(error);
                });
            }
          });

          Issues.subscribe('issues.issue_created_event', function(params) {
            var issueId = params[0];
            var authorId = params[1];
            var fromOfficeId = params[2];
            var officeId = params[3];
            if (authorId == vm.model.userId || vm.model.userOffices.indexOf(officeId) > -1) {
                Issues.findById(issueId).then(
                  function(issue) {
                    if (issue != null) {
                      vm.model.issues.push(issue);
                    }
                  },
                  function(error) {

                  }
                )
            }
          });

        }

        /* ************************************************************************* */
        /* ************************ FORMATEO DE DATOS ****************************** */
        /* ************************************************************************* */
        function loadUser(userId) {
          if (userId == null || userId == '') {
            return
          }
          if (vm.model.users[userId] == null) {
            Users.findById([userId]).then(
              function(users) {
                vm.model.users[userId] = users[0];
                var user = vm.model.users[userId];
                if (user.photoSrc == undefined || user.photoSrc == null) {
                  Users.findPhoto(users[0].photo).then(function(photo) {
                    vm.model.users[userId].photoSrc = Files.toDataUri(photo);
                  });
                }
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

        function setInitDay(date) {
          date.setHours(0);
          date.setMinutes(0);
          date.setSeconds(0);
          date.setMilliseconds(0);
        }

        function getDiffDay(issue) {
          if (issue == null) {
            return '';
          }
          var date = ('date' in issue) ? new Date(issue.date) : new Date(issue.start);
          var now = new Date();
          setInitDay(date);
          setInitDay(now);
          var diff = now - date;
          var days = Math.floor(diff / (1000 * 60 * 60 * 24));
          return (days == 0) ? 'Hoy' : (days == 1) ? 'Ayer' : 'Hace ' + days + ' días'
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
          if (issue == null || issue.userId == null || issue.fromOfficeId == undefined) {
            vm.model.office = null;
            return;
          }
          Offices.findById([issue.fromOfficeId]).then(
            function(offices) {
              vm.model.office = (offices == null || offices.length <= 0) ? null : offices[0];
            }, function(error) {
              vm.messageError(error);
            }
          )
        }

        function loadUserOffices(userId) {
          vm.model.selectedFromOffice = null;
          vm.model.userOffices = [];
          Offices.getOfficesByUser(userId, false).then(
            function(ids) {
              if (ids == null || ids.length <= 0) {
                return;
              }
              Offices.findById(ids).then(
                function(offices) {
                  vm.model.userOffices = (offices == null || offices.length <= 0) ? [] : offices;
                  vm.model.selectedFromOffice = (offices.length > 0) ? offices[0] : null;
                }, function(error) {
                  vm.messageError(error);
                }
              )
            }, function(error) {
              vm.messageError(error);
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

        function getCreator(issue) {
          if (issue.creatorId == null || issue.creatorId == '') {
            return '';
          }

          var user = vm.model.users[issue.creatorId];
          return user.name + ' ' + user.lastname ;
        }

        function getUserPhoto(issue) {
          var user = (issue == null) ? null : vm.model.users[issue.userId];
          if (user == null || user.photo == null || user.photoSrc == '') {
            return "../login/modules/img/imgUser.jpg";
          } else {
            return user.photoSrc;
          }
        }

        function loadIssue(id) {
          Issue.findById(id).then(
            function(issue) {
              vm.viewDetail(issue);
            }, function(error) {
              vm.messageError(error);
            }
          );
        }


        /* ************************************************************************* */
        /* ************************ BUSQUEDA DE DATOS ****************************** */
        /* ************************************************************************* */

        function getMyIssues() {
          vm.messageLoading();
          Issues.getMyIssues().then(
            function(issues) {
                for (var i = 0; i < issues.length; i++) {
                  var dateStr = issues[i].start;
                  issues[i].date = new Date(dateStr);

                  // obtengo la posicion de ordenacion del estado
                  var item = vm.view.status[issues[i].statusId];
                  issues[i].statusPosition = vm.view.statusSort.indexOf(item);

                  loadUser(issues[i].userId);
                  loadUser(issues[i].creatorId);
                }
                vm.model.issues = issues;
                vm.sortStatus();
                vm.closeMessage();
            },
            function(err) {
              vm.messageError(error);
            }
          );
        }

        function messageError(error) {
          vm.view.style3 = vm.view.styles3[1];
          vm.view.style4 = vm.view.styles4[2];
          $timeout(function() {
            vm.closeMessage();
          }, 2000);
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

        function loadOffices() {
          vm.model.offices = [];
          Issues.getOffices().then(
            function(offices) {
              vm.model.offices = offices;
            },
            function(error) {
              vm.messageError(error);
            }
          )
        }


      function loadAreas(office) {
        vm.model.areas = [];
        Issues.getAreas(office.id).then(
          function(offices) {
            vm.model.areas = offices;
          },
          function(error) {
            vm.messageError(error);
          }
        )
      }

      function loadSubjects(office) {
        Issues.getOfficeSubjects(office.id).then(function(subjects) {
          vm.model.subjects = subjects;
        });
      }

    }
})();
