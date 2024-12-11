function initializeImagePreview() {
    const imageInput = document.getElementById('image_file');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const preview = document.getElementById('image-preview');
                    const uploadIcon = document.getElementById('upload-icon');
                    if (preview && uploadIcon) {
                        preview.src = e.target.result;
                        preview.classList.remove('hidden');
                        uploadIcon.classList.add('hidden');
                    }
                }
                reader.readAsDataURL(file);
            }
        });
    }
}

function deleteImage() {
    const imageInput = document.getElementById('image_file');
    const preview = document.getElementById('image-preview');
    const uploadIcon = document.getElementById('upload-icon');
    
    if (imageInput) {
        imageInput.value = '';
    }
    if (preview) {
        preview.classList.add('hidden');
    }
    if (uploadIcon) {
        uploadIcon.classList.remove('hidden');
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializeImagePreview);