(function() {
    'use strict';

    angular
        .module('issues')
        .controller('MyOrdersCommentCtrl', MyOrdersCommentCtrl);

    MyOrdersCommentCtrl.$inject = ['$scope', '$routeParams', '$location', '$timeout', 'Issues', 'Files', 'Login'];

    /* @ngInject */
    function MyOrdersCommentCtrl($scope, $routeParams, $location, $timeout, Issues, Files, Login) {
        var vm = this;

        vm.model = {
          issue: null,
          replyDescription: '',
          files: [],
          privateTransport: null
        }

        vm.view = {
          style3: '',
          styles3: ['','pantallaMensajeAlUsuario'],
          style4: '',
          styles4: ['', 'mensajeCargando', 'mensajeError', 'mensajeEnviado']
        }

        vm.addFile = addFile;
        vm.removeFile = removeFile;
        vm.createComment = createComment;
        vm.cancelComment = cancelComment;

        vm.closeMessage = closeMessage;
        vm.messageLoading = messageLoading;
        vm.messageError = messageError;
        vm.messageSending = messageSending;


        $scope.$on('openPrivateConnection', function(event, args) {
          vm.model.privateTransport = Login.getPrivateTransport();
          activate();
        });

        activate();


        function activate() {
          if (Login.getPrivateTransport() == null) {
            return;
          }
          var params = $routeParams;
          if (params.issueId == undefined) {
            $location.path('/myOrders');
          }
          messageLoading();
          vm.model.files = [];
          loadIssue(params.issueId);
        }

        function loadIssue(id) {
          Issues.findById(id).then(
            function(issue) {
              $scope.$apply(function() {
                vm.model.issue = issue;
                closeMessage();
              })
            }, function(error) {
              vm.messageError(error);
            }
          );
        }

        function addFile(fileName,fileContent, fileType, fileSize) {
          var file = {};
          file.name = fileName;
          file.content = window.btoa(fileContent);
          file.type = fileType;
          file.size = fileSize;
          file.codec = Files.BASE64;
          vm.model.files.push(file);
        }

        function removeFile(file) {
          var index = vm.model.files.indexOf(file);
          if (index >= 0) {
            vm.model.files.splice(index, 1);
          }
        }

        function cancelComment() {
          $location.path('myOrdersDetail/' + vm.model.issue.id);
        }

        function createComment() {
          var subject = vm.model.issue.subject;
          var parentId = vm.model.issue.id;
          var officeId = vm.model.issue.projectId;

          vm.messageLoading();
          Issues.createComment(subject, vm.model.replyDescription, parentId, officeId, vm.model.files).then(
            function(data) {
              $scope.$apply(function() {
                vm.messageSending();
              });
              $timeout(function() {
                $location.path('myOrdersDetail/' + vm.model.issue.id);
              }, 2000);
            }, function(error) {
              vm.messageError(error);
            }
          );
        }

        function messageError(error) {
          vm.view.style3 = vm.view.styles3[1];
          vm.view.style4 = vm.view.styles4[2];
          $timeout(function() {
            vm.closeMessage();
          }, 2000);
        }

        function closeMessage() {
          vm.view.style3 = vm.view.styles3[0];
          vm.view.style4 = vm.view.styles4[0];
        }

        function messageLoading() {
          vm.view.style3 = vm.view.styles3[1];
          vm.view.style4 = vm.view.styles4[1];
        }

        function messageSending() {
          vm.view.style3 = vm.view.styles3[1];
          vm.view.style4 = vm.view.styles4[3];
        }



    }
})();
