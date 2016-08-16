(function() {
    'use strict';

    angular
        .module('issues')
        .controller('MyOrdersCommentCtrl', MyOrdersCommentCtrl);

    MyOrdersCommentCtrl.$inject = ['$scope', '$routeParams', '$location', 'Issues', 'Files'];

    /* @ngInject */
    function MyOrdersCommentCtrl($scope, $routeParams, $location, Issues, Files) {
        var vm = this;

        vm.model = {
          issue: null,
          replyDescription: '',
          files: []
        }

        vm.addFile = addFile;
        vm.removeFile = removeFile;
        vm.createComment = createComment;
        vm.cancelComment = cancelComment;


        activate();

        function activate() {
          var params = $routeParams;
          if (params.issueId == undefined) {
            $location.path('/myOrdersList');
          }
          vm.model.files = [];
          loadIssue(params.issueId);
        }

        function loadIssue(id) {
          Issues.findById(id).then(
            function(issue) {
              vm.model.issue = issue;
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

          // vm.messageLoading();
          Issues.createComment(subject, vm.model.replyDescription, parentId, officeId, vm.model.files).then(
            function(data) {

            }, function(error) {
              vm.messageError(error);
            }
          );
        }



    }
})();
