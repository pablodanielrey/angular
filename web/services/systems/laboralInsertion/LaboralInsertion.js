
angular
  .module('mainApp')
  .service('LaboralInsertion',LaboralInsertion);

LaboralInsertion.inject = ['$rootScope','$wamp','Session']

function LaboralInsertion($rootScope,$wamp,Session) {

  /*
  */
  this.findAllInscriptions = function(filters) {
    return $wamp.call('system.laboralInsertion.findAllInscriptions',[filters]);
  }

  this.getFilters = function() {
    return $wamp.call('system.laboralInsertion.getFilters');
  }

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
    Elimina una escripcion dado el id.
  */
  this.deleteInscriptionById = function(iid) {
    return $wamp.call('system.laboralInsertion.deleteInscriptionById', [iid]);
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

  /*
    envía un mail a la empresa con los usuarios seleccionados.
  */
  this.sendEmailToCompany = function(inscriptions, company) {
    return $wamp.call('system.laboralInsertion.sendEmailToCompany', [inscriptions, company])
  }

  /*
    encuentra todas las companies definidas en la base de datos.
  */
  this.findAllCompanies = function() {
    return $wamp.call('system.laboralInsertion.company.findAll')
  }

  /*
    encuentra todos los sent que tengan el id de incripcion
  */
  this.findSentByInscriptionId = function(id) {
    return $wamp.call('system.laboralInsertion.sent.findByInscription', [id]).then(function(sents) {
      return {'id':id, 'sents':sents};
    })
  }



}
