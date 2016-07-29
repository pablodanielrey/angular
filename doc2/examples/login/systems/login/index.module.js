angular
    .module('login',['ngRoute','vxWamp'])
    .config(function($wampProvider) {
      /*
      if (config.url == undefined || config.url == 'autodetect') {

        var conn = {
          url: "ws://" + location.host + ":443/ws",
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
      }*/

      var conn = {
        url: "ws://" + location.hostname + ":8080",
        realm: "core",
        authmethods: ["ticket"]
      };
      $wampProvider.init(conn);

    });
