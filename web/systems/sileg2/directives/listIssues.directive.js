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
              var template = (attr.template == undefined) ?  'directives/listIssues.html' : attr.template;
              var time = new Date().getTime();
              return template + '?t=' + time;
            },
            scope: {},
            link: linkFunc,
            controller: ListIssuesDirectiveCtrl,
            controllerAs: 'vm',
            bindToController: {
              issues: '=issues',
              users: '=users',
              search: '=search',
              src: '=src'
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
        vm.getStatus = getStatus;
        vm.getCreator = getCreator;
        vm.getPriority = getPriority;

        vm.view= {
          status: ['','abierta', 'enProgreso', 'cerrada', 'comentarios', 'cerrada', 'rechazada', 'pausada'],
          priorities: ['baja', 'normal', 'alta', 'alta', 'alta'] //solo se maneja el estilo alta, si esta como urgente o inmediata se lo toma solo como alta
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
          if (issue == null) {
            return;
          }

          issue.fullName = (user == null ) ? 'No tiene nombre' : getName(user) + ' ' + getLastname(user);

          return issue.fullName;
        }

        function getName(user) {
          return (user.name == undefined) ? '' : user.name;
        }

        function getLastname(user) {
          return (user.lastname == undefined) ? '' : user.lastname;
        }

        function getStatus(issue) {
          if (issue == null) {
            return '';
          }
          return vm.view.status[issue.statusId];
        }

        function getCreator(issue) {
          if (issue == null || issue.creatorId == null || issue.creatorId == '') {
            return '';
          }

          var user = vm.users[issue.creatorId];
          issue.creatorName = (user == null ) ? 'No tiene nombre' : getName(user) + ' ' + getLastname(user);
          return issue.creatorName;
        }

        function getPriority(issue) {
          if (issue == null || issue.priority == undefined) {
            return '';
          }
          var p = (issue.priority > 2) ? 2 : issue.priority - 1;
          return vm.view.priorities[p];
        }


    }
})();
