angular
  .module('mainApp')
  .service('Camaras',Camaras);

Camaras.inject = ['$rootScope','$wamp','Session'];

function Camaras($rootScope,$wamp,Session) {

  this.findAllCamaras = findAllCamaras;
  this.findRecordings = findRecordings;

  function findAllCamaras(callbackOk,callbackError) {
    callbackOk([]);
  }

  function findRecordings(start,end,camaras,callbackOk,callbackError) {
    var r1 = {
      'displayName':'1 - Planta Baja',
      'start':new Date(),
      'duration':'01:25:13',
      'size':'45 Mb',
      'fileName':'2015-07-31_23-00-02',
      'src':'http://163.10.56.194/gluster/camaras/archivo/2015-08-18_09-00-01_camara1.m4v.mp4'
    };

    var r2 = {
      'displayName':'2 - 2do piso',
      'start':new Date(),
      'duration':'01:00:13',
      'size':'35 Mb',
      'fileName':'2015-07-30_23-00-02',
      'src':'http://163.10.56.194/gluster/camaras/archivo/2015-08-18_09-00-01_camara1.m4v.mp4'
    };

    recordings = [r1,r2];
    callbackOk(recordings);
  }
}
