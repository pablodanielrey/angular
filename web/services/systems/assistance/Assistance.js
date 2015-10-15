var app = angular.module('mainApp');

app.service('Assistance', ['Utils','Session','$wamp',

	function(Utils, Session, $wamp) {

		this.getAssistanceData = function(userId, date, callbackOk, callbackError) {
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

		this.getAssistanceStatusByDate = function(userId, date, callbackOk, callbackError) {
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




		this.getFailsByDate = function(start, end, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			var uid = Session.getCurrentSessionUserId();
      console.log(sid)
      console.log(uid)
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

		this.getFailsByFilter = function (users, offices, start, end, filter, callbackOk, callbackError) {

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



		this.getAssistanceStatusByUsers = function(usersIds, dates, status, callbackOk, callbackError) {
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




		this.getSchedules = function(userId, date, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.getSchedules', [sid, usersId, date])
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

		this.persistSchedule = function(schedule, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.persistSchedule', [sid, schedule])
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


    this.deleteSchedule = function(id, callbackOk, callbackError) {
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




		this.getJustifications = function(callbackOk, callbackError) {
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

		this.getJustificationsByUser = function(userId, callbackOk, callbackError) {
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


		this.getJustificationStock = function(userId, justificationId, date, period, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.justifications.getJustificationsStock', [sid, userId, justificationId, date, period])
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
    this.updateJustificationStock = function(userId, justificationId, stock, callbackOk, callbackError) {
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

		this.getJustificationRequestsByDate = function(status, usersIds, start, end, callbackOk, callbackError){
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

		this.getJustificationRequestsToManage = function(status, group, callbackOk, callbackError){
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


		this.getJustificationRequests = function(status, callbackOk, callbackError){
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


		this.updateJustificationRequestStatus = function(requestId, status, callbackOk, callbackError) {
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

		this.requestJustification = function(userId, justification, status, callbackOk, callbackError) {
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

		this.requestJustificationRange = function(userId, justificationId, start, end, status, callbackOk, callbackError) {
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
		 * Obtener solicitudes de horas extra realizadas por el usuario que esta logueado
		 */
		this.getOvertimeRequests = function(status, callbackOk, callbackError){
			var sid = Session.getSessionId();
			$wamp.call('assistance.overtime.getRequests', [sid, status])
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
		this.getOvertimeRequestsToManage = function(status, group, callbackOk, callbackError){
			var sid = Session.getSessionId();
			$wamp.call('assistance.overtime.getRequestsToManage', [sid, status, group])
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
		this.requestOvertime = function(userId, request, callbackOk, callbackError){
			var sid = Session.getSessionId();
			$wamp.call('assistance.overtime.requestOvertime', [sid, userId, request])
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
		this.updateRequestOvertimeStatus = function(requestId, status, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.overtime.persistStatus', [sid, requestId, status])
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
		this.getSpecialJustifications = function(callbackOk, callbackError) {
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
    this.requestGeneralJustification = function(justification, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.justifications.requestGeneralJustification', [sid, justification])
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
    this.requestGeneralJustificationRange = function(justification, callbackOk, callbackError) {
			var sid = Session.getSessionId();
			$wamp.call('assistance.justifications.requestGeneralJustificationRange', [sid, justification])
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
    this.getGeneralJustificationRequests = function(callbackOk, callbackError){
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

    this.deleteGeneralJustificationRequest = function(requestId, callbackOk, callbackError){
			var sid = Session.getSessionId();
			$wamp.call('assistance.justifications.deleteGeneralJustificationRequest', [sid, requestId])
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






}]);
