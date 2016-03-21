angular
  .module('mainApp')
  .service('Tutors',Tutors);

Tutors.ineject = ['$wamp','Session'];

function Tutors($wamp, Session) {

  /*
    PARTE NUEVA, LA REIMPLEMENTACIÓN.
    DEJO LOS OTROS METODOS PARA TENER UNA REFERENCIA PERO HAY QUE PASARLOS A PROMESAS Y
    VER SI EL TEMA DEL CACHE ESTA OK. CREO QUE NO POR AHORA.

    wamp ya retorna promesas.
  */

  this.search = function(regex) {
    return $wamp.call('users.search', [regex]);
  }

  this.loadTutorings = function() {
    var sid = Session.getSessionId();
    return $wamp.call('tutors.loadTutorings',[sid]);
  }

  this.persist = function(tutoring) {
    return $wamp.call('tutors.persist',[tutoring]);
  }

}
