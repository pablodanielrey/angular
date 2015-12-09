

app.controller('IndexCtrl',IndexCtrl);

function IndexCtrl() {


  $scope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });
}
