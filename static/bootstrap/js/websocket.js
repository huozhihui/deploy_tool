/**
 * Created by huozhihui on 16/12/13.
 */
function conn_websocket(host, method, data) {
// function conn_websocket(ws, data) {
    // ws = new WebSocket("ws://" + host + '/' + method + '/' + date['task_log_id']);
    ws = new WebSocket("ws://" + host + '/' + method);
    console.log(ws)

    ws.onopen = function () {
        output("onopen");
        ws.send(JSON.stringify(data));
    };

    ws.onmessage = function (e) {
        // e.data contains received string.
        output("onmessage: " + e.data);
        if (e.data == 'null') {
            ws.close();
            return false
        }

        if (JSON.parse(e.data)['accept']) {
        } else {
            h = JSON.parse(e.data);
            ws_invoke(h);
            // ws.close();
            // for(var i=0; i < h.length; i++){
            //     output(JSON.parse(h[i]));
            //     ws_invoke(JSON.parse(h[i]));
            // }
        }

    };

    ws.onclose = function () {
        output("onclose");
    };

    ws.onerror = function (e) {
        output("onerror");
        console.log(e)
        ws.close();
    };
}

function output(msg) {
    console.log(msg)
}