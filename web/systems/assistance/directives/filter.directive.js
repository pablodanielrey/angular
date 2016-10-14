(function() {
    'use strict';

    angular
        .module('assistance')
        .directive('eFilterAssistance', eFilterAssistance);

    /* @ngInject */
    function eFilterAssistance() {
        var directive = {
            restrict: 'E',
            templateUrl: function(elem, attr) {
              var time = new Date().getTime();
              return 'directives/filter.html?t=' + time;
            },
            scope: {},
            link: linkFunc,
            controller: FilterAssistanceCtrl,
            controllerAs: 'vm',
            bindToController: {
              search: '=search',
              columns: '=columns',
              getOffices: '&getOffices',
              find: '&find',
              print: '&print',
              download: '&download'
            }
        };

        return directive;

        function linkFunc(scope, el, attr, ctrl) {

        }
    }

    FilterAssistanceCtrl.$inject = ['$scope', 'Offices'];

    /* @ngInject */
    function FilterAssistanceCtrl($scope, Offices) {
        var vm = this;

        vm.model = {
          search: {},
          columns: []
        }

        vm.view = {
          style: ''
        }

        vm.resetFilters = resetFilters;
        vm.selectAllOffices = selectAllOffices;
        vm.displayOffices = displayOffices;
        vm.displayDate = displayDate;
        vm.isSelectedOffice = isSelectedOffice;
        vm.selectOffice = selectOffice;
        vm.findAndClose = findAndClose;
        vm.isAllOffices = isAllOffices;

        activate();

        function activate() {
          angular.copy(vm.search, vm.model.search);
          angular.copy(vm.columns, vm.model.columns);
          vm.view.officeSearch = '';
        }

        function resetFilters() {
          vm.search.offices = vm.model.search.offices ;
          vm.search.start = vm.model.search.start;
          vm.search.end = vm.model.search.end;
          vm.columns = vm.model.columns;
          vm.find();
        }

        function selectAllOffices() {
          if (!vm.isAllOffices()) {
            var offices = vm.getOffices();
            for (var i = 0; i < offices.length; i++) {
              if (!isSelectedOffice(offices[i])) {
                vm.search.offices.push(offices[i].id);
              }
            }
          } else {
            vm.search.offices = [];
          }
        }

        function isAllOffices() {
          return vm.search.offices.length == vm.getOffices().length;
        }

        function findAndClose() {
          vm.view.style = '';
          vm.find();
        }

        function isSelectedOffice(office) {
          return vm.search.offices.indexOf(office.id) >=  0;
        }

        function selectOffice(office) {
          var index = vm.search.offices.indexOf(office.id);
          if (index < 0) {
            vm.search.offices.push(office.id);
          } else {
            vm.search.offices.splice(index, 1);
          }
        }

        function displayOffices() {
          vm.view.style = (vm.view.style == "seleccionarOficinas") ? '' : "seleccionarOficinas";
        }

        function displayDate() {
          vm.view.style = (vm.view.style == "rangoFechas") ? '' : "rangoFechas";
        }


    }
})();
