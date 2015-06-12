
/*
  bug de angular que no autollena los campos que son salvados por los exploradores.


  http://stackoverflow.com/questions/14965968/angularjs-browser-autofill-workaround-by-using-a-directive

  
*/

var app = angular.module('mainApp');

app.directive("autofill", function () {
    return {
        require: "ngModel",
        link: function (scope, element, attrs, ngModel) {
            scope.$on("autofill:update", function() {
                ngModel.$setViewValue(element.val());
            });
        }
    };
});
