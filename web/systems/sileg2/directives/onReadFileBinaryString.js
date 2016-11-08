(function() {
    'use strict';

    angular
        .module('issues')
        .directive('eOnReadFileBinaryString', eOnReadFileBinaryString);

		eOnReadFileBinaryString.$inject = ['$parse']

    function eOnReadFileBinaryString($parse) {
        var directive = {
            restrict: 'A',
            link: linkFunc
        };

        return directive;

        function linkFunc(scope, element, attrs) {
					var fn = $parse(attrs.eOnReadFileBinaryString);

					element.on('change', function(onChangeEvent) {

						var reader = new FileReader();
						var src = (onChangeEvent.srcElement || onChangeEvent.target);
						var file = src.files[0];

						reader.fileName = file.name;
						reader.fileType = file.type;
						reader.fileSize = file.size;
						//reader.fileLastModified = file.lastModified;

						reader.onload = function(onLoadEvent) {
							scope.$apply(function() {
								fn(scope, {
									fileName: onLoadEvent.target.fileName,
									fileType: onLoadEvent.target.fileType,
									fileSize: onLoadEvent.target.fileSize,
									//fileLastModified: onLoadEvent.target.fileLastModified,
									fileContent:onLoadEvent.target.result
								});
							});
						};

						reader.readAsBinaryString(file);

					});
				}
    }

})();
