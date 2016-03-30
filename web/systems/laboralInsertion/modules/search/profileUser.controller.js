angular
  .module('mainApp')
  .controller('ProfilesCtrl', ProfilesCtrl);

ProfilesCtrl.$inject = ['$rootScope','$scope', 'LaboralInsertion'];

function ProfilesCtrl($rootScope, $scope, LaboralInsertion) {

  $scope.initialize = initialize;
  $scope.getTitleProfile = getTitleProfile;
  $scope.cancelProfile = cancelProfile;
  $scope.saveProfile = saveProfile;
  $scope.saveUserData = saveUserData;

  $scope.data = {};
  $scope.selectInscription = null;

  function initialize() {
    console.log("Profile users");
  }

  $rootScope.$on('$viewContentLoaded', function(event) {
    $scope.initialize();
  });

  $scope.$on('openProfileEvent', function(event, i, userData) {
    $scope.data.approved = i.approved;
    $scope.data.userId = i.userId;
    $scope.data.degree = i.degree;
    $scope.data.average1 = i.average1;
    $scope.data.average2 = i.average2;
    $scope.data.userData = userData;
    $scope.selectInscription = i;
  });

  function cancelProfile() {
    $scope.data = {};
    $scope.selectInscription = null;
    $scope.$emit('closeProfileEvent');
  }

  function saveProfile() {
    $scope.selectInscription.approved = $scope.data.approved;
    $scope.selectInscription.userId = $scope.data.userId;
    $scope.selectInscription.degree = $scope.data.degree;
    $scope.selectInscription.average1 = $scope.data.average1;
    $scope.selectInscription.average2 = $scope.data.average2;
    $scope.selectInscription.checked = true;
    LaboralInsertion.persistInscriptionByUser($scope.selectInscription.userId,$scope.selectInscription).then(function(r) {
      $scope.saveUserData();
    }, function(err) {
      console.log(err);
    });;
  }

  function saveUserData() {
    LaboralInsertion.persist($scope.data.userData).then(function(r) {
      $scope.$emit('closeProfileEvent');
    }, function(err) {
      console.log(err);
    });
  }


  function getTitleProfile() {
     var i = $scope.data;
     if (i == null || i.userId == null) {
       return '';
     }

     var user = $scope.model.users[i.userId];
     return user.lastname + ", " + user.name;
  }

}
