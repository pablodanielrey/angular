(function() {
		'use strict'
		angular
			.module('issues')
			.service('IssuesDD', IssuesDD);

		IssuesDD.inject = ['$q', 'Issues', 'Users', 'Files'];

		function IssuesDD($q, Issues, Users, Files) {

      this.issueDetail = issueDetail; //get issue and childs witch users and creators
			this.usersPhotoByIds = usersPhotoByIds; //get issue and childs witch users and creators


			function usersPhotoByIds(ids){
				return Users.findById(ids).then(
					function(users){
						var promises = []
						for(var i = 0; i < users.length; i++){
							//retornar issue si no hay datos definidos de la foto
							if (!users[i].photo) {
								var deferred = $q.defer();
								deferred.resolve("img/avatarWoman.jpg");
								var p = deferred.promise;
							} else {
								var p = Users.findPhoto(users[i].photo).then(
									function(photo) { return Files.toDataUri(photo); }
								);
							}
							promises.push(p);
						}

						return $q.all(promises).then(
							function(response){
								for(var i = 0; i < users.length; i++){
									users[i].photoSrc = response[i];
								}
								return users;
							}
						)
					}
				);
			}


      function issueDetail(id){
				var self = this;
        return Issues.findById(id).then(
          function(issue){
            var size = (issue.children.length) ? issue.children.length : 0;
            var userIds = [];

						//format date
						if(issue.start) issue.start = new Date(issue.start);
            if(issue.userId) userIds.push(issue.userId);
            if(issue.creatorId) userIds.push(issue.creatorId);

            for (var i = 0; i < size; i++) {
                if(issue.children[i].userId) { userIds.push(issue.children[i].userId); }
                if(issue.children[i].creatorId) { userIds.push(issue.children[i].creatorId); }
            }

            if(!userIds.length) return issue;

            return self.usersPhotoByIds(userIds).then(
              function(users){
                for(var i = 0; i < users.length; i++){
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
