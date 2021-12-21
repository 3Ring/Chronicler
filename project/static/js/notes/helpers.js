
/* 
check if element or any of its parents contain attribute
*/
function click_inside_element(e, attribute) {
  let el = e.target;
  // check if element clicked has attribute
  if (el.hasAttribute(attribute)) {
    return el;
  } else {
    // check if any of the parentNodes have the attribute
    while ((el = el.parentNode)) {
      if (el.hasAttribute(attribute)) {
        return el;
        // break before final loop otherwise it will throw an error
      } else if (el.parentNode == document) {
        break;
      }
    }
  }
  return false;
}

/* 
Set new session form's default number to n+1 of highest current session
*/
function set_new_session_form_highest(highest) {
  if (document.querySelector(`form[data-flag="formNewSession_container"]`)) {
    let sessionNumberField = document.querySelector(
        `input[data-flag="formNewSession_inputSessionNumber"`
      )
    let sessionTitleField = document.querySelector(
        `input[data-flag="formNewSession_inputSessionTitle"]`
      );

    sessionNumberField.value = parseInt(highest) + 1;
    sessionTitleField.value = "";
  }
}

