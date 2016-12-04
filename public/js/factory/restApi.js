function restApi( $q , $rootScope,$http) {
	//var baseUrl =  'http://10.20.14.83:9003';//"http://124.124.83.165:9000";
	var baseUrl =  'http://127.0.0.1:9000';//"http://124.124.83.165:9000";
	
	console.log("Rest api Initiated");
	var restApi = {};
	
	// login
	restApi.getStockResults = function(username,password){
			var defer=$q.defer();
			$.ajax({
		        type: "GET",
		        url: baseUrl +'/getLatestData',
		        contentType: "application/json",
		        headers: {
	        		'Access-Control-Allow-Origin': baseUrl 
		        },
		        async:true,
		        success: function(data, textStatus, xhr){
		            defer.resolve(data);
		        },
		        error: function(data, textStatus, xhr){
		            defer.reject(data);
		        },
		        timeout: 15000 
		    });
			return defer.promise;
	};
	

	return restApi;
	
}