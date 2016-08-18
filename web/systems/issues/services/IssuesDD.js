(function() {
		'use strict'
		angular
			.module('issues')
			.service('IssuesDD', IssuesDD);

		IssuesDD.inject = ['Issues', 'Users'];

		function IssuesDD(Issues, Users) {

      this.issueDetail = issueDetail; //get issue and childs witch users and creators


      function issueDetail(id){
        return Issues.findById(id).then(
          function(issue){
            var size = (issue.children.length) ? issue.children.length : 0;
            var userIds = [];
            if(issue.userId) userIds.push(issue.userId);
            if(issue.creatorId) userIds.push(issue.creatorId);

            for (var i = 0; i < size; i++) {
                if(issue.children[i].userId) { userIds.push(issue.children[i].userId); }
                if(issue.children[i].creatorId) { userIds.push(issue.children[i].creatorId); }
            }

            if(!userIds.length) return issue;

            return Users.findById(userIds).then(
              function(users){
                for(var i = 0; i < users.length; i++){
                    console.log(issue.userId);
                    if(issue.creatorId == users[i].id){ issue.creator = users[i]; }
                    if(issue.userId == users[i].id){ issue.user = users[i]; }
                    for (var j = 0; j < issue.children.length; j++) {
                      if(issue.children[j].userId == users[i].id){ issue.children[j].user = users[i]; }
                      if(issue.children[j].creatorId == users[i].id){ issue.children[j].creator = users[i]; }
                      if(issue.children[j].creator && issue.children[j].user) break;
                    }
                }

                return issue;
              }
            );
          }
        );
      };
		};



})();
