angular
  .module('mainApp')
  .service('Tutors',Tutors);

Tutors.ineject = ['$wamp','Login'];

function Tutors($wamp, Login) {

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
    return new Promise(function(cok, cerr) {
      Login.getSessionData()
        .then(function(s) {
          var tutorId = s.user_id;
          $wamp.call('tutors.findByTutorId',[tutorId])
            .then(function(tutorings) {
                for (var i = 0; i < tutorings.length; i++) {
                  tutorings[i].date = new Date(tutorings[i].date);
                }

                // debo ordenarlas por fecha.
                tutorings.sort(function(a, b) {
                  return a.date - b.date;
                })

                cok(tutorings);
              },function(err) {
                cerr(err);
              });
        }, function(err) {
          cerr(err);
        });
    });
  }

  this.persist = function(tutoring) {
    return $wamp.call('tutors.persist', [tutoring]);
  }

  this.delete = function(tid) {
    return $wamp.call('tutors.delete', [tid]);
  }

}
