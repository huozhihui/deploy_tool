/*
 WSSH Javascript Client

 Usage:

 var client = new WSSHClient();

 client.connect({
 // Connection and authentication parameters
 username: 'root',
 hostname: 'localhost',
 authentication_method: 'password', // can either be password or private_key
 password: 'secretpassword', // do not provide when using private_key
 key_passphrase: 'secretpassphrase', // *may* be provided if the private_key is encrypted

 // Callbacks
 onError: function(error) {
 // Called upon an error
 console.error(error);
 },
 onConnect: function() {
 // Called after a successful connection to the server
 console.debug('Connected!');

 client.send('ls\n'); // You can send data back to the server by using WSSHClient.send()
 },
 onClose: function() {
 // Called when the remote closes the connection
 console.debug('Connection Reset By Peer');
 },
 onData: function(data) {
 // Called when data is received from the server
 console.debug('Received: ' + data);
 }
 });

 */

function WSSHClient() {
};

WSSHClient.prototype._generateEndpoint = function (options) {
    if (window.location.protocol == 'https:') {
        var protocol = 'wss://';
    } else {
        var protocol = 'ws://';
    }
    var endpoint = protocol + window.location.host +
        '/wssh/' + encodeURIComponent(options.hostname) + '/' +
        encodeURIComponent(options.username) + '/' + encodeURIComponent(options.password) + '/' + encodeURIComponent(options.port);
    // if (options.authentication_method == 'password') {
    //     endpoint += '?password=' + encodeURIComponent(options.password) +
    //     '&port=' + encodeURIComponent(options.port);
    // } else if (options.authentication_method == 'private_key') {
    //     endpoint += '?private_key=' + encodeURIComponent(options.private_key) +
    //     '&port=' + encodeURIComponent(options.port);
    //     if (options.key_passphrase !== undefined)
    //         endpoint += '&key_passphrase=' + encodeURIComponent(
    //             options.key_passphrase);
    // }
    // if (options.command != "") {
    //     endpoint += '&run=' + encodeURIComponent(
    //         options.command);
    // }
    return endpoint;
};

WSSHClient.prototype.connect = function (options) {
    var endpoint = this._generateEndpoint(options);

    if (window.WebSocket) {
        this._connection = new WebSocket(endpoint);
    }
    else if (window.MozWebSocket) {
        this._connection = MozWebSocket(endpoint);
    }
    else {
        options.onError('WebSocket Not Supported');
        return;
    }

    this._connection.onopen = function () {
        options.onConnect();
    };

    this._connection.onmessage = function (evt) {
        var data = JSON.parse(evt.data.toString());
        if (data.error !== undefined) {
            options.onError(data.error);
        }
        else {
            options.onData(data.data);
        }
    };

    this._connection.onclose = function (evt) {
        options.onClose();
    };
};

WSSHClient.prototype.send = function (data) {
    this._connection.send(JSON.stringify({'data': data}));
};


function getCharSize() {
    var $span = $("<span>", {text: "qwertyuiopasdfghjklzxcvbnm"});
    $('#term').append($span);
    var lh = $span.css("line-height");
    lh = lh.substr(0, lh.length - 2);
    var size = {
        width: $span.outerWidth() / 26
        // , heigth: (lh / 1)
        // , height: (lh / 1)
        // , height: $span.outerHeight()
        , height: lh
    };

    $span.remove();
    return size;
}
function getwindowSize() {
    var e = window,
        a = 'inner';
    if (!('innerWidth' in window )) {
        a = 'client';
        e = document.documentElement || document.body;
    }
    return {width: e[a + 'Width'], height: e[a + 'Height']};

}

function get_resize() {
    var charSize = getCharSize();
    var windowSize = getwindowSize();
    console.log(charSize)
    console.log(windowSize)
    return {
        x: Math.floor(windowSize.width / charSize.width)
        , y: Math.floor(windowSize.height / charSize.height) -5
    };

};