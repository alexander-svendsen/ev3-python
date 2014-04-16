//Not really used for anything except making it easier for us to use the boilerplate

define([
    // These are path alias that we configured in our bootstrap
    'jquery',     // libs/jquery/jquery
    'underscore', // libs/underscore/underscore
    'backbone'    // libs/backbone/backbone
], function($, _, Backbone){
    // Above we have passed in jQuery, Underscore and Backbone
    // They will not be accessible in the global scope
    return {};
    // What we return here will be used by other modules
});