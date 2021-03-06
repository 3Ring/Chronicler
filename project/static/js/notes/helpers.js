

/**
 * Given an event, return the element that has the specified attribute
 * @param e - The event object.
 * @param attribute - The attribute to look for.
 * @returns The element that has the attribute. or false
 */
function click_inside_element(e, attribute) {
  let el = e.target;
  if (el.hasAttribute(attribute)) {
    return el;
  } else {
    while ((el = el.parentNode)) {
      if (el.hasAttribute(attribute)) {
        return el;
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

