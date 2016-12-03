function stockController($scope,$rootScope,$location,$http,$websocket) {
	console.log("Home controller");
	  $scope.isWorking = "Yes, it is working";

	  //var dataStream = $websocket('ws://54.242.218.128:9000/sock/ws');
	  var dataStream = $websocket('ws://127.0.0.1:9000/sock/ws');

      dataStream.onMessage(function(message) {
      	console.log("Recieved message "+ message.data);
      	$scope.isWorking = message.data;
      });

      dataStream.onOpen(function() {
	    console.log('connection open');
	    dataStream.send('Hello World');
	  });

	  dataStream.onError(function(event) {
	    console.log('connection Error', event);
	  });

	  dataStream.onClose(function(event) {
	    console.log('connection closed', event);
	  });
    
}
