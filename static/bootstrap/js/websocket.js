/**
 * Created by huozhihui on 16/12/13.
 */
// function conn_websocket(host, method, date) {
function conn_websocket(ws, date) {
    // ws = new WebSocket("ws://" + host + '/' + method + '/' + date['task_log_id']);
    console.log(ws)

    ws.onopen = function () {
        output("onopen");
        ws.send(JSON.stringify(date));
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
            ws.close();
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