
// variables
var className__hidden = "hidden"
, className__cancel = "game_cancel"
, className__confirm = "game_confirm"
, className__cardsConfirm = "confirm_card"
, className__selectGame = "select_game"
, className__active = "--active"

, idPrefixName_selectGame = "selectGame_"
, idPrefixName_confirmCard = "confirmCard_";

document.addEventListener("DOMContentLoaded", function() {

    var elements__buttonCancel = document.getElementsByClassName(className__cancel)
    , elements__buttonConfirm = document.getElementsByClassName(className__confirm)
    , elements__selectGame = document.getElementsByClassName(className__selectGame)
    , elements__cardConfirm = document.getElementsByClassName(className__cardsConfirm);

    // Helper functions
    //
    //
    //
    //

    // Add hidden class name to any confirm element that doesn't have one already
    function hide() {
        for (let i = 0; i < elements__cardConfirm.length; i++) {
            if (elements__cardConfirm[i].classList.contains(className__hidden)) {} else {
                elements__cardConfirm[i].classList.add(className__hidden);
            }
        }
    }

    // remove hidden class element from element and add active hook
    function reveal(element_id) {
        let element_to_reveal = document.getElementById(element_id);
        element_to_reveal.classList.remove(className__hidden);
        element_to_reveal.classList.add(className__active);
    }
    function clean_id(id) {
        if (id) {
            return id.length
        } else {
            return false
        }
    }
    // Check if the id has the correct prefix and return id
    function checkPrefix(element_id, prefix) {
        var id = ""
        , current = ""
        , clean_length = clean_id(element_id);

        if (clean_length) {
            for (let i = 0; i < element_id.length; i++) {
                current += element_id[i];
                if (current == prefix) {
                    for (let j = i+1; j < element_id.length; j++) {
                        id += element_id[j];
                    }
                    break
                }
            }
        }
        return id
    }
    // Core
    // 
    // 
    // 
    // 

    // Add click events

    // Add events to hide all confirm elements on page when cancel button is clicked
    for (let i = 0; i < elements__buttonCancel.length; i++) {
        elements__buttonCancel[i].addEventListener("click", function() {
            hide();
        })
    }

    // add events to reveal confirm cards
    for (let i = 0; i < elements__selectGame.length; i++) {
        elements__selectGame[i].addEventListener("click", function(event) {
            let element = event.target;
            var id = checkPrefix(element.id, idPrefixName_selectGame);
            if ( id != '' ) {
                reveal(id);
            } else {
                while ( element = element.parentNode ) {
                    id = checkPrefix(element.id, idPrefixName_selectGame)
                    if ( id != '' ) {
                        reveal(idPrefixName_confirmCard + id);
                    }
                }
            }
        })
    }

});
