// Functions for displaying Session containers properly
// 
// //

// update current session variable on change
function set_currentSessionVariable_fromElement(element) {

    current_session_int = parseInt(element.getAttribute("data-number_sessionList"));
    current__session_number = current_session_int;
}
// display correct session container element and hide others
function display_sessionCont (active_listElement) {

    // get active session container element
    let elements__sessionConts = document.querySelectorAll("div[data-flag='session_cont']")
    , active_sessionNumber = active_listElement.getAttribute("data-number_sessionList")
    , element__newActiveSessionCont = document.querySelector("div[data-number_sessionCont='" + active_sessionNumber + "']");

    // hide all session containers and remove any active flags
    for ( let i = 0; i < elements__sessionConts.length; i++ ) {
        // hide all sessions
        if ( ! elements__sessionConts[i].classList.contains( className__hidden ) ) {
            elements__sessionConts[i].classList.add( className__hidden );
        }
        // remove all active flags
        if ( elements__sessionConts[i].classList.contains( className__active ) ) {
            elements__sessionConts[i].classList.remove( className__active );
        }
    }

    // display session container
    element__newActiveSessionCont.classList.remove(className__hidden);
    // add active flag
    element__newActiveSessionCont.classList.add(className__active);
}

// remove all active flags from sessionList elements
function remove_activeFlags_sessionList () {

    // compile a list of all the session list elements
    let elements__sessionList = document.querySelectorAll("li[data-flag='sessionList']");

    for ( i = 0; i < elements__sessionList.length; i++ ) {
        // remove active flag if it's there
        if (elements__sessionList[i].classList.contains(className__active_sessionList)) {
            elements__sessionList[i].classList.remove(className__active_sessionList);
        }
    }
}

// get session list container element from event bubbling
function get_sessionList_parent (event) {

    let el = event.target;

    // return element if element is parent
    if ( el.getAttribute("data-number_sessionList") ) {
        return el

    // iterate through parent nodes to find corrent element and return it
    } else {
        while ( el = el.parentNode ) {
            
            // if no match found
            if ( el.parentNode == document ) {
                return null
            } 

            // return container element
            if ( el.getAttribute("data-number_sessionList") ) {
                return el
            }
        }
    }
    return null
}
// apply highlight logic
function apply_sessionHighlightLogic_fromElement (element) {
    // check to make sure function returned parent element
    if ( element ) {

        // check if selected session is already active
        if ( ! element.classList.contains( className__active_sessionList ) ) {
            // remove active flag from all list elements
            remove_activeFlags_sessionList();
            // add active flag to this element
            element.classList.add( className__active_sessionList );
            // display corresponding session container element and hide others
            display_sessionCont(element);
            // update current session variable
            set_currentSessionVariable_fromElement(element);
        }
    }
}
// Session highlight logic
function clickListener__sessionList () {

    // get list of elements in session navbar
    let elements__sessionList = document.querySelectorAll("li[data-flag='sessionList']");

    // add click listeners
    for ( let i = 0; i < elements__sessionList.length; i++ ) {
        elements__sessionList[i].addEventListener( "click", function (event) {
            
            // get new_session element that was clicked on if it exists
            let new_session = get_sessionList_parent( event );
            
            apply_sessionHighlightLogic_fromElement(new_session);

        })
    }
}

// Display most recent session and set active hook on page load
function setActiveSession__onPageLoad () {

    // Local Variables
    let highest = 0
    , flag__containers_session = "div[data-flag='session_cont']"

    // get list of session containers
    , elements__containers_session = document.querySelectorAll(flag__containers_session);

    // check if there are any sessions in the db yet
    if ( elements__containers_session.length != 0 ) {
        
        // iterate through session elements to find most recent one
        for ( let i = 0, session_number = 0; i < elements__containers_session.length; i++ ) {
            // find session number of current element
            session_number = parseInt(elements__containers_session[i].getAttribute("data-number_sessionCont"))
            // check if the number is the highest one
            if ( session_number > highest ) { highest = session_number }
        }

        // set current session variable
        current__session_number = highest;

        // Flag most recent session elements and display most recent session container
        // Sessions List
        let element__sessionList_mostRecent = document.querySelector("li[data-number_sessionList='" + highest + "']");
        element__sessionList_mostRecent.classList.add(className__active_sessionList);

        // Session Container
        let element__sessionCont_mostRecent = document.querySelector("div[data-number_sessionCont='" + highest + "']");
        element__sessionCont_mostRecent.classList.add(className__active)
            // Display container
            element__sessionCont_mostRecent.classList.remove(className__hidden);
    }
}