angular
	.module('mainApp')
	.service('Assistance',Assistance);

Assistance.inject = ['Utils','Session','$wamp'];

function Assistance (Utils, Session, $wamp) {

	var services = this;

	services.getAssistanceData = getAssistanceData;
	services.getAssistanceStatusByDate = getAssistanceStatusByDate;
	services.getAssistanceStatusByUsers = getAssistanceStatusByUsers;

	//  ------------------------ FAILS -----------------------------
	services.getFailsByDate = getFailsByDate;
	// services.getFailsByFilter = getFailsByFilter; --> no se esta utilizando

	//  ------------------------ SCHEDULES -----------------------------
	services.getSchedules = getSchedules;
	services.getSchedulesHistory = getSchedulesHistory;
	services.persistSchedule = persistSchedule;
	services.persistScheduleWeek = persistScheduleWeek;
	services.deleteSchedule = deleteSchedule;

	//  ------------------------ JUSTIFICATIONS -----------------------------
	services.getJustifications = getJustifications;
	services.getJustificationsByUser = getJustificationsByUser;
	services.getJustificationStock = getJustificationStock;
	services.updateJustificationStock = updateJustificationStock;

	services.getGeneralJustificationRequests = getGeneralJustificationRequests;
	services.deleteGeneralJustificationRequest = deleteGeneralJustificationRequest;
	services.requestGeneralJustification = requestGeneralJustification;

	services.requestGeneralJustificationRange = requestGeneralJustificationRange;


	// services.getJustificationRequestsByDate = getJustificationRequestsByDate;
	services.getJustificationRequestsToManage = getJustificationRequestsToManage;
	services.getJustificationRequests = getJustificationRequests;
	services.updateJustificationRequestStatus = updateJustificationRequestStatus;
	services.requestJustification = requestJustification;
	services.requestJustificationRange = requestJustificationRange;
	services.getSpecialJustifications = getSpecialJustifications;

	//  ------------------------ OVERTIME -----------------------------
	services.getOvertimeRequests = getOvertimeRequests;
	services.getOvertimeRequestsToManage = getOvertimeRequestsToManage;
	services.requestOvertime = requestOvertime;
	services.updateRequestOvertimeStatus = updateRequestOvertimeStatus;




	function getAssistanceData(userId, date, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.getAssistanceData', [sid, userId, date])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	};

	function getAssistanceStatusByDate(userId, date, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.getAssistanceStatusByDate', [sid, userId, date])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	};


	function getAssistanceStatusByUsers(usersIds, dates, status, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.getAssistanceStatusByUsers', [sid, usersIds, dates, status])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	};

	/* --------------------------------------------------------------
	 * --------------------  FALLAS ---------------------------------
	 * --------------------------------------------------------------
	 */

	function getFailsByDate(start, end, callbackOk, callbackError) {

		var sid = Session.getSessionId();
		var uid = Session.getCurrentSessionUserId();

		$wamp.call('assistance.getFailsByDate', [sid, uid, start, end])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	};

	/*
	 * ----------- NO SE ESTA USANDO ------------------------------------------

	function getFailsByFilter(users, offices, start, end, filter, callbackOk, callbackError) {

		var usersIds = [];
		var officesIds = [];
		var ffilter = {};

		if (users != null && users.length > 0) {
			for (var i = 0; i < users.length; i++) {
				usersIds.push(users[i].id);
			}
		}

		if (offices != null && offices.length > 0) {
			for (var i = 0; i < offices.length; i++) {
				officesIds.push(offices[i].id);
			}
		}

		// chequeo los filtros
		if (filter != null) {
			if (filter.failTypeSelected != null) {
				ffilter.failType = filter.failTypeSelected.name;
			}

			if (filter.periodicitySelected != null) {
				ffilter.periodicity = filter.periodicitySelected;
				if (filter.hoursOperator != null) {
					ffilter.hoursOperator = filter.hoursOperator.value;
					ffilter.hours = filter.hours;
					ffilter.minutes = filter.minutes;
				}
			}

			if (filter.count != null) {
				ffilter.count = filter.count;
			}
		}

		var sid = Session.getSessionId();
		$wamp.call('assistance.getFailsByFilter', [sid, usersIds, officesIds, start, end, ffilter])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});

	}

	*/



	/* ---------------------------------------------------------------------
	 * ------------------------ SCHEDULES ----------------------------------
	 * ---------------------------------------------------------------------
	 */

	function getSchedules(userId, date, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.getSchedules', [sid, userId, date])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	};


	function getSchedulesHistory(userId, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.getSchedulesHistory', [sid, userId])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	};


		/*
		schedule:{
			user_id:"id del Usuario",
			date:"fecha de que se empieza a utilizar el schedule, si no se envia se toma la fecha actual",
			start:"hora de inicio del turno",
			end:"hora de fin de turno",
			daysOfWeek:[],
			isDayOfWeek:"es dia de la semana, si no se envia se toma como false",
			isDayOfMonth:"es dia un dia del mes, si no se envia se toma como false",
			isDayOfYear:"es dia del año, si no se envia se toma como false"
		}
		*/

	function persistSchedule(schedule, callbackOk, callbackError) {
		var sid = Session.getSessionId();

		var params = [sid, schedule.user_id, schedule.date, schedule.start, schedule.end]
		if (schedule.isDayOfWeek) {
				params.push(schedule.isDayOfWeek);
		}

		$wamp.call('assistance.persistSchedule', params)
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	};

	/*
	schedule:{
		user_id:"id del Usuario",
		date:"fecha de que se empieza a utilizar el schedule, si no se envia se toma la fecha actual",
		start:"hora de inicio del turno",
		end:"hora de fin de turno",
		daysOfWeek:[]
	}
	*/

	function persistScheduleWeek(schedule, callbackOk, callbackError) {
		var sid = Session.getSessionId();

		$wamp.call('assistance.persistScheduleWeek', [sid, schedule.user_id, schedule.date, schedule.start, schedule.end, schedule.daysOfWeek])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	};


  function deleteSchedule(id, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.deleteSchedule', [sid, id])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
  };



	/* -----------------------------------------------------------------------
	 * ---------------------------- JUSTIFICATIONS ---------------------------
	 * -----------------------------------------------------------------------
	 */

	function getJustifications(callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.justifications.getJustifications', [sid])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	};


	function getJustificationsByUser(userId, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.justifications.getJustificationsByUser', [sid, userId])
			.then(function(res) {

				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	};


	function getJustificationStock(userId, justificationId, date, period, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		if(!date) date = new Date();

		$wamp.call('assistance.justifications.getJustificationsStockByUser', [sid, userId, justificationId, date, period])
			.then(function(res) {

				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	};

    /**
     * Actualizar stock de la justificacion de un usuario
     * @param {userId} userId
     * @param {justificationId} justificationId
     * @param {stock} stock
     */

	function updateJustificationStock(userId, justificationId, stock, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.justifications.updateJustificationStock', [sid, userId, justificationId, stock])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	};


	function getJustificationRequestsByDate(status, usersIds, start, end, callbackOk, callbackError){
		var sid = Session.getSessionId();
		$wamp.call('assistance.justifications.getJustificationsRequestsByDate', [sid, userIds, start, end, status])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	}


	function getJustificationRequestsToManage(status, group, callbackOk, callbackError){
		var sid = Session.getSessionId();
		$wamp.call('assistance.justifications.getJustificationsRequestsToManage', [sid, status, group])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	}


	function getJustificationRequests(status, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.justifications.getJustificationsRequests', [sid, status])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	}

	function updateJustificationRequestStatus(requestId, status, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.justifications.updateJustificationRequestStatus', [sid, requestId, status])
			.then(function(res) {
				if (res != null) {
					callbackOk(res);
				} else {
					callbackError('Error');
				}
			},function(err) {
				callbackError(err);
			});
	};


	function requestJustification(userId, justification, status, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.justifications.requestJustification', [sid, userId, justification, status])
		.then(function(res) {
			if (res != null) {
				callbackOk(res);
			} else {
				callbackError('Error');
			}
		},function(err) {
			callbackError(err);
		});
	}

	function requestJustificationRange(userId, justificationId, start, end, status, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.justifications.requestJustificationRange', [sid, userId, justificationId, start, end, status])
		.then(function(res) {
			if (res != null) {
				callbackOk(res);
			} else {
				callbackError('Error');
			}
		},function(err) {
			callbackError(err);
		});
	}



	/**
	*	Obtiene las justificaciones especiales que puede solicitar
	*/
	function getSpecialJustifications(callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.justifications.getSpecialJustifications', [sid])
		.then(function(res) {
			if (res != null) {
				callbackOk(res);
			} else {
				callbackError('Error');
			}
		},function(err) {
			callbackError(err);
		});
	};

  /**
   * solicitar justificacion general
   * @param {type} justification Datos de la justificacion
   * @param {type} callbackOk
   * @param {type} callbackError
   * @returns {undefined}
   */
  function requestGeneralJustification(justification, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		var justificationId = justification.id;
		var begin = justification.begin;

		$wamp.call('assistance.justifications.requestGeneralJustification', [sid, justificationId, begin])
		.then(function(res) {
			if (res != null) {
				callbackOk(res);
			} else {
				callbackError('Error');
			}
		},function(err) {
			callbackError(err);
		});
	};

	/**
   * solicitar justificacion general en un rango
   * @param {type} justification Datos de la justificacion
   * @param {type} callbackOk
   * @param {type} callbackError
   * @returns {undefined}
   */
  function requestGeneralJustificationRange(justification, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.justifications.requestGeneralJustificationRange', [sid, justification.id, justification.begin, justification.end])
		.then(function(res) {
			if (res != null) {
				callbackOk(res);
			} else {
				callbackError('Error');
			}
		},function(err) {
			callbackError(err);
		});
	};

	/**
   * solicitar justificaciones generales
   * @param {type} callbackOk
   * @param {type} callbackError
   * @returns {undefined}
   */
  function getGeneralJustificationRequests(callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('assistance.justifications.getGeneralJustificationRequests', [sid])
		.then(function(res) {
			if (res != null) {
				callbackOk(res);
			} else {
				callbackError('Error');
			}
		},function(err) {
			callbackError(err);
		});
  };

  function deleteGeneralJustificationRequest(requestId, callbackOk, callbackError) {
    console.log(requestId);
		var sid = Session.getSessionId();
		$wamp.call('assistance.justifications.deleteGeneralJustificationRequest', [sid, requestId])
		.then(function(res) {
		  console.log(res)
			if (res != null) {
				callbackOk(res);
			} else {
				callbackError('Error');
			}
		},function(err) {
			callbackError(err);
		});
  };


	/* ---------------------------------------------------------------
	 * --------------------------- OVERTIME --------------------------
	 * ---------------------------------------------------------------
	 */

	/**
	 * Obtener solicitudes de horas extra realizadas por el usuario que esta logueado
	 */
	function getOvertimeRequests(status, callbackOk, callbackError){
		var sid = Session.getSessionId();
		$wamp.call('overtime.getOvertimeRequests', [sid, status])
		.then(function(res) {
			if (res != null) {
				callbackOk(res);
			} else {
				callbackError('Error');
			}
		},function(err) {
			callbackError(err);
		});
	};

	/**
	* Obtener solicitudes de horas extra realizadas por el usuario que esta logueado
	*/
	function getOvertimeRequestsToManage(status, group, callbackOk, callbackError){
		var sid = Session.getSessionId();
		$wamp.call('overtime.getOvertimeRequestsToManage', [sid, status, group])
		.then(function(res) {
			if (res != null) {
				callbackOk(res);
			} else {
				callbackError('Error');
			}
		},function(err) {
			callbackError(err);
		});
	};

	/**
	 * Cargar nueva solicitud de horas extra
	 * @param userId id del usuario al cual se solicita la hora extra
	 * @param request Solicitud de hora extra
	 */
	function requestOvertime(requestorId, userId, begin, end, reason, callbackOk, callbackError){

		var sid = Session.getSessionId();
		$wamp.call('overtime.requestOvertime', [sid, requestorId, userId, begin, end, reason])
		.then(function(res) {
			if (res != null) {
				callbackOk(res);
			} else {
				callbackError('Error');
			}
		},function(err) {
			callbackError(err);
		});
	};

	/**
	 * Actualizar estado de solicitud de hora extra
	 * @param requestId Id de la solicitud
	 * @param state Nuevo estado de la solicitud
	 */
	function updateRequestOvertimeStatus(requestId, status, callbackOk, callbackError) {
		var sid = Session.getSessionId();
		$wamp.call('overtime.updateStatus', [sid, requestId, status])
		.then(function(res) {
			if (res != null) {
				callbackOk(res);
			} else {
				callbackError('Error');
			}
		},function(err) {
			callbackError(err);
		});
	}


};
