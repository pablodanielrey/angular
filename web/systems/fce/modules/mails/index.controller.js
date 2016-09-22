(function() {
    'use strict';

    angular
        .module('mainApp')
        .controller('MailsCtrl', MailsCtrl);

    MailsCtrl.$inject = ['$rootScope', '$scope', 'Login','Users', '$window'];

    /* @ngInject */
    function MailsCtrl($rootScope, $scope, Login, Users, $window) {
        var vm = this;

        vm.model = {
          user: null,
          userId: null,
          laboralMails: [],
          alternativeMails: [],
          mail: ''
        }

        vm.view = {
          style: '',
          styles: ['', 'newMail'],
          styleMail: ['confirmed', 'pending', 'sending']
        }

        // métodos
        vm.initModel = initModel;
        vm.initView = initView;
        vm.openWebmail = openWebmail;
        vm.addMail = addMail;
        vm.saveMail = saveMail;
        vm.resendEmailValidation = resendEmailValidation;
        vm.loadMails = loadMails;
        vm.removeMail = removeMail;

        activate();

        function activate() {
          vm.model.userId = null;
          vm.initView();
          Login.getSessionData()
            .then(function(s) {
                vm.model.userId = s.user_id;
                vm.initModel();
            }, function(err) {
              console.log(err);
            });
        }

        function initView() {
          vm.view.style = vm.view.styles[0];
        }

        function initModel() {
          Users.findById([vm.model.userId]).then(function(users) {
            vm.model.user = (users == null || users.length <= 0) ? null : users[0];
          }, function(error) {
            console.log('Error al buscar el usuario')
          });

          vm.loadMails();
        }

      function loadMails() {
        vm.model.alternativeMails = [];
        vm.model.laboralMails = [];
        
        Users.findAllMails(vm.model.userId).then(function(mails) {
          setLaboralMails(mails);
          setAlternativeMails(mails);
        }, function(error) {
          console.log('Error al buscar los mails del usuario')
        });
      }

      function setLaboralMails(mails) {
          for (var i = 0; i < mails.length; i++) {
            mails[i].style = (mails[i].confirmed) ? vm.view.styleMail[0] : vm.view.styleMail[1];
            if (isLaboral(mails[i].email)) {
              vm.model.laboralMails.push(mails[i]);
            }
          }
        }

        function isLaboral(mail) {
          var domain = 'econo.unlp.edu.ar'
          var array = mail.split("@")
          return (array.length > 1 && array[array.length - 1] == domain)
        }

        function setAlternativeMails(mails) {
          for (var i = 0; i < mails.length; i++) {
            if (!isLaboral(mails[i].email)) {
              vm.model.alternativeMails.push(mails[i]);
            }
          }
        }

        function openWebmail() {
          $window.open('http://correo.econo.unlp.edu.ar', '_blank');
        }

        function addMail() {
          vm.model.email = '';
          vm.view.style = vm.view.styles[1];
        }

        function saveMail() {
          var re = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/i;
          if (!re.test(vm.model.email)) {
            return;
          }

          Users.createMail(vm.model.email, vm.model.userId).then(function(email) {
            email.style = vm.view.styleMail[2];
            vm.model.alternativeMails.push(email);
            vm.view.style = vm.view.styles[0];
            vm.resendEmailValidation(email);
          }, function(error) {
            console.log('Error al crear el mail')
          });
        }

        function resendEmailValidation(email) {
          email.code = '';
          Users.sendEmailConfirmation(vm.model.user.name, vm.model.user.lastname, email.id).then(function(ok) {
            email.style = vm.view.styleMail[1];
          }, function(error) {
            console.log('Error al enviar el mail')
          });
        }

        function removeMail(email) {
          Users.removeMail(email.id).then(function (ok) {
            console.log('eliminado');
            vm.loadMails();
          }, function(error) {
            console.log('Error al eliminar el mail')
          });
        }

    }
})();
