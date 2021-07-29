var rowSocket;
var currentEntry;


function startRowSocket() {
    var wsURL = socketType + "://"
        + window.location.hostname
        + portNumber
        + "/ws/row/"
        + dictionaryData.slug;

    rowSocket = new WebSocket(wsURL);

    rowSocket.onopen = function() {
        console.log("rowSocket is connected")
        $("#socket-status").parent().children("span").text("Connected");
        $("#socket-status")
            .removeClass("disconnected")
            .addClass("connected");
    }

    rowSocket.onclose = function() {
        rowSocket = null;
        $("#socket-status").parent().children("span").text("Disconnected");
        $("#socket-status")
            .removeClass("connected")
            .addClass("disconnected");
        console.error("rowSocket closed unexpectedly. Retrying...");

        console.log("Trying to connect...")
        setTimeout(startRowSocket, 1000);
    }

    rowSocket.onmessage = function(event) {
        var response = JSON.parse(event.data);
        console.log(response)

        if (response["action"] == "read") {
            var row = new Row(response["data"]);
            showEditRowWindow(row);
        } else if (response["action"] == "updated") {
            updateRowElement(response["data"]);
        } else if (response["action"] == "inserted") {
            insertRowElement(response["data"]);
        } else if (response["action"] == "deleted") {
            deleteRowElement(response["data"]);
        } else if (response["action"] == "appended") {
            appendRowElement(response["data"]);
        }
    };
}


function submitRowChanges() {
    rowData = {
        id: $("#row-id").text(),
        en_text: $("#text-en").val(),
        en_comment: $("#comment-en").val(),
        en_colour: $("#colour-en").val()
            .replace("#", "")
            .replace("000000", ""),
        de_text: $("#text-de").val(),
        de_comment: $("#comment-de").val(),
        de_colour: $("#colour-de").val()
            .replace("#", "")
            .replace("000000", ""),
        nl_text: $("#text-nl").val(),
        nl_comment: $("#comment-nl").val(),
        nl_colour: $("#colour-nl").val()
            .replace("#", "")
            .replace("000000", ""),
    }

    sockUpdateRow(rowData);
}


function showEditRowWindow(row) {
    $("#row-id").text(row.id);

    for (var language of ["de", "en", "nl"]) {
        cell = row.getattr(language);

        for (var item of ["text", "comment", "colour"]) {
            if (item == "colour" && [null, "", "000000"].indexOf(cell.colour) == -1) {
                $("#" + item + "-" + language).val("#" + cell.colour);
            } else {
                $("#" + item + "-" + language).val(cell[item]);
            }
        }
    }
    showPopup("edit-row-cells-form");
}


/**************
 * Socket functions
 */

function sockReadRow(rowID) {
    var socketData = {
        method: "read",
        data: { id: rowID },
    };

    rowSocket.send(JSON.stringify(socketData));
}


function sockUpdateRow(rowData) {
    rowSocket.send(JSON.stringify({
        method: "update",
        data: rowData,
    }));
}


function sockInsertRow(rowID) {
    var socketData = {
        method: "insert",
        data: { id: rowID },
    };

    rowSocket.send(JSON.stringify(socketData));
}


function sockAppendRow(rowID) {
    var socketData = {
        method: "append",
        data: { id: rowID },
    };

    rowSocket.send(JSON.stringify(socketData));
}


function sockDeleteRow(rowID) {
    var socketData = {
        method: "delete",
        data: { id: rowID },
    };

    rowSocket.send(JSON.stringify(socketData));
}


/**************
 * DOM changes
 */

function updateRowElement(rowData) {
    $rowCurrent = $(`[data-row-id='${rowData.id}']`).first();
    var rowNew = new Row(rowData);
    $rowCurrent.replaceWith(rowNew.jq);
}


function insertRowElement(responseData) {
    $rowCurrent = $(`[data-row-id='${responseData["prev_id"]}']`).first();
    var rowNew = new Row(responseData["new_row"]);
    rowNew.jq.insertBefore($rowCurrent);
}


function appendRowElement(responseData) {
    $appendRowButton = $(`.cat-container[data-cat-id="${responseData["cat_id"]}"]`)
        .find(".append-row-button").first();
    var rowNew = new Row(responseData["new_row"]);
    rowNew.jq.insertBefore($appendRowButton.parents()[1]);
}


function deleteRowElement(responseData) {
    $rowCurrent = $(`[data-row-id='${responseData["id"]}']`).first();
    $rowCurrent.remove();
}


startRowSocket();
