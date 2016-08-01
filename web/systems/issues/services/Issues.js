(function() {
		'use strict'
		angular
			.module('issues')
			.service('Issues', Issues);

		Issues.inject = ['Login'];

		function Issues(Login) {

		  this.getMyIssues = getMyIssues;
		  this.getOfficesIssues = getOfficesIssues;
		  this.getAssignedIssues = getAssignedIssues;
		  this.findById = findById;
		  this.create = create;
		  this.createComment = createComment;
		  this.changeStatus = changeStatus;
			this.changePriority = changePriority;
			this.getOffices = getOffices;
			this.getAreas = getAreas;
			this.$wamp = Login.getTransport()['private'];

		  function getMyIssues() {
		    return new Promise(function(cok, cerr) {
		  		this.$wamp.call('issues.getMyIssues')
		      .then(function(v) {
		        cok(v);
		      },function(err) {
		        cerr(err);
		      });
		    });
			}

		  function getOfficesIssues() {
				return new Promise(function(cok, cerr) {
		  		this.$wamp.call('issues.getOfficesIssues')
		      .then(function(v) {
		        cok(v);
		      },function(err) {
		        cerr(err);
		      });
		    });
			}

		  function getAssignedIssues() {
				return new Promise(function(cok, cerr) {
		  		this.$wamp.call('issues.getAssignedIssues')
		      .then(function(v) {
		        cok(v);
		      },function(err) {
		        cerr(err);
		      });
		    });
			}

		  function findById(id) {
				return new Promise(function(cok, cerr) {
		  		this.$wamp.call('issues.findById', [id])
		      .then(function(v) {
		        cok(v);
		      },function(err) {
		        cerr(err);
		      });
		    });
			}

		  function create(subject, description, parentId, officeId, fromOfficeId, authorId, files) {
				return new Promise(function(cok, cerr) {
		  		this.$wamp.call('issues.create', [subject, description, parentId, officeId, fromOfficeId, authorId, files])
		      .then(function(v) {
		        cok(v);
		      },function(err) {
		        cerr(err);
		      });
		    });
			}

		  function createComment(subject, description, parentId, officeId, files) {
				return new Promise(function(cok, cerr) {
		  		this.$wamp.call('issues.createComment', [subject, description, parentId, officeId, files])
		      .then(function(v) {
		        cok(v);
		      },function(err) {
		        cerr(err);
		      });
		    });
			}

		  function changeStatus(issue, status) {
				return new Promise(function(cok, cerr) {
		  		this.$wamp.call('issues.changeStatus', [issue, status])
		      .then(function(v) {
		        cok(v);
		      },function(err) {
		        cerr(err);
		      });
		    });
			}

		  function changePriority(issue, priority) {
				return new Promise(function(cok, cerr) {
		  		this.$wamp.call('issues.changePriority', [issue, priority])
		      .then(function(v) {
		        cok(v);
		      },function(err) {
		        cerr(err);
		      });
		    });
			}

			function getOffices() {
				return this.$wamp.call('issues.getOffices',[]);

			}

			function getAreas(office) {
				return this.$wamp.call('issues.getAreas',[office.id]);
			}

		}

})();
