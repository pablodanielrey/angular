var app = angular.module('mainApp');

app.controller('LibraryCtrl', ["$rootScope", '$scope',
  function ($rootScope, $scope) {
    console.log("LibraryCtrl");

    var nombres = ['Walter Roberto', 'Pablo Daniel', 'Alejandro Agustin', 'Maximiliano Antonio', 'Ivan Roberto'];
    var dnis = ['2738457298', '27294557', '30001823', '12345678', '876554432'];
    var cclase = '';

    $scope.logs = [];
    for (var i = 0; i < 100; i++) {
      if (i % 2 == 0) {
        cclase = 'entrada';
      } else {
        cclase = 'salida';
      };

      $scope.logs.push(
        {
          clase: cclase,
          tipo: 'NoDocente',
          name: nombres[i % nombres.length],
          lastname: 'Blanco',
          dni: dnis[i % dnis.length],
          hora: '10:30 am',
          dia: '05/08/2026'
        }
      );
    };

    /*
      repetir solooooo

      $scope.variable = [];
      for (var i = 0; i < cantidad; i++) {
        $scope.variable.push('valor a agregar');
      }

      y en el html usar:

      ng-repeat='i in variable'

    */


    /*

      la lista inicial va entre []
      los valores internos a la lista van entre {}
      se separan usando ,
      acordarse al final de la lista poner ;
      ej:

      $scope.variable = [

        {
            hora:'sdfdsf',
            nombre:'sdfdsf',
            dni:'sdfdsf',
            lastname:'sdfdsf',
            tipo:'sdf',
            clase:'sdf'
        },

        {
            hora:'sdfdsf',
            nombre:'sdfdsf',
            dni:'sdfdsf',
            lastname:'sdfdsf',
            tipo:'sdf',
            clase:'sdf'
        },

        {
            hora:'sdfdsf',
            nombre:'sdfdsf',
            dni:'sdfdsf',
            lastname:'sdfdsf',
            tipo:'sdf',
            clase:'sdf'
        },

        {
            hora:'sdfdsf',
            nombre:'sdfdsf',
            dni:'sdfdsf',
            lastname:'sdfdsf',
            tipo:'sdf',
            clase:'sdf'
        },

        {
            hora:'sdfdsf',
            nombre:'sdfdsf',
            dni:'sdfdsf',
            lastname:'sdfdsf',
            tipo:'sdf',
            clase:'sdf'
        },

        {
            hora:'sdfdsf',
            nombre:'sdfdsf',
            dni:'sdfdsf',
            lastname:'sdfdsf',
            tipo:'sdf',
            clase:'sdf'
        },

        {
            hora:'sdfdsf',
            nombre:'sdfdsf',
            dni:'sdfdsf',
            lastname:'sdfdsf',
            tipo:'sdf',
            clase:'sdf'
        }

    ];

    */



  }
]);
