
app.service("Tema", ["$wamp", function($wamp) {
  this.findById = function(id) {
    return $wamp.call('expedientes.tema.findById', [id])
  }

  this.gridData = function(search, pageSize, pageNumber) {
    return $wamp.call('expedientes.tema.gridData', [search, pageSize, pageNumber])
  }

  this.numRows = function(search) {
    return $wamp.call('expedientes.tema.numRows', [search])
  }


}]);