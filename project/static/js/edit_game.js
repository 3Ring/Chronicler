/*
TODO Edit Game:
hide/reveal name, img
set published to toggle
set published to correct value
set new to fill <div data-flag="edit_img"> through socket

hide/reveal remove player data-flag="remove_cp_init">
hide/reveal remove character
hide/reveal transfer ownership
set <h2 data-flag="transfer_header"> innerhtml to be "Confirm by entering <player_name> and <game_name> below" through socket
set <h2 data-flag="remove_player_header"> innerhtml Remove <player name> from <game name>?
set image inside <div data-flag="remove_player_cont"> on submit
set <h2 data-flag="remove_character_header"> innerhtml Remove <character name> from <game name>?
set image inside <div data-flag="remove_character_cont"> on submit
set image inside <div data-flag="transfer_form_cont" on submit


*/
const SOCKET = set_socket();
function set_socket() {
  let socket = null;
  if (heroku) {
    socket = io("https://www.chronicler.gg", {
      withCredentials: true,
    });
  } else {
    socket = io();
  }
  return socket;
}
const HIDDEN = "hidden";
document.addEventListener("DOMContentLoaded", () => {
  let pub = document.querySelector("input[data-published]");
  pub.getAttribute("data-published") == "True"
    ? (pub.checked = true)
    : (pub.checked = false);
  let rPlayerId = null;
  let rPlayerName = null;
  if (players) {
    set_select_title("select[id='players']", "Choose player to remove");
    set_select_title("select[id='characters']", "Choose character to remove");

    document
      .querySelector("select[id='players']")
      .addEventListener("change", function () {
        rPlayerId = this.value;
        rPlayerName = this.innerHTML;
      });
  }
  /*
  Buttons
  */
  document
    .querySelector("a[data-change_name='button']")
    .addEventListener("click", () => {
      document
        .querySelector("div[data-change_name='input']")
        .classList.toggle(HIDDEN);
    });
  document
    .querySelector("a[data-change_img='button']")
    .addEventListener("click", () => {
      document
        .querySelector("div[data-change_name='input']")
        .classList.toggle(HIDDEN);
    });
  if (players) {
    document
      .querySelector("a[data-remove_player='button']")
      .addEventListener("click", () => {
        hide_remove_character_form();
        document
          .querySelector("form[data-flag='remove_player']")
          .classList.toggle(HIDDEN);
      });
    document
      .querySelector("a[data-remove_character='button']")
      .addEventListener("click", () => {
        hide_remove_player_form();
        document
          .querySelector("form[data-flag='remove_character']")
          .classList.toggle(HIDDEN);
      });

    /*
  Confirmation display functions
  */
    document
      .querySelector("a[data-flag='remove_player_select_button']")
      .addEventListener("click", () => {
        if (!rPlayerName) {
          alert("You must select a player to remove");
        } else {
          document.querySelector(
            "input[data-flag='player_remove_hidden']"
          ).value = rPlayerId;
          let header = document.querySelector(
            `h2[data-flag="remove_player_header"]`
          );
          header.innerHTML = `Do you wish to remove ${rPlayerName}?`;
          let cont = document.querySelector(
            `div[data-flag="remove_player_cont"]`
          );
          cont.classList.remove(HIDDEN);
          document
            .querySelector(`a[data-flag="remove_player_cancel"]`)
            .addEventListener("click", () => {
              cont.classList.add(HIDDEN);
            });
        }
      });
    document
      .querySelector("a[data-flag='remove_player_cancel_button']")
      .addEventListener("click", () => {
        hide_remove_player_form();
      });
  }
  // SOCKET.on("remove_player_start_success", (user_name, user_id) => {});
});

function hide_remove_player_form() {
  document
    .querySelector("form[data-flag='remove_player']")
    .classList.add(HIDDEN);
}
function hide_remove_character_form() {
  document
    .querySelector("form[data-flag='remove_character']")
    .classList.add(HIDDEN);
}
if (players) {
  function set_select_title(selector, header) {
    let players = document.querySelector(selector);
    let title = document.createElement("option");
    title.setAttribute("selected", true);
    title.setAttribute("hidden", true);
    title.setAttribute("value", "");
    title.innerHTML = header;
    players.insertAdjacentElement("afterbegin", title);
  }
}
