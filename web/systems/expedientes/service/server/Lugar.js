
app.service("Lugar", ["$wamp", function($wamp) {
  this.findById = function(id) {
    return $wamp.call('expedientes.lugar.findById', [id])
  }

  this.gridData = function(filterParams) {
    return $wamp.call('expedientes.lugar.gridData', [filterParams])
  }

  this.numRows = function(search) {
    return $wamp.call('expedientes.lugar.numRows', [search])
  }


}]);