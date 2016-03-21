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
    return new Promise(function(cok, cerr) {
      $wamp.call('users.search', [regex])
      .then(function(users) {
        for (var i = 0; i < users.length; i++) {
          if (users[i]['user'].genre == 'Femenino') {
            users[i]['user'].img='img/avatarWoman.jpg';
          } else {
            users[i]['user'].img='img/avatarMen.jpg';
          }
        }
        cok(users);
      }, function(err) {
        cerr(err);
      });
    });
  }

  this.loadTutorings = function() {
    var sid = Session.getSessionId();
    return $wamp.call('tutors.loadTutorings',[sid]);
  }

  this.persist = function(tutoring) {
    return new Promise(function(cok, cerr) {
      var t = JSON.parse(JSON.stringify(tutoring));
      t.id = '';
      cok(t);
    });
    //return $wamp.call('tutors.persist',[tutoring]);
  }

}
