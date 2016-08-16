(function() {
    'use strict';

    angular
        .module('issues')
        .directive('eListIssues', eListIssues);

    /* @ngInject */
    function eListIssues() {
        var directive = {
            restrict: 'E',
            templateUrl: function(elem, attr) {
              var time = new Date().getTime();
              return 'directives/listIssues.html?t=' + time;
            },
            scope: {},
            link: linkFunc,
            controller: ListIssuesDirectiveCtrl,
            controllerAs: 'vm',
            bindToController: {
              issues: '=issues',
              users: '=users',
              detail: '&onDetail'
            }
        };

        return directive;

        function linkFunc(scope, el, attr, ctrl) {
        }
    }

    ListIssuesDirectiveCtrl.$inject = ['$scope'];

    /* @ngInject */
    function ListIssuesDirectiveCtrl($scope) {
        var vm = this;
        vm.getDate = getDate;
        vm.getDiffDay = getDiffDay;
        vm.getFullName = getFullName;
        vm.viewDetail = viewDetail;

        function viewDetail(issue) {
          vm.detail({issueId: issue.id});
        }

        activate();

        function activate() {
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

        function getFullName(issue) {
          if (issue == null) {
            return;
          }
          var user = vm.users[issue.userId];
          return (user == null) ? 'No tiene nombre' : user.name + ' ' + user.lastname;
        }


    }
})();
