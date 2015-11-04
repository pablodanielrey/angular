
angular
  .module('mainApp')
  .service('LaboralInsertion',LaboralInsertion);

LaboralInsertion.inject = ['$rootScope','$wamp','Session']

function LaboralInsertion($rootScope,$wamp,Session) {

  /**
    obtiene todas las inscripciones de un usuario determinado
  */
  this.findAllInscriptionsByUser = function(userId) {
    return $wamp.call('system.laboralInsertion.findAllInscriptionsByUser', [userId]);
  }

  /*
    crea una nueva inscripción a la bosla para el usuario determinado
  */
  this.persistInscriptionByUser = function(userId, data) {
    return $wamp.call('system.laboralInsertion.persistInscriptionByUser', [userId, data]);
  }


  /*
    Encuentra todos los datos de insercion laboral independientes de las inscripciones en la bolsa que tenga el usuario.
  */
  this.findByUser = function(userId) {
    return $wamp.call('system.laboralInsertion.findByUser',[userId]);
  }

  /*
    persiste los datos de insercion laboral genericos. esto no incluye las inscripcinoes a la bolsa.
  */
  this.persist = function(data) {
    return $wamp.call('system.laboralInsertion.persist',[data]);
  }

}
