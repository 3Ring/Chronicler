/* 
display image preview on change
 */
document.addEventListener('DOMContentLoaded', function () {
    const img = document.querySelector(`img[data-flag="game_img"]`);
    const input = document.querySelector(`input[name="img"]`);
    input.addEventListener("change", () => {
        if (input.files[0]) {
            img.src = URL.createObjectURL(input.files[0]);
        }
    });
});