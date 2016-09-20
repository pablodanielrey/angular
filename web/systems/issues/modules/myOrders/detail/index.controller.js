(function() {
    'use strict';

    angular
        .module('issues')
        .controller('MyOrdersDetailCtrl', MyOrdersDetailCtrl);

    MyOrdersDetailCtrl.$inject = ['$scope', '$routeParams', '$location', '$timeout', 'Issues', 'Users', 'Files', 'Offices', 'Login'];

    /* @ngInject */
    function MyOrdersDetailCtrl($scope, $routeParams, $location, $timeout, Issues, Users, Files, Offices, Login) {
        var vm = this;
        vm.model = {
          issue: null,
          users: [],
          privateTransport: null
        }

        vm.view = {
          status: ['','abierta', 'enProgreso', 'cerrada', 'comentarios', 'cerrada', 'rechazada', 'pausada'],
          style3: '',
          styles3: ['','pantallaMensajeAlUsuario'],
          style4: '',
          styles4: ['', 'mensajeCargando', 'mensajeError', 'mensajeEnviado']
        }


        vm.loadIssue = loadIssue;
        vm.getName = getName;
        vm.getLastname = getLastname;
        vm.getStatus = getStatus;
        vm.getUserPhoto = getUserPhoto;
        vm.getDiffDay = getDiffDay;
        vm.getDate = getDate;
        vm.reply = reply;

        vm.closeMessage = closeMessage;
        vm.messageLoading = messageLoading;
        vm.messageError = messageError;
        vm.messageSending = messageSending;

        $scope.$on('openPrivateConnection', function(event, args) {
          vm.model.privateTransport = Login.getPrivateTransport();
          activate();
        });

        activate();


        function activate() {
          if (Login.getPrivateTransport().getConnection() == null) {
            return;
          }
          var params = $routeParams;
          if (params.issueId == undefined) {
            $location.path('/myOrders');
          }
          vm.model.users = [];
          vm.loadIssue(params.issueId);
          registerEventManagers();
          messageLoading();
        }

        function loadIssue(id) {
          Issues.findById(id).then(
            function(issue) {
              loadUser(issue.userId);
              loadUser(issue.creatorId);
              var size = (issue.children == undefined) ? 0 : issue.children.length;
              for (var i = 0; i < size; i++) {
                  var child = issue.children[i];
                  if (child.user == undefined) {
                    loadUser(child.userId);
                  }
              }
              if (issue.fromOfficeId != undefined) {
                loadOffice(issue.fromOfficeId);
              }
              $scope.$apply(function() {
                vm.model.issue = issue;
                closeMessage();
              });
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
            if (vm.model.issue.id == parentId) {
              Issues.findById(commentId).then(
                function(comment) {
                  $scope.$apply(function() {
                    vm.model.issue.children.push(comment);
                    if (comment.user == undefined) {
                      loadUser(comment.userId);
                    }
                  });
                },
                function(error) {
                    vm.messageError(error);
                });
            }
          });
        }

        function loadUser(userId) {
          if (userId == null || userId == '') {
            return
          }
          if (vm.model.users[userId] == null) {
            Users.findById([userId]).then(
              function(users) {
                $scope.$apply(function() {
                  vm.model.users[userId] = users[0];
                  var user = vm.model.users[userId];
                  if (user.photoSrc == undefined || user.photoSrc == null) {
                    Users.findPhoto(users[0].photo).then(function(photo) {
                      $scope.$apply(function() {
                        vm.model.users[userId].photoSrc = Files.toDataUri(photo);
                      });
                    });
                  }
                });
              }
            );
          }
        }

        function loadOffice(officeId) {
          if (officeId == undefined || officeId == null) {
            vm.model.office = null;
            return;
          }
          Offices.findById([officeId]).then(
            function(offices) {
              $scope.$apply(function() {
                vm.model.office = (offices == null || offices.length <= 0) ? null : offices[0];
              });
            }, function(error) {
              // vm.messageError(error);
            }
          )
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

        function getStatus(issue) {
          if (issue == null) {
            return '';
          }
          return vm.view.status[issue.statusId];
        }

        function getUserPhoto(issue) {
          var user = (issue == null) ? null : vm.model.users[issue.userId];
          if (user == null || user.photo == null || user.photoSrc == '') {
            var img = (user == null || vm.model.users[issue.userId].genre == undefined || vm.model.users[issue.userId].genre == 'Masculino' || vm.model.users[issue.userId].genre == 'Hombre') ? "img/avatarMan.jpg" : "img/avatarWoman.jpg";
            return img;
          } else {
            return user.photoSrc;
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

        function reply() {
          $location.path('/myOrdersComment/' + vm.model.issue.id);
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

    }
})();
