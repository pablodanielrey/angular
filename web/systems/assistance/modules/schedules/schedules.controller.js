(function() {
    'use strict'
    angular
      .module('assistance')
      .controller('SchedulesCtrl', ReportsCtrl);

    ReportsCtrl.$inject = ['$scope', 'Assistance', 'Users', '$timeout', 'Login', '$window', 'Offices', '$filter'];

    function ReportsCtrl($scope, Assistance, Users, $timeout, Login, $window, Offices, $filter) {
        var vm = this;
    }


})();
