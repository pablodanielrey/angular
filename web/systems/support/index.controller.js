
app.controller('IndexCtrl',IndexCtrl);

IndexCtrl.$inject = ['$rootScope','$scope', '$window', 'Notifications', 'Login'];

function IndexCtrl($rootScope, $scope, $window, Notifications, Login) {

    $scope.$on('$viewContentLoaded', function(event) {

    });

};
