var tasksURI =  "http://" + $(location).attr('host');
var json_ajax_request = function(uri, uri_method, data) {
    var request = {
        url: uri,
        type: uri_method,
        contentType: "application/json",
        accepts: "application/json",
        cache: false,
        dataType: 'json',
        data: JSON.stringify(data)
    };
    return $.ajax(request, {
        success: function(response) {
            // e.g. filter the response
            return response.result
        }
    });
};

function jsonrpc(path, method){
    var args = [].slice.apply(arguments);
    args = args.slice(2);

    var data = {
        'method' : method,
        'params' : args,
        'id' : 0
    };

    return json_ajax_request(tasksURI + '/' + path, 'POST', data);  //must parse response yourself
}