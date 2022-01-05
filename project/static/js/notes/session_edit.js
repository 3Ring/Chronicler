/*
Main function
*/
function Session_Editor() {
  let deployed = { confirm: false, edit: false, context: false };
  if (USER_IS_DM) {
    document.addEventListener("click", (e) => {
      if (!deployed.confirm) {
        if (!deployed.edit) {
          if (!deployed.context) {
            if (!!click_inside_element(e, "data-sessionEditButton_num")) {
              deploy_context(e, deployed);
            } else {
              toggle_all_off(deployed);
            }
          } else if (!!click_inside_element(e, "data-sessionContext_id")) {
            const choice = e.target.getAttribute("data-action");
            if (choice == "edit") {
              deploy_edit(e, deployed);
            } else if (choice == "delete") {
              deploy_confirm(e, deployed);
            }
          } else {
            toggle_all_off(deployed);
          }
        } else if (!!click_inside_element(e, "data-sessionEditCancel_id")) {
          toggle_all_off(deployed);
        }
      } else if (!!click_inside_element(e, "data-sessionConfirm_id")) {
        let choice = e.target.getAttribute("data-action");
        if (choice == "delete") {
          toggle_all_off(deployed);
          SOCKET.emit(
            "check_delete_session",
            e.target.getAttribute("data-sessionConfirm_id")
          );
        } else if (choice == "cancel") {
          toggle_all_off(deployed);
        }
      }
    });
    const edit_forms = document.querySelectorAll(
      `form[data-flag='formEditSession_form']`
    );
    for (let i = 0; i < edit_forms.length; i++) {
      edit_forms[i].addEventListener("submit", (e) => {
        e.preventDefault();
        const id_num = e.target.getAttribute("data-sid");
        const number = document.querySelector(
          `input[data-session_edit_number="${id_num}"]`
        ).value;
        const title = document.querySelector(
          `input[data-session_edit_title="${id_num}"]`
        ).value;
        console.log(id_num, number, title);
        SOCKET.emit("edit_session", id_num, number, title);
        toggle_all_off(deployed);
      });
    }
  }
}

/*
socket actions
*/
SOCKET.on("check_delete_session_fail", () => {
  alert("session has other user's notes. cannot delete session");
});

SOCKET.on("check_delete_session_pass", (session_num) => {
  let sl = document.querySelector(`li[data-number_sessionList='${session_num}']`);
  sl.remove();
  let sc = document.querySelector(`div[data-number_sessionCont='${session_num}']`);
  sc.remove();
});

/*
Menu deployment functions
*/
function deploy_context(e, deployed) {
  const target_id = e.target.getAttribute("data_sessionEditButton_id");
  const target_element = document.querySelector(
    `div[data-sessionContext_id="${target_id}"]`
  );
  toggle_session_element_on(target_element);
  deployed.context = true;
}
function deploy_edit(e, deployed) {
  toggle_all_off(deployed);
  const session_id = e.target.getAttribute("data-editChoices_id");
  const edit = document.querySelector(
    `div[data-sessionEdit_id="${session_id}"]`
  );
  toggle_session_element_on(edit);
  deployed.edit = true;
}
function deploy_confirm(e, deployed) {
  toggle_all_off(deployed);
  const session_id = e.target.getAttribute("data-editChoices_id");
  const confirm = document.querySelector(
    `div[data-sessionConfirm_id="${session_id}"]`
  );
  toggle_session_element_on(confirm);
  deployed.confirm = true;
}

/*
Deployment helper functions
*/
function toggle_session_element_on(el) {
  el.classList.add(CLASSNAME_ACTIVE);
  el.classList.remove(CLASSNAME_HIDDEN);
}
function toggle_all_off(deployed) {
  const all = document.querySelectorAll(`div[data-flag='sessionEdit']`);
  all.forEach((el) => {
    el.classList.remove(CLASSNAME_ACTIVE);
    el.classList.add(CLASSNAME_HIDDEN);
  });
  for (let key of Object.keys(deployed)) {
    deployed[key] = false;
  }
}
