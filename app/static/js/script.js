document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('uploadType').addEventListener('change', function() {
        var selectedType = this.value;
        document.getElementById('audioField').style.display = 'none';
        document.getElementById('textField').style.display = 'none';
        document.getElementById('imageField').style.display = 'none';
        document.getElementById('videoField').style.display = 'none';

        if (selectedType === 'audio') {
            document.getElementById('audioField').style.display = 'block';
        } else if (selectedType === 'text') {
            document.getElementById('textField').style.display = 'block';
        } else if (selectedType === 'image') {
            document.getElementById('imageField').style.display = 'block';
        } else if (selectedType === 'video') {
            document.getElementById('videoField').style.display = 'block';
        }
    });
});
