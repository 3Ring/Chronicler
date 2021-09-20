// Main Function
// 
// 
// //

// Start app
function init(DM="") {

    // note editting functions
    Note_Editor();

    // general functions
    Checkbox_logic();

    // Quill functions
    let quill = make_quill ();
    NewQuill_submitListener(quill);

    // set current session
    setActiveSession__onPageLoad();
    clickListener__sessionList ();
    if (DM == "DM") {
        // newSession functions
        NewSessionMaker();
    }
    
}