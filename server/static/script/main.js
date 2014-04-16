
// Require.js allows us to configure shortcut alias, simplifying later usage
require.config({
    paths: {
        jquery: 'libs/jquery/jquery.min',
        underscore: 'libs/underscore/underscore-min',
        backbone: 'libs/backbone/backbone-min',
        bootstrap: 'libs/bootstrap/bootstrap.min',
        text: 'libs/require/text'
    }
});

require([
    'app'
], function(App){
   App.initialize();
});