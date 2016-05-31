angular
  .module('mainApp')
  .controller('ProfileCtrl', ProfileCtrl);

ProfileCtrl.inject = ['$rootScope', '$scope', 'Users', 'Login', 'Systems', 'Files', 'Student']

function ProfileCtrl($rootScope, $scope, Users, Login, Systems, Files, Student) {

  $scope.initialize = initialize;
  $scope.loadUser = loadUser;
  $scope.getUserPhoto = getUserPhoto;
  $scope.addPhoto = addPhoto;
  $scope.getStudentNumber = getStudentNumber;

  $scope.model = {
    user: null,
    userId: '',
    loadingPhoto: false,
    studentNumber: null
  }

  $scope.$on('$viewContentLoaded', function(event) {
    $scope.model.userId = '';
    Login.getSessionData()
      .then(function(s) {
          $scope.model.userId = s.user_id;
          $scope.initialize();
      }, function(err) {
        console.log(err);
      });
  });

  function initialize() {
    $scope.loadUser();
  }

  function loadUser() {
    Users.findById([$scope.model.userId]).then(function(users) {
      $scope.model.user = (users.length > 0) ? users[0] : null;
    }, function(error) {
      console.log('Error al buscar el usuario')
    });

    Student.findById($scope.model.userId).then(function(student) {
      if (student != null && student.studentNumber != undefined) {
        $scope.model.studentNumber = student.studentNumber;
      }
    });
  }

  function getStudentNumber() {
    return $scope.model.studentNumber;
  }

  function addPhoto(fileName, fileContent) {
    $scope.model.formatPhoto = false;
    console.log(fileName);

    re = /^.*\.jpg$/i
    if (!re.test(fileName)) {
      console.log('formato no soportado');
      $scope.model.formatPhoto = true;
      return;
    }

    $scope.model.loadingPhoto = true;

    var photo = window.btoa(fileContent);
    Files.upload(null, fileName, 'image/jpeg', Files.BASE64, photo).then(
        function(id) {
          $scope.model.loadingPhoto = false;
          $scope.model.user.photo = id;
          Users.updateUser($scope.model.user, function(res) {

          }, function(err) {
            console.log(err);
          })
        },
        function(err) {
          $scope.model.loadingPhoto = false;
          console.log(err);
          Notifications.message(err);
        }

    )
  }

  function getUserPhoto() {
    if ($scope.model.user == null || $scope.model.user.photo == null || $scope.model.user.photo == '') {
      return null;
    } else {
      return "/c/files.py?i=" + $scope.model.user.photo;
    }
  }


}
