// Variables
const socket = io("https://chronicler.gg")
, className__hidden = "hidden"
, className__active = "--active"
, className__active_sessionList = "current";
var menu_deployed = false
, current__session_number = 0

, flag__formEdit_form = "form[data-flag='formEdit']"

, flag__formNewSession_container = "div[data-flag='formNewSession_container']"
, flag__button_newSessionDisplay = "[data-flag='button_newSessionDisplay']"
, flag__formNewSession_form = "form[data-flag='formNewSession_form']"
, flag__formNewSession_inputSessionNumber = "input[data-flag='formNewSession_inputSessionNumber']"
, flag__formNewSession_inputSessionTitle = "input[data-flag='formNewSession_inputSessionTitle']"
, flag__formNewSession_inputSessionSynopsis = "input[data-flag='formNewSession_inputSessionSynopsis"
, flag__formNewSession_buttonCancel = "input[data-flag='formNewSession_buttonCancel']"
, flag__formNewSession_idGame = "input[data-flag='formNewSession_idGame']"

, flag__newQuill_formSession = "form[data-flag='newQuill_FormSession']"
, flag__newQuillPrivate = "input[data-flag='newQuillPrivate']"

, flag__sessionContainer = "div[data-flag='sessionsContainer']"

, attribute__editButtons = "data-editButtonAnchorId"
, attribute__editMenu = "data-editMenuId"
, attribute__contextForm = "data-contextMenuId";
