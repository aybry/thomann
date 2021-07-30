class deletedRow {
    constructor(data) {
        self.id = data["id"];
        self.de = data["de_text"];
        self.en = data["en_text"];
        self.nl = data["nl_text"];
        self.cat = data["category_name"];
        self.deldate = data["deleted_at"];
    }

    get jq() {
        return $(`
        <tr class="rubbish-row" data-row-id="${ self.id }">
            <td>${ self.de }</td>
            <td>${ self.en }</td>
            <td>${ self.nl }</td>
            <td>${ self.cat }</td>
            <td>${ self.deldate }</td>
            <td>
                <button class="centered-inline-button"
                        title="Restore row"
                        onclick="sockRestoreRow('${ self.id }');">
                    <i class="fas fa-trash-restore"></i>
                </button>
            </td>
        </tr>
        `)
    }
}


function showRubbishPopup(deletedRows) {
    console.log(deletedRows);
    $("#rubbish-table-body").html("");

    for (var rowData of deletedRows) {
        var row = new deletedRow(rowData);
        $("#rubbish-table-body").append(row.jq);
    }

    showPopup("rubbish-popup");
}