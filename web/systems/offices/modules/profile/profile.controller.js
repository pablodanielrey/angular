(function() {
    'use strict'
    angular
      .module('offices')
      .controller('ProfileCtrl',ProfileCtrl);

    ProfileCtrl.$inject = ['$scope'];

    function ProfileCtrl($scope) {
        var vm = this;

        ////////////////

        vm.view = {
          style: '',
          styleMail: '',
          back: back,
          newMail: newMail,
          editMail: editMail,
          editProfileAdvanced: editProfileAdvanced,
          editPassword: editPassword,
          getEMailClass: getEMailClass,
        }


        function editMail() {
          vm.view.style = 'pantallaEdicionUsuario editarMail';
        }

        function editProfileAdvanced() {
          vm.view.style = 'pantallaEdicionUsuario editarPerfilAvanzado';
        }

        function editPassword() {
          vm.view.style = 'pantallaEdicionUsuario editarContrasena';
        }

        function newMail() {
          vm.view.styleMail = 'nuevoMail';
        }

        function back() {
          // console.log('dffg');
          vm.view.styleMail = '';
        }

        function getEMailClass(e) {
          if (e.confirmed) {
            if (e.preferred) {
              return "mailConfirmado mailPredeterminado";
            } else {
              return "mailconfimado";
            }
          } else {
            return "mailSinConfirmar";
          }
        }

        var handleFileSelect = function(evt) {
          var file=evt.currentTarget.files[0];
          var reader = new FileReader();
          reader.onload = function (evt) {
            $scope.$apply(function($scope){
              vm.model.user.myImage = evt.target.result;
            });
          };
          reader.readAsDataURL(file);
        };
        angular.element(document.querySelector('#fileInput')).on('change',handleFileSelect);


        ////////////////////////


        vm.model = {
          user: {
            myImage: '/systems/offices/img/noImage.jpg',
            myCroppedImage: ''
          },

          userMails: [
            {
              email: 'prueba@econo.unlp.edu.ar',
              confirmed: false,
              preferred: true
            },
            {
              email: 'prueba2@econo.unlp.edu.ar',
              confirmed: true,
              preferred: false
            },
            {
              email: 'pruba@hotmail.com',
              confirmed: true,
              preferred: false
            },
            {
              email: 'pruba2@hotmail.com',
              confirmed: true,
              preferred: true
            }
          ]

        }

        vm.deleteEmail = function(m) {
          for (var i = 0; i < vm.model.userMails.length; i++) {
            console.log(m);
            if (vm.model.userMails[i] == m) {
              vm.model.userMails.splice(i,1);
            }
          }
        }

        vm.addEmail = function(email) {
          vm.moedl.userMails.push({
            email: email,
            confirmed: false,
            preferrd: false
          });
        }


        vm.save = save;

        function save() {
          vm.view.style = '';
          // vm.myImage = vm.myCroppedImage;
        }




    }


})();
