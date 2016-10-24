(function() {
    'use strict';

    angular
        .module('assistance')
        .service('AssistanceUtils', AssistanceUtils);

    AssistanceUtils.$inject = ['$window', '$filter'];

    /* @ngInject */
    function AssistanceUtils($window, $filter) {
        this.sort = sort;
        this.clearSort = clearSort;
        this.clearReverse = clearReverse;
        this.processSortRev = processSortRev;
        /*
        Dispara la ordenación del listado.
        list: lista a ordenar
        key: nombre del elemento en la cache
        order: campos a ordenar
        comparator: comparador(debe estar implentado en este service)
        */
        function sort(list, key, orderValue, comparator) {
          var keyComp = key + 'Comparator';
          var order = $window.sessionStorage.getItem(key);
          if (order == null) {
            order = orderValue;
            $window.sessionStorage.setItem(key, JSON.stringify(order));
            $window.sessionStorage.removeItem(keyComp);
          } else {
            order = JSON.parse(order);
          }

          var comp = $window.sessionStorage.getItem(keyComp);
          if (comp == null) {
            comp = comparator;
            $window.sessionStorage.setItem(keyComp, comp);
          }

          list = (comp == null) ?  $filter('orderBy')(list, order, false) : $filter('orderBy')(list, order, false, eval(comp));
          return list
        }

        /*
          retorna el valor de orden inverso o order normal. y almacena el inverso.
          solo se usa cuando se clickea el ordenamiento explícitamente.
          no cuando se ordena el listado.
        */
        function processSortRev(key) {
          var rev = $window.sessionStorage.getItem(key);
          if (rev == null) {
            rev = false;
            $window.sessionStorage.setItem(key, JSON.stringify(!rev));
          } else {
            rev = JSON.parse(rev);
          }

          // almaceno el orden a inverso.
          if (rev) {
            $window.sessionStorage.setItem(key, JSON.stringify(!rev));
          } else {
            $window.sessionStorage.setItem(key, JSON.stringify(!rev));
          }

          return rev;
        }

        /*
        elimina los valores de la cache
        */
        function clearSort(key) {
          var keyComp = key + 'Comparator';
          $window.sessionStorage.removeItem(keyComp);
          $window.sessionStorage.removeItem(key);
        }

        function clearReverse(reverse) {
          $window.sessionStorage.removeItem(reverse);          
        }

        /*
         En caso de que sea string utiliza el localeCompare, para que ordene correctamente los acentos
        */
        function localeSensitiveComparator(v1, v2) {
          if (v1.type === 'number' && v2.type === 'number') {
            return (v1.value < v2.value) ? -1 : (v1.value == v2.value) ? 0 : 1;
          }

          if (v1.value == undefined || v2.value == undefined) {
            return (v1.value == undefined) ? -1 : 1;
          }

          if (v1.type !== 'string' || v2.type !== 'string') {
            return (v1.value < v2.value) ? -1 : (v1.value == v2.value) ? 0 : 1;
          }

          // Compare strings alphabetically, taking locale into account
          return v1.value.localeCompare(v2.value);
        };

        /*
         Esta comparacion tiene en cuenta la longitud del string
        */
        function dniComparator(v1, v2) {
          // If we don't get strings, just compare by index
          if (v1.type !== 'string' || v2.type !== 'string') {
            return (v1.index < v2.index) ? -1 : (v1.index == v2.index) ? 0 : 1;
          }

          return (v1.value.length == v2.value.length) ? v1.value.localeCompare(v2.value) : (v1.value.length < v2.value.length) ? -1 : 1;
        };

        /*
         Compara por el dia de la semana
        */
        function dayComparator(v1, v2) {
          if (v1.type === 'object' && !isNaN(v1.value) && v2.type === 'object' && !isNaN(v2.value)) {
            var d1 = new Date(v1.value).getDay();
            var d2 = new Date(v2.value).getDay();
            return (d1 < d2) ? -1 : (d1 == d2) ? 0 : 1;
          }

          if (v1.value == "null" || v2.value == 'null') {
            return (v1.value == "null") ? -1 : 1;
          }

          return localeSensitiveComparator(v1, v2)
        };
    }
})();
