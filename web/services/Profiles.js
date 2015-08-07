var app = angular.module('mainApp');


app.service('Profiles', function($wamp) {

  this.checkAccess = function(sessionId, profiles, cok, cerr) {
    $wamp.call('systems.profiles.checkProfileAccess', [sessionId, profiles])
      .then(function(res) {
        if (res == null) {
          cerr('');
        } else {
          cok(res);
        }
      }
      ),function(err) {
        cerr(err);
      };
  }

});
