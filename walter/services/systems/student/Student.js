
var app = angular.module('mainApp');

app.service('Student', function(Messages, Utils, Session, Cache) {

  var self = this;
  this.prefix = 'student_'; //prefijo de identificacion de la cache


  /**
   * buscar datos de estudiante
   * @param studentId Id del estudiante. Es el mismo que el id del usuario
   * @param callbackOk
   * @param callbackError
   */
  this.findStudentData = function(studentId,callbackOk,callbackError) {

    //chequear cache para ver si existe el student
    var student = Cache.getItem(self.prefix + studentId);
    if (student != null) {
      callbackOk(student);
      return;
    }

    //si no existe usuario en la cache, enviar mensaje al servidor para consultar estudiante
    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action:'findStudent',
      student: {
        id: studentId
      }
    }

    Messages.send(msg,
		function(response){
			callbackOk(response);
			if(response.student != null){
				Cache.setItem(self.prefix + response.student.id, response.student);
			}
		},

		function(error){
			callbackError(error);
		})
  }


  this.persistStudent = function(student, callbackOk, callbackError){

    //eliminar estudiante de la cache
    Cache.removeItem(self.prefix + student.id);

    var msg = {
      id: Utils.getId(),
      session: Session.getSessionId(),
      action: 'persistStudent',
      student: student
    };

    Messages.send(msg,function(response){
      if (response.error != undefined) {
        callbackError(response.error);
      } else {
        callbackOk(response.ok);
      }
    });
  }

});
