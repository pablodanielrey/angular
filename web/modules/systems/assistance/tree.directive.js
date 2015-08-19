angular
    .module('mainApp')
    .directive('tree', tree);

tree.$inject = ['$compile'];
function tree($compile) {
  return {
      restrict: "E",
      scope: {family: '='},
      templateUrl: '/modules/systems/assistance/tree.html',
      compile: function(tElement, tAttr) {
          var contents = tElement.contents().remove();
          var compiledContents;
          return function(scope, iElement, iAttr) {
              if(!compiledContents) {
                  compiledContents = $compile(contents);
              }
              compiledContents(scope, function(clone, scope) {
                       iElement.append(clone);
              });
          };
      }
  };
}
