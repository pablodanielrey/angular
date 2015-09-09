angular
    .module('mainApp')
    .controller('RecordController',RecordController);

RecordController.$inject = ['$scope','$timeout','$sce'];

function RecordController($scope,$timeout,$sce) {

    $scope.model = {
      recordings:[],
      listRecordings:[],
      selecteds: [],
      video: null,
      rate: 1
    };

    $scope.view = {
        style: '',
        selecAll: false,
        paused: false,
        displayListRecordings: false,
        styles:['','reproductor']
    };


/* ---------------------------------------------------------------
 * ------------------- MANEJO DE LA VISTA ------------------------
 * ---------------------------------------------------------------
 */

    $scope.initialize = initialize;
    $scope.setStyle = setStyle;

    function initialize() {
      $scope.view.displayListRecordings = false;
      $scope.view.selectAll = false;
      $scope.model.recordings = [];
      $scope.model.listRecordings = [];
      $scope.model.selecteds = [];
      $scope.model.video = null;
    }

    function setStyle(index) {
      $scope.view.style = $scope.view.styles[index];
    }




/* ---------------------------------------------------------------
 * ---------------------- EVENTOS --------------------------------
 * ---------------------------------------------------------------
 */

    $scope.$on('$viewContentLoaded', function(event) {
     $scope.initialize();
    });

    $scope.$on('$viewRecordings', function(event) {
      $scope.view.displayListRecordings = false;
    });


/* ---------------------------------------------------------------
 * ---------------------- BUSQUEDA -------------------------------
 * ---------------------------------------------------------------
 */
    $scope.search = search;

    function search() {
      var r1 = {'displayName':'1 - Planta Baja','selected':false,'start':new Date(),'duration':'01:25:13','size':'45 Mb','fileName':'2015-07-31_23-00-02','src':'http://163.10.56.194/gluster/camaras/archivo/2015-08-18_09-00-01_camara1.m4v.mp4'}
      var r2 = {'displayName':'2 - 1er piso','selected':false,'start':new Date(),'duration':'01:00:13','size':'35 Mb','fileName':'2015-07-30_23-00-02','src':'http://163.10.56.194/gluster/camaras/archivo/2015-08-18_09-00-01_camara1.m4v.mp4'}
      $scope.model.recordings = [r1,r2]
      $scope.view.displayListRecordings = true;
    }



/* ---------------------------------------------------------------
 * ------------- Acciones sobre el listado de videos -------------
 * ---------------------------------------------------------------
 */
    $scope.selectRecording = selectRecording;
    $scope.viewRecording = viewRecording;
    $scope.downloadRecording = downloadRecording;
    $scope.viewSelecteds = viewSelecteds;
    $scope.selectAll = selectAll;

    function selectRecording(recording) {
      $scope.view.selectAll = false;
      var index = $scope.model.selecteds.indexOf(recording);
      if (recording.selected) {
        if (index == -1) {
          $scope.model.selecteds.push(recording);
          if ($scope.model.selecteds.length == $scope.model.recordings.length) {
            $scope.view.selectAll = true;
          }
        }
      } else {
        if (index != -1) {
          $scope.model.selecteds.splice(index, 1);
        }
      }
    }

    function selectAll() {
      if ($scope.view.selectAll) {
        $scope.model.selecteds = $scope.model.recordings.slice();
      } else {
        $scope.model.selecteds = [];
      }
      for (var i = 0; i < $scope.model.recordings.length; i++) {
        $scope.model.recordings[i]['selected'] = $scope.view.selectAll;
      }
    }

    function viewRecording(recording) {
      $scope.displayReproductor([recording]);
    }

    function downloadRecording(recording) {

    }

    function viewSelecteds() {
      $scope.displayReproductor($scope.model.selecteds);
    }


/* ---------------------------------------------------------------
 * --------------------- REPRODUCTOR -----------------------------
 * ---------------------------------------------------------------
 */
    $scope.displayReproductor = displayReproductor;
    $scope.closeReproductor = closeReproductor;
    $scope.selectVideo = selectVideo;
    $scope.pause = pause;
    $scope.play = play;
    $scope.faster = faster;
    $scope.slower = slower;
    $scope.seekForward = seekForward;
    $scope.seekBackwards = seekBackwards;
    $scope.next = next;
    $scope.previous = previous;

    function displayReproductor(items) {
      $scope.setStyle(1);
      $scope.model.listRecordings = items;
      $scope.view.paused = false;
      var video = document.getElementById("video");
      video.addEventListener("pause", pauseEvent, true);
      video.addEventListener("play", playEvent, true);

      if (items.length > 0) {
        $scope.selectVideo(items[0]);
      } else {
        $scope.model.video = null;
        video.src = "";
      }
    }

    function selectVideo(recording) {
      $scope.model.video = recording;
      var video = document.getElementById("video");
      video.src = $scope.model.video.src;
    }

    function pauseEvent() {
      $scope.view.paused = true;
    }

    function playEvent() {
      $scope.view.paused = false;
    }

    function closeReproductor() {
      $scope.setStyle(0);
      $scope.model.listRecordings = [];
    }

    $scope.$watch('view.paused', function(newValue, oldValue) {
      if (newValue) {
        $scope.model.rate = 1;
        var video = document.getElementById("video");
        video.playbackRate = $scope.model.rate;
      }
    });


    function pause() {
      var video = document.getElementById("video");
      video.pause();
    }

    function play() {
      var video = document.getElementById("video");
      video.play();
    }

    function faster() {
      $scope.model.rate = $scope.model.rate + 0.5;
      var video = document.getElementById("video");
      video.playbackRate = $scope.model.rate;
      $scope.view.paused = false;

      if ($scope.model.rate > 0) {
        video.play();
      }
    }


    function slower() {
      $scope.view.paused = false;
      var video = document.getElementById("video");
      $scope.model.rate = $scope.model.rate - 0.5;

      if ($scope.model.rate < 0) {
        $scope.model.rate = 0;
        video.pause();
      }

      video.playbackRate = $scope.model.rate;
    }

    function seekForward() {
      $scope.model.rate = 1;
      var video = document.getElementById("video");
      video.currentTime = video.currentTime + 1;
      video.playbackRate = $scope.model.rate;
      video.pause();
    }

    function seekBackwards() {
      $scope.model.rate = 1;
      var video = document.getElementById("video");
      video.currentTime = video.currentTime - 1;
      video.playbackRate = $scope.model.rate;
      video.pause();
    }

    function next() {
      var index = $scope.model.listRecordings.indexOf($scope.model.video);
      if (index == -1 || index == ($scope.model.listRecordings.length - 1)) {
        return;
      }
      $scope.selectVideo($scope.model.listRecordings[index+1]);
    }

    function previous() {
      var index = $scope.model.listRecordings.indexOf($scope.model.video);
      if (index <= 0) {
        return;
      }
      $scope.selectVideo($scope.model.listRecordings[index-1]);
    }

}
