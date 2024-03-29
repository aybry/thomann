var dictionary;
const dictionaryApiUrl = window.location.origin
    + "/api/dictionary_data/"
    + dictionaryInfo.slug;

class Dictionary {
    constructor() {
        this.categories = [];
    }

    initialise() {
        fetch(dictionaryApiUrl).then(response => {
            console.log("Fetching dictionary...")

            if (response.status !== 200) {
                console.log("Dictionary fetch error")
                return
            }

            this.destroy();
            response.json().then(dictionaryData => {
                for (var cat of dictionaryData["category_set"]) {
                    var category = new Category(cat);
                    this.appendCategory(category);
                }
                this.hideLoading();
            });
            console.log("Dictionary fetched!")
        })
    }

    destroy() {
        $("#hub-table > tbody").remove();
    }

    showLoading() {
        $("#loading-dictionary-popup").show();
    }

    hideLoading() {
        $("#loading-dictionary-popup").hide();
    }

    appendCategory(category) {
        var tbody = category.makeTbodyJQ();
        $("#hub-table").append(tbody);
    }
}


class Category {
    constructor(data) {
        this.id = data.id;
        this.name = data.name;

        if (typeof(data["row_set"]) !== "undefined") {
            // When category barebones is fetched (see serialisers)
            this.rows = this.createRows(data["row_set"]);
        }
    }

    createRows(rows) {
        var catRows = new Array();
        for (var rowData of rows) {
            catRows.push(new Row(rowData));
        }
        return catRows;
    }

    makeTbodyJQ() {
        var container = $(this.containerHTML);
        for (var row of this.rows) {
            container.append(row.jq);
        }
        container.append(this.lastRowJQ);
        return container;
    }


    get lastRowJQ() {
        return $(`<tr data-cat-id="${this.id}">
            <td class="no-border"></td>
            <td class="buttons-left">
                <button
                    class="pure-button dictionary-button append-row-button"
                    title="Insert new row here"
                    onclick="sockAppendRow('${this.id}');">
                    <i class="far fa-plus-square fa-lg"></i>
                </button>
            </td>
        </tr>
        <tr data-cat-id="${this.id}">
            <td class="no-border"></td>
            <td class="buttons-left">
                <button
                    class="pure-button dictionary-button"
                    title="Insert new category here"
                    onclick="sockInsertCategory('${this.id}');">
                    <i class="fas fa-folder-plus fa-lg"></i>
                </button>
            </td>
        </tr>
        <tr class='spacer-row'><td class='no-border'></td></tr>`)
    }

    get containerHTML() {
        return `
        <tbody class="cat-container" data-cat-id="${escapeHTML(this.id)}">
            <tr class="cat-header-row">
                <td class="filler"></td>
                <td class="filler"></td>
                <th colspan="3" class="cat-header">${escapeHTML(this.name)}</th>
                ${rightButtonsHTMLCategory(this)}
            </tr>
        </tbody>`
    }

    get brandNewJq() {
        return $(this.containerHTML).append(this.lastRowJQ);
    }
}


class Row {
    constructor(data) {
        this.id = data.id;

        this.de = {};
        this.en = {};
        this.nl = {};

        this.de.text = data["de_text"];
        this.de.comment = data["de_comment"];
        this.de.colour = data["de_colour"];

        this.en.text = data["en_text"];
        this.en.comment = data["en_comment"];
        this.en.colour = data["en_colour"];

        this.nl.text = data["nl_text"];
        this.nl.comment = data["nl_comment"];
        this.nl.colour = data["nl_colour"];

        this.isFlagged = data["is_flagged"];
        this.category = data["category"];
        this.lastModified = data["updated_at"]

        this.pureJSON = data;
    }

    get jq() {
        return $(this.html);
    }

    get html() {
        return rowHTML(this);
    }

    getattr(attribute) {
        if (attribute === "en" ) { return this.en }
        else if (attribute === "de" ) { return this.de }
        else if (attribute === "nl" ) { return this.nl }
        else { return null }
    }

    commentHTML(language) {
        var comment = this.getattr(language).comment;
        if ([undefined, null, ""].indexOf(comment) == -1) {
            return `
                <div class="entry-comment-wrapper">
                    <i class="entry-comment fa fa-sticky-note fa-lg" title="${ escapeHTML(comment) }"></i>
                </div>
            `
        } else {
            return ``
        }
    }

    colourHTML(language) {
        var colour = this.getattr(language).colour;
        if ([undefined, null, ""].indexOf(colour) == -1) {
            return `style="border-right-width: 16px; border-right-color: #${ colour }; border-right-style: solid;"`
        } else {
            return ``
        }
    }
}


function setSocketConnectedButton(isConnected) {
    if (isConnected) {
        $("#socket-status").parent().children("span").text("Connected");
        $("#socket-status")
            .removeClass("fa-unlink")
            .addClass("fa-link");
        $("#socket-status")
            .removeClass("disconnected")
            .addClass("connected");
    } else {
        $("#socket-status").parent().children("span").text("Connected");
        $("#socket-status")
            .removeClass("fa-unlink")
            .addClass("fa-link");
        $("#socket-status")
            .removeClass("disconnected")
            .addClass("connected");
    }
}


var escape = document.createElement('textarea');
function escapeHTML(html) {
    escape.textContent = html;
    return escape.innerHTML;
}


const leftButtonsHTML = (row) => `
    <td class="buttons-left">
        <button
            class="pure-button dictionary-button"
            title="Delete this row"
            data-key="${ row.id }"
            onclick="sockDeleteRow('${ row.id }');">
            <i class="far fa-minus-square fa-lg"></i>
        </button>
    </td>
    <td class="buttons-left">
        <button
            class="pure-button dictionary-button"
            title="Insert new row here"
            data-key="${ row.id }"
            onclick="sockInsertRow('${ row.id }');">
            <i class="far fa-plus-square fa-lg"></i>
        </button>
    </td>
`

const dictionaryElemsHTML = (row) => `
    <td class="hub-entry text-cell de"
        ` + row.colourHTML("de") + `>
        <div class="hub-entry-text"
            id="${ row.id }-de"
            data-key="${ row.id }"
            data-target-language="de">
            ${ escapeHTML(row.de.text) }
            </div>
        ` + row.commentHTML("de") + `
    </td>
    <td class="hub-entry text-cell en"
        ` + row.colourHTML("en") + `>
        <div class="hub-entry-text"
            id="${ row.id }-en"
            data-key="${ row.id }"
            data-target-language="en">
            ${ escapeHTML(row.en.text) }
            </div>
        ` + row.commentHTML("en") + `
    </td>
    <td class="hub-entry text-cell nl"
        ` + row.colourHTML("nl") + `>
        <div class="hub-entry-text"
            id="${ row.id }-nl"
            data-key="${ row.id }"
            data-target-language="nl">
            ${ escapeHTML(row.nl.text) }
            </div>
        ` + row.commentHTML("nl") + `
    </td>
    `

const rightButtonsHTML = (row) => `
    <td class="buttons-right">
        <button
            class="pure-button dictionary-button"
            title="Edit this row"
            data-key="${ row.id }"
            onclick="sockReadRow('${ row.id }');">
            <i class="far fa-edit fa-lg"></i>
        </button>
    </td>
    `


const rightButtonsHTMLCategory = (category) => `
    <td class="buttons-right"">
        <button
            class="pure-button dictionary-button"
            title="Edit this category"
            data-key="${ category.id }"
            onclick="sockReadCategory('${ category.id }');">
            <i class="fas fa-edit fa-lg"></i>
        </button>
    </td>
    `


const rowHTML = (row) => `<tr class="entry-row" data-row-id="${ row.id }">` +
        leftButtonsHTML(row) +
        dictionaryElemsHTML(row) +
        rightButtonsHTML(row) +
    `</tr>`;


function downloadBackup() {
    $("#get-backup-link")[0].click();
}


$(document).keydown(function(event) {
    // Close all inputs on escape key
    if (event.keyCode == 27) {
        $("#popup-container").hide();
    } else if (event.keyCode == 90 && event.ctrlKey && !$("#undo-button").prop("disabled")) {
        dictionary.undo();
    }
});


$(document).ready( function() {

    $("#popup-container").on("click", function(event) {
        if (event.target == $("#popup-container")[0]) {
            $("#popup-container").hide();
        }
    })

    $("#submit-row-button").on("click", function() {
        submitRowChanges();
        $("#popup-container").hide();
    })

    $(".edit-entry-row > input").on("keyup", function(event) {
        if (event.keyCode == 13) {
            $("#submit-row-button").click();
        }
    })

    $("#submit-category-button").on("click", function() {
        submitCategoryChanges();
        $("#popup-container").hide();
    })

    $("#category-name").on("keyup", function(event) {
        if (event.keyCode == 13) {
            $("#submit-category-button").click();
        }
    })
})
