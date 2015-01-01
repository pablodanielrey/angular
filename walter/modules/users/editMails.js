var app = angular.module('mainApp');

app.controller('EditMailsCtrl', function($scope, Users) {

  $scope.user = { email: '' };
  $scope.mails = [];
  $scope.selected = '';

  /*
    Actualizo los mails del usuario en caso de que sea el que estoy mostrando.
  */
  $scope.$on('UserUpdatedEvent', function(event,data) {
    var user_id = data;
    if ($scope.selected != user_id) {
      return;
    }
    Users.findMails(user_id,
      function(mails) {
        if (mails == null) {
          $scope.mails = [];
        } else {
          $scope.mails = mails;
        }
      },
      function(error) {
        alert(error);
      });
  });

  /*
    Busco los mails del usuario selecionado
  */
  $scope.$on('UserSelectedEvent', function(event,data) {
    $scope.selected = data;
    Users.findMails(data,
      function(mails) {
        if (mails == null) {
          $scope.mails = [];
        } else {
          $scope.mails = mails;
        }
      },
      function(error) {
        alert(error);
      });
  });



  $scope.addMail = function() {
    var email = {
      user_id: $scope.selected,
      email: $scope.user.email
    };
    Users.addMail(email,
      function(ok) {
        // no hago nada ya que voy a recibir un evento : UserUpdatedEvent
      },
      function(error) {
        alert(error);
      }
    );
  }




  $scope.sendConfirmation = function(id) {
    Users.sendConfirmMail(id,
      function(ok) {
        alert('Se ha enviado un mail de confirmación a su casilla. por favor chequee su bandeja de entrada y la carpeta de correo no deseado');
      },
      function(error) {
        alert(error);
      });
  }

  $scope.deleteMail = function(id) {
    Users.deleteMail(id,
      function(ok) {
        // no hago nada ya que se dispara un evento de UserUpdatedEvent
      },
      function(error) {
        alert(error);
      });

  }

});
