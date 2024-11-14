document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('image-upload-form').addEventListener('submit', function(event) {
      const fileInput = document.getElementById('image_file');
      const errorMessageElement = document.getElementById('error-message');

      if (!fileInput.files || !fileInput.files[0] || !fileInput.files[0].type.includes("png")) {
        event.preventDefault();
        errorMessageElement.style.display = "block";
        errorMessageElement.innerText = "PNG file required.";
        errorMessageElement.style.fontSize = "0.8rem"
      } else {
        errorMessageElement.style.display = "none";
      }
    });
});

function clearFileInput() {
  const fileInput = document.getElementById('image_file');
  fileInput.value = '';
  document.getElementById('error-message').style.display = "none";
}
// Preview Icon image
function previewImage(event) {
  const file = event.target.files[0];
  if (file && file.type.includes('image')) {
    const reader = new FileReader();
    reader.onload = function(e) {
      // Hide the SVG icon
      document.getElementById('upload-icon').style.display = 'none';
      
      // Set the image source and make it visible
      const imagePreview = document.getElementById('image-preview');
      imagePreview.src = e.target.result;
      imagePreview.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
  }
}

function clearFileInput() {
  const fileInput = document.getElementById('image_file');
  fileInput.value = ''; // Clear the input

  // Reset the preview elements
  document.getElementById('image-preview').classList.add('hidden');
  document.getElementById('upload-icon').style.display = 'block';
}

// document.addEventListener('DOMContentLoaded', function () {
  document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('image-upload-form').addEventListener('submit', function (event) {
      const fileInput = document.getElementById('image_file');
      const errorMessage = document.getElementById('error-message');
  
      if (!fileInput.files || !fileInput.files[0]) {
        event.preventDefault(); // Prevent form submission
  
        // Show the error message tooltip without additional positioning logic
        errorMessage.classList.remove('hidden');
        errorMessage.style.display = 'block'; // Ensure it's visible
  
        // Hide the tooltip after 3 seconds
        setTimeout(() => {
          errorMessage.classList.add('hidden');
          errorMessage.style.display = 'none';
        }, 3000);
      }
    });
  });
 