function make_quill() {
  if (!document.getElementById("Quill_sessionNew")) {
    return;
  }
  var quill = new Quill("#Quill_sessionNew", {
    modules: {
      toolbar: [
        ["bold", "italic"],
        [{ size: ["small", false, "large", "huge"] }],
        [{ list: "ordered" }, { list: "bullet" }],
      ],
    },
    placeholder: "A note about this session.",
    theme: "snow",
  });
  return quill;
}
