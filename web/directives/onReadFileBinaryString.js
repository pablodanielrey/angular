var app = angular.module('mainApp');

app.directive('onReadFileBinaryString', function ($parse) {
	return {
		restrict: 'A',
		scope: false,
		link: function(scope, element, attrs) {
            var fn = $parse(attrs.onReadFileBinaryString);

						element.on('change', function(onChangeEvent) {

							var reader = new FileReader();
							var src = (onChangeEvent.srcElement || onChangeEvent.target);
							var file = src.files[0];

							reader.fileName = file.name;
							reader.onload = function(onLoadEvent) {
								scope.$apply(function() {
									fn(scope, {fileName:onLoadEvent.target.fileName,fileContent:onLoadEvent.target.result});
								});
							};

							reader.readAsBinaryString(file);

						});
					}
			};
});
