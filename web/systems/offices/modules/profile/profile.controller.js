(function() {
    'use strict'
    angular
      .module('offices')
      .controller('ProfileCtrl',ProfileCtrl);

    ProfileCtrl.$inject = ['$scope'];

    function ProfileCtrl($scope) {
        var vm = this;

        vm.myImage="/systems/offices/img/noImage.jpg";
        vm.myCroppedImage='';

        vm.save = save;

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
