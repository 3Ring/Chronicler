document.addEventListener("DOMContentLoaded", function () {
    var options = document.getElementsByTagName("select");
    if (options) {
        let el = document.createElement("option");
        el.setAttribute("selected", true);
        el.setAttribute('hidden', true);
        el.setAttribute('value', "");
        el.innerHTML = "Choose Your Character"
        options[0].insertAdjacentElement("afterbegin", el);
    }
});
