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
	this.getOffices = getOffices;
	this.getAreas = getAreas;


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

	offices = [{name: 'Ditesi', id: '1', parentId: null, subjects: ['Internet', 'Wifi', 'Programas', 'No puedo iniciar la pc', 'Error en sistema','Correo Electrónico', 'Otro']},
						 {name:'Soporte', id:'2', parentId:'1', subjects: ['Internet', 'Wifi', 'Programas', 'No puedo iniciar la pc', 'Correo Electrónico', 'Otro']},
 						 {name:'Desarrollo', id:'3', parentId:'1', subjects: ['Error en sistema', 'Otro']},
 						 {name:'Redes y Servidores', id:'4', parentId:'1', subjects: ['Internet', 'Wifi', 'Correo Electrónico', 'Otro']},
						 {name:'Mantenimiento y Servicios Generales', id: '5', parentId: null, subjects: ['Limpieza', 'Electricidad', 'Tendido cableado de red', 'Otro']},
					 	 {name:'Mantenimiento', id:'6', parentId:'5', subjects: ['Electricidad', 'Tendido cableado de red', 'Otro']},
 						 {name:'Servicios Generales', id:'7', parentId:'5', subjects: ['Limpieza', 'Otro']}
						]

	subjects = ['Internet', 'Wifi', 'Correo Electrónico', 'Otro', 'Limpieza', 'Electricidad', 'Tendido cableado de red']

	function getOffices() {
		return new Promise(function(cok, cerr) {
			off = []
			for (var i = 0; i < offices.length; i++) {
				if (offices[i].parentId == null) {
					off.push(offices[i]);
				}
			}
			cok(off);
    });

	}

	function getAreas(office) {
		return new Promise(function(cok, cerr) {
			off = [];
			for (var i = 0; i < offices.length; i++) {
				if (offices[i].parentId == office.id) {
					off.push(offices[i]);
				}
			}
			cok(off);
    });
	}


}
