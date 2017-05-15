var path = require('path')
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')


module.exports = { 
	// base directory (absolute path)
	'context' : __dirname, 

	/// entry point 
	'entry' : './assets/js/index',

	output : { 
	/// where compiled bundle resides
		path : path.resolve('./assets/bundles/'),
		filename : '[name]-[hash].js',

	},

	'plugins' : [ 
		// tells webpack where to store data about your bundles
		new BundleTracker( { 
			filename : './webpack-stats.json'
		}), 

		new webpack.ProvidePlugin({
			$ : 'jquery', 
			jQuery : 'jquery', 
			'window.jQuery' : 'jquery'
		}),

	], 

	'module' : {
		loaders : [
			// load jsx files using babel loader  
			{ 
				test : /\.jsx?$/ , 
				exclude : /node_modules/, 
				loader : 'babel-loader', 
				query : { 
					// specify that we will be dealing with React code
					presets : ['react']
				}

			}
		]
	}, 

	'resolve' : {
		// tells webpack where to look for modules 
		modules : ['node_modules', 'bower-components'] , 
		extensions : ['.js', '.jsx']
	}
}
