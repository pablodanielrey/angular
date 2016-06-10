angular
	.module('mainApp')
	.service('Issue', Issue);

Issue.inject = ['Utils','Session','$wamp'];

function Issue (Utils, Session, $wamp) {

  this.getMyIssues = getMyIssues;
  this.getOfficesIssues = getOfficesIssues;
  this.getAssignedIssues = getAssignedIssues;
  this.findById = findById;
  this.create = create;
  this.createComment = createComment;
  this.changeStatus = changeStatus;


  function getMyIssues() {
    return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('issue.getMyIssues', [sid])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
	}

  function getOfficesIssues() {
		return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('issue.getOfficesIssues', [sid])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
	}

  function getAssignedIssues() {
		return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('issue.getAssignedIssues', [sid])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
	}

  function findById(id) {
		return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('issue.findById', [sid, id])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
	}

  function create(subject, description, parentId, officeId) {
		return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('issue.create', [sid, subject, description, parentId, officeId])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
	}

  function createComment(subject, description, parentId, officeId) {
		return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('issue.createComment', [sid, subject, description, parentId, officeId])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
	}

  function changeStatus(issue, status) {
		return new Promise(function(cok, cerr) {
      var sid = Session.getSessionId();
  		$wamp.call('issue.changeStatus', [sid, issue, status])
      .then(function(v) {
        cok(v);
      },function(err) {
        cerr(err);
      });
    });
	}

}
