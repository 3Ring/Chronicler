/* 
display image preview on change
 */
document.addEventListener('DOMContentLoaded', function () {
    
    const img = document.querySelector(`img[data-flag="changing_image"]`);
    const input = document.querySelector(`input[data-img="image_change_listener"]`);
    input.addEventListener("change", () => {
        if (input.files[0]) {
            img.src = URL.createObjectURL(input.files[0]);
        }
    });
});