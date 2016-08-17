(function() {
		'use strict'
		angular
			.module('issues')
			.service('IssuesDD', IssuesDD);

		IssuesDD.inject = ['Issues', 'Users'];

		function IssuesDD(Issues, Users) {

      this.fullIssue = fullIssue; //get issue and childs witch users


      function issueFull(id){
        Issues.findById(id).then(
          function(issue) {
            var size = (issue.children.length) ? issue.children.length : 0;
            var userIds = [];
            if(issue.userId) userIds.push(issue.userId);

            for (var i = 0; i < size; i++) {
                var child = issue.children[i];

                if (child.user == undefined) {
                  loadUser(child.userId);
                }
            }

            vm.model.issue = issue;
            if (issue.fromOfficeId != undefined) {
              loadOffice(issue.fromOfficeId);
            }
            closeMessage();
          }, function(error) {
            vm.messageError(error);
          }
        );
      };


		}

})();
