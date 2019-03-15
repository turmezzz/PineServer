function readURL(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();

    reader.onload = function(e) {
      $('.zip-upload-wrap').hide();

      $('.file-upload-zip').attr('src', e.target.result);
      $('.file-upload-content').show();

      $('.zip-title').html(input.files[0].name);
    };

    reader.readAsDataURL(input.files[0]);

  } else {
    removeUpload();
  }
}

function removeUpload() {
  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
  $('.file-upload-content').hide();
  $('.zip-upload-wrap').show();
}
$('.zip-upload-wrap').bind('dragover', function () {
    $('.zip-upload-wrap').addClass('zip-dropping');
  });
  $('.zip-upload-wrap').bind('dragleave', function () {
    $('.zip-upload-wrap').removeClass('zip-dropping');
});

