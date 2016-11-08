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
          editMail: editMail,
          editProfileAdvanced: editProfileAdvanced,
          editPassword: editPassword,
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




        vm.myImage="/systems/offices/img/noImage.jpg";
        vm.myCroppedImage='';

        vm.save = save;
        vm.editMail = editMail;

        var handleFileSelect=function(evt) {
          var file=evt.currentTarget.files[0];
          var reader = new FileReader();
          reader.onload = function (evt) {
            $scope.$apply(function($scope){
              vm.myImage=evt.target.result;
            });
          };
          reader.readAsDataURL(file);
        };
        angular.element(document.querySelector('#fileInput')).on('change',handleFileSelect);


        function save() {
          vm.view.style = '';
          // vm.myImage = vm.myCroppedImage;
        }




    }


})();
