
app.service("Destino", ["$wamp", function($wamp) {
  this.findById = function(id) {
    return $wamp.call('expedientes.destino.findById', [id])
  }

  this.gridData = function(search, pageSize, pageNumber) {
    return $wamp.call('expedientes.destino.gridData', [search, pageSize, pageNumber])
  }

  this.numRows = function(search) {
    return $wamp.call('expedientes.destino.numRows', [search])
  }


}]);