var stockMarketAnalyser = angular.module('stockMarketAnalyser', ['ngRoute']);

// ecomApp config Config method
stockMarketAnalyser.config(function($routeProvider){
	// Put all the routing here 
	$routeProvider

		.when('/', {
			controller: 'stockController',
			templateUrl: 'views/stock/displayStock.html'
		})
		.otherwise({redirectTo: '/notFound'})
});

// Custome directives

// Register all the factories 
//ecomApp.factory('productFactory', productFactory);
//stockMarketAnalyser.factory('appFactory', appFactory);
//stockMarketAnalyser.factory('restApi', restApi);

// Register all the controllers 
stockMarketAnalyser.controller('stockController', stockController);


