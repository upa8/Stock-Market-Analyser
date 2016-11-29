function stockController($scope,$rootScope,$location,$http,$websocket) {
	console.log("Home controller");
	  $scope.isWorking = "Yes, it is working";

	  //var dataStream = $websocket('ws://echo.websocket.org/');
	  var dataStream = $websocket('ws://127.0.0.1:9000/ws');

      var collection = [];

      dataStream.onMessage(function(message) {
      	console.log("Recieved message "+ message.data);
        collection.push(JSON.parse(message.data));
      });

      var methods = {
        collection: collection,
        get: function() {
          dataStream.send(JSON.stringify({ action: 'get' }));
        }
      };

      dataStream.onOpen(function() {
	    console.log('connection open');
	    dataStream.send('Hello World');
	    dataStream.send('again');
	    dataStream.send('and again');
	  });

	  dataStream.onError(function(event) {
	    console.log('connection Error', event);
	  });

	  dataStream.onClose(function(event) {
	    console.log('connection closed', event);
	  });
    
}
