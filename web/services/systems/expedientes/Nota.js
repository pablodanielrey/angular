
app.service("Nota", ["$wamp", function($wamp) {
  this.findById = function(id) {
    return $wamp.call('expedientes.nota.findById', [id])
  }

  this.gridData = function(search, pageSize, pageNumber) {
    return $wamp.call('expedientes.nota.gridData', [search, pageSize, pageNumber])
  }

  this.numRows = function(search) {
    return $wamp.call('expedientes.nota.numRows', [search])
  }


}]);