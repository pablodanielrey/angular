angular
    .module('mainApp')
    .controller('RecordController',RecordController);

RecordController.$inject = ['$scope','$timeout','$filter','$sce','Camaras'];

function RecordController($scope,$timeout,$filter,$sce,Camaras) {

    $scope.model = {
      recordings:[],
      listRecordings:[],
      selecteds: [],
      video: null,
      camaras: [],
      filter: {
        start: null,
        end: null,
        camaras: []
      },
      rate: 1
    };

    $scope.view = {
        style: '',
        selecAll: false,
        paused: false,
        displayListRecordings: false,
        styles:['','reproductor','displayFilterCamera'],
        reverseCamera:false,
        reverseDate:false,
        reverseHour:false,
        reverseDuration:false,
        reverseSize:false
    };



/* ---------------------------------------------------------------
 * ------------------- MANEJO DE LA VISTA ------------------------
 * ---------------------------------------------------------------
 */

    $scope.initialize = initialize;
    $scope.initializeCamaras = initializeCamaras;
    $scope.setStyle = setStyle;
    $scope.viewFilterCamera = viewFilterCamera;
    $scope.selectCamara = selectCamara;
    $scope.order = order;
    $scope.orderByHour = orderByHour;

    function initialize() {
      $scope.view.displayListRecordings = false;
      $scope.view.selectAll = false;
      $scope.model.recordings = [];
      $scope.model.listRecordings = [];
      $scope.model.selecteds = [];
      $scope.model.video = null;
      $scope.model.filter = {};
      $scope.model.filter.start = new Date();
      $scope.model.filter.end = new Date();
      $scope.initializeCamaras();

      $scope.view.reverseCamera = false;
      $scope.view.reverseDate = false;
      $scope.view.reverseHour = false;
      $scope.view.reverseDuration = false;
      $scope.view.reverseSize = false;
    }

    function initializeCamaras() {
      $scope.model.filter.camaras = [];
      Camaras.findAllCamaras(
        function(camaras) {
          $scope.model.camaras = camaras;
          for (var i = 0; i < camaras.length; i++) {
            camaras[i].selected = false;
          }
        },
        function(error){
          Notifications.message(error);
        }
      );
    }

    function selectCamara(camara) {
      if (camara.selected) {
        $scope.model.filter.camaras.push(camara.id);
      } else {
        var index = $scope.model.filter.camaras.indexOf(camara['id']);
        if (index > -1) {
          $scope.model.filter.camaras.splice(index,1);
        }
      }
    }

    function setStyle(index) {
      $scope.view.style = $scope.view.styles[index];
    }

    function viewFilterCamera() {
      if ($scope.view.style == $scope.view.styles[2]) {
        $scope.setStyle(0);
      } else {
        $scope.setStyle(2);
      }
    }

    function order(predicate, reverse) {
      $scope.model.recordings = $filter('orderBy')($scope.model.recordings, predicate, reverse);
    }

    function orderByHour(reverse) {
      var recordings = $scope.model.recordings;
      for (var i = 0; i < recordings.length; i++) {
        for (var j = i; j < recordings.length; j++) {
          var rec = recordings[i];
          var recDate = new Date(rec['start']);
          var minRec = (recDate.getHours() * 60) + recDate.getMinutes();

          var auxDate = new Date(recordings[j]['start']);
          var minAux = (auxDate.getHours() * 60) + auxDate.getMinutes();

          if (reverse && minAux > minRec) {
            recordings[i] = recordings[j];
            recordings[j] = rec;
          }
          if (!reverse && minAux < minRec) {
            recordings[i] = recordings[j];
            recordings[j] = rec;
          }
        }
      }
    }


    $scope.$watch('model.filter.start', function(newValue, oldValue) {
      $scope.model.filter.start.setSeconds(0);
      $scope.model.filter.start.setMilliseconds(0);
    });

    $scope.$watch('model.filter.end', function(newValue, oldValue) {
      $scope.model.filter.end.setSeconds(0);
      $scope.model.filter.end.setMilliseconds(0);
    });

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
      Camaras.findRecordings($scope.model.filter.start,$scope.model.filter.end,$scope.model.filter.camaras,
        function(recordings) {
          $scope.model.recordings = recordings;
          for (var i = 0; i < recordings.length; i++) {
            $scope.model.recordings[i].selected = false;
          }
          $scope.view.displayListRecordings = true;
          $scope.order(['start','camera.floor','camera.number'],$scope.view.reverseCamera);
        },
        function(error) {
          $scope.model.recordings = [];
          Notifications.message(error);
        }
      );
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

      video.addEventListener("pause", function() {
        $scope.$apply(function() {$scope.view.paused = true;});
      });

      video.addEventListener("play", function() {
        $scope.$apply(function() {$scope.view.paused = false;});
      });

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

    $scope.$watch('view.paused', function(newValue, oldValue) {
      $scope.model.rate = 1;
      var video = document.getElementById("video");
      video.playbackRate = $scope.model.rate;
    });

    function closeReproductor() {
      $scope.setStyle(0);
      $scope.model.listRecordings = [];
    }

    function pause() {
      var video = document.getElementById("video");
      video.pause();
      $scope.view.paused = true;
    }

    function play() {
      var video = document.getElementById("video");
      video.play();
      $scope.view.paused = false;
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
