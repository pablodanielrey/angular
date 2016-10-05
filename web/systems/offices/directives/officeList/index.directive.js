(function() {
    'use strict';

    angular
        .module('offices')
        .directive('eOfficeList', eOfficeList);

    /* @ngInject */
    function eOfficeList() {
        var directive = {
            restrict: 'E',
            templateUrl: function(elem, attr) {
              var time = new Date().getTime();
              return 'directives/officeList/index.html?t=' + time;
            },
            scope: {},
            link: linkFunc,
            controller: OfficeListCtrl,
            controllerAs: 'vm',
            bindToController: {
              offices: '=offices',
              types: '=types',
              selectedType: '=selectedType',
              onSelectType: '&onSelectType',
              onRemove: '&onRemove',
              onCreate: '&onCreate',
              onSelect: '&onSelect'
            }
        };

        return directive;

        function linkFunc(scope, el, attr, ctrl) {

        }
    }

    OfficeListCtrl.$inject = ['$scope'];

    /* @ngInject */
    function OfficeListCtrl($scope) {
        var vm = this;
        vm.create = create;
        vm.remove = remove;
        vm.select = select;
        vm.selectType = selectType;
        vm.model = {
          search: {'name':'', 'type': {'value':''}}
        };
        activate();

        function activate() {
          vm.model.search = {};
          vm.model.search.name = '';
          vm.model.search.type = {};
          vm.model.search.type = (vm.selectedType == null || vm.selectedType.value === undefined) ? '' : vm.selectedType.value;
        }

        $scope.$watch('vm.selectedType', function(newValue, oldValue) {
          vm.model.search.type = {};
          vm.model.search.type.value = (vm.selectedType == null || vm.selectedType.value === undefined) ? '' : vm.selectedType.value;
        })

        function create() {
          vm.onCreate();
        }

        function remove(office) {
          vm.onRemove({office: office});
        }

        function select(office) {
          vm.onSelect({office: office});
        }

        function selectType() {
          vm.onSelectType({type: vm.selectedType});
        }
    }
})();
