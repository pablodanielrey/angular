
app.service("Tema", ["$wamp", function($wamp) {
  this.findById = function(id) {
    return $wamp.call('expedientes.tema.findById', [id])
  }

  this.gridData = function(filterParams) {
    return $wamp.call('expedientes.tema.gridData', [filterParams])
  }

  this.numRows = function(search) {
    return $wamp.call('expedientes.tema.numRows', [search])
  }


}]);