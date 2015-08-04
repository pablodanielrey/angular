angular
    .module('mainApp',['ngRoute','vxWamp'])
    .config(function($wampProvider) {

      if (config_firmware.url == undefined || config_firmware.url == 'autodetect') {
        var conn = {
          url: "ws://" + location.host + "/ws",
          realm: config_firmware.realm
        };
        console.log(conn);
        $wampProvider.init(conn);
      } else {
        var conn = {
          url: config_firmware.url,
          realm: config_firmware.realm
        };
        console.log(conn);
        $wampProvider.init(conn);
      }
    });
    /*
    .run(function($wamp) {
      $wamp.open();
    });
    */
