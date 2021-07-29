
// function print(input) {
//     console.log(input);
// }


function showPopup(popupID) {
    $("#popup-container > div").hide();
    $("#popup-container").show();
    $(`#${ popupID }`).show();
}


$(document).ready(function() {
    $("#popup-container").on("click", function(event) {
        if (event.target == $("#popup-container")[0]) {
            $("#popup-container").hide();
        }
    })
})


