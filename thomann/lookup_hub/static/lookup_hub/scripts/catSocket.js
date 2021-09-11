
function startCatSocket() {
    var wsURL = socketType + "://"
        + window.location.hostname
        + portNumber
        + "/ws/category/"
        + dictionaryInfo.slug;

    catSocket = new WebSocket(wsURL);

    catSocket.onopen = function() {
        try {
            if (rowSocket.readyState === WebSocket.OPEN) {
                dictionary = null;
                dictionary = new Dictionary();
                dictionary.initialise();
                setSocketConnectedButton(true);
            }
        } catch(err) {
            console.log(err);
        }

        console.log("catSocket is connected");
    }

    catSocket.onclose = function() {
        // catSocket = null;

        try {
            if (rowSocket.readyState === WebSocket.CLOSED) {
                dictionary.showLoading();
                setSocketConnectedButton(false);
            }
        } catch(err) {
            console.log(err);
        }

        console.error("catSocket closed unexpectedly. Retrying...");
        console.log("Trying to connect...")
        setTimeout(startCatSocket, 1000);
    }

    catSocket.onmessage = function(event) {
        var response = JSON.parse(event.data);
        console.log(response)

        if (response["action"] == "read") {
            var category = new Category(response["data"]);
            showEditCatWindow(category);
        } else if (response["action"] == "updated") {
            updateCatElement(response["data"]);
        } else if (response["action"] == "inserted") {
            insertCatElement(response["data"]);
        } else if (response["action"] == "appended") {
            appendCatElement(response["data"]);
        }
    };
}


function showEditCatWindow(category) {
    $("#cat-id").text(category.id);
    $("#category-name").val(category.name);
    showPopup("edit-category-form");
}


function submitCategoryChanges() {
    catData = {
        id: $("#cat-id").text(),
        name: $("#category-name").val(),
    }

    sockUpdateCategory(catData);
}




/**************
 * Socket functions
 */

 function sockReadCategory(catID) {
    var socketData = {
        method: "read",
        data: { id: catID },
    };

    catSocket.send(JSON.stringify(socketData));
}


function sockUpdateCategory(catData) {
    catSocket.send(JSON.stringify({
        method: "update",
        data: catData,
    }));
}


function sockInsertCategory(catID) {
    var socketData = {
        method: "insert",
        data: { id: catID },
    };

    catSocket.send(JSON.stringify(socketData));
}


/**************
 * DOM changes
 */

 function updateCatElement(responseData) {
    $catContainerCurrent = $(`.cat-container[data-cat-id='${responseData["id"]}']`).first();
    $catContainerCurrent.find(".cat-header").text(escapeHTML(responseData["name"]));
}


function insertCatElement(responseData) {
    $catCurrent = $(`.cat-container[data-cat-id='${responseData["prev_id"]}']`).first();
    var catNew = new Category(responseData["new_cat"]);
    catNew.brandNewJq.insertAfter($catCurrent);
}


startCatSocket();
