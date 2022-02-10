/*
*
*
Flash Close Button
*/

//set close button
const closeButton = document.getElementById('btn-close');

//if there is a close button on the page
if ( closeButton != null) {

    //fire on click
    document.getElementById('btn-close').onclick = function(){
        this.parentNode.parentNode.parentNode
        .removeChild(this.parentNode.parentNode);
        return false;
    };

}