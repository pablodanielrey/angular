(function() {
    'use strict';

    angular
        .module('issues')
        .controller('MyOrdersDetailCtrl', MyOrdersDetailCtrl);

    MyOrdersDetailCtrl.$inject = ['$scope', '$routeParams', '$location', 'Issues', 'Users', 'Files', 'Offices'];

    /* @ngInject */
    function MyOrdersDetailCtrl($scope, $routeParams, $location, Issues, Users, Files, Offices) {
        var vm = this;
        vm.model = {
          issue: null,
          users: []
        }

        vm.view = {
          status: ['','abierta', 'enProgreso', 'cerrada', 'comentarios', 'cerrada', 'rechazada', 'pausada']
        }

        vm.loadIssue = loadIssue;
        vm.getName = getName;
        vm.getLastname = getLastname;
        vm.getStatus = getStatus;
        vm.getUserPhoto = getUserPhoto;
        vm.getDiffDay = getDiffDay;
        vm.getDate = getDate;
        vm.reply = reply;

        activate();

        function activate() {
          var params = $routeParams;
          if (params.issueId == undefined) {
            $location.path('/myOrdersList');
          }
          vm.model.users = [];
          vm.loadIssue(params.issueId);
        }

        function loadIssue(id) {
          Issues.findById(id).then(
            function(issue) {
              var size = (issue.children == undefined) ? 0 : issue.children.length;
              for (var i = 0; i < size; i++) {
                  var child = issue.children[i];
                  if (child.user == undefined) {
                    loadUser(child.userId);
                  }
              }

              vm.model.issue = issue;
              if (issue.fromOfficeId != undefined) {
                loadOffice(issue.fromOfficeId);
              }
            }, function(error) {
              vm.messageError(error);
            }
          );
        }

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

        function loadOffice(officeId) {
          if (officeId == undefined || officeId == null) {
            vm.model.office = null;
            return;
          }
          Offices.findById([officeId]).then(
            function(offices) {
              vm.model.office = (offices == null || offices.length <= 0) ? null : offices[0];
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
            return '/systems/login/modules/img/imgUser.jpg';
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

    }
})();
