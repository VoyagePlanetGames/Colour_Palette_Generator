// Show the chosen filename and support drag-and-drop on the upload box.
const fileInput = document.getElementById("file-input");
const fileDrop = document.getElementById("file-drop");
const fileDropText = document.getElementById("file-drop-text");

if (fileInput) {
  fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
      fileDropText.textContent = fileInput.files[0].name;
    }
  });

  ["dragenter", "dragover"].forEach((evt) =>
    fileDrop.addEventListener(evt, (e) => {
      e.preventDefault();
      fileDrop.classList.add("dragover");
    })
  );

  ["dragleave", "drop"].forEach((evt) =>
    fileDrop.addEventListener(evt, (e) => {
      e.preventDefault();
      fileDrop.classList.remove("dragover");
    })
  );

  fileDrop.addEventListener("drop", (e) => {
    if (e.dataTransfer.files.length > 0) {
      fileInput.files = e.dataTransfer.files;
      fileDropText.textContent = fileInput.files[0].name;
    }
  });
}

// Click a swatch to copy its HEX code to the clipboard.
const toast = document.getElementById("toast");

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("show");
  setTimeout(() => toast.classList.remove("show"), 1600);
}

document.querySelectorAll(".swatch").forEach((swatch) => {
  swatch.addEventListener("click", async () => {
    const hex = swatch.dataset.hex;
    try {
      await navigator.clipboard.writeText(hex);
      showToast(`Copied ${hex}`);
    } catch {
      showToast("Copy failed — your browser blocked it.");
    }
  });
});
