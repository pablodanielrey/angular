(function() {
    'use strict'
    var app = angular.module('sileg')

    app.config(['$routeProvider', function($routeProvider) {
      $routeProvider

      .when('/teacher', {templateUrl: 'modules/teacher/teacher.html', controller: 'TeacherCtrl' })
      .otherwise({ redirectTo: '/teacher' });

    }]);

})();
