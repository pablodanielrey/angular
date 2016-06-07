
var app = angular.module('mainApp');

app.service('Student', function($wamp) {

  var self = this;
  this.prefix = 'student_'; //prefijo de identificacion de la cache

  this.findById = function(userId) {
    return $wamp.call('system.students.findById', [userId]);
  }

  this.persist = function(userId, sn) {
    var student = {
      id: userId,
      studentNumber: sn,
      condition: 'regular'
    };
    return $wamp.call('system.students.persist', [student]);
  }

});
