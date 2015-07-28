angular
    .module('mainApp',['ngRoute','vxWamp'])
    .config(function($wampProvider) {
      var conn = {
        url: config_firmware.url,
        realm: config_firmware.realm
      };
      console.log(conn);
      $wampProvider.init(conn);
    });
    /*
    .run(function($wamp) {
      $wamp.open();
    });
    */
