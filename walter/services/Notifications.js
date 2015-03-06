
var app = angular.module('mainApp');


app.service('Notifications',function($rootScope) {

  this.message = function(data) {

    var message = { };
    if (typeof data === 'string') {
      message = {messages:[data], callback:null};
    } else {
      message = {messages:data, callback:null};
    }

    $rootScope.$broadcast('ShowMessageEvent',message);
  }

  this.messageWithCallback = function(data,callback) {

    var message = { };
    if (typeof data === 'string') {
      message = {messages:[data], callback:callback};
    } else {
      message = {messages:data, callback:callback};
    }

    $rootScope.$broadcast('ShowMessageEvent',message);
  }

});
