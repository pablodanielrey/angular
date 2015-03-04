var app = angular.module('mainApp');

app.directive('onReadFileBinaryString', function ($parse) {
	return {
		restrict: 'A',
		scope: false,
		link: function(scope, element, attrs) {
            var fn = $parse(attrs.onReadFileBinaryString);
            
			element.on('change', function(onChangeEvent) {
				var reader = new FileReader();
                
				reader.onload = function(onLoadEvent) {
					scope.$apply(function() {
						fn(scope, {$fileContent:onLoadEvent.target.result});
					});
				};

				reader.readAsBinaryString((onChangeEvent.srcElement || onChangeEvent.target).files[0]);
			});
		}
	};
});
