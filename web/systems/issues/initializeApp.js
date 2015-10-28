
var app = angular
    .module('mainApp',['ngRoute','vxWamp','ui.tree'])
    .config(function($wampProvider) {
      if (config.url == undefined || config.url == 'autodetect') {
        var conn = {
          url: "ws://" + location.host + ":8000/ws",
          realm: config.realm
        };
        console.log(conn);
        $wampProvider.init(conn);
      } else {
        var conn = {
          url: config.url,
          realm: config.realm
        };
        console.log(conn);
        $wampProvider.init(conn);
      }
    })
    .run(function($wamp) {
      $wamp.open();
    });
