// $(document).ready(function(){
//     var image_crop = $('#image_demo').croppie({
//         viewport: {
//             width: 600,
//             height: 300,
//             type:'square' //circle
//         },
//         boundary:{
//             width: 650,
//             height: 350
//         }
//     });
//     $('#cover_image').on('change', function(){
//         var reader = new FileReader();
//         reader.onload = function (event) {
//             image_crop.croppie('bind', {
//                 url: event.target.result,
//             });
//         }
//         reader.readAsDataURL(this.files[0]);
//         $('#uploadimageModal').modal('show');
//     });
//     $('.crop_image').click(function(event){
//         var formData = new FormData();
//         image_crop.croppie('result', {type: 'blob', format: 'png'}).then(function(blob) {
//             formData.append('cropped_image', blob);
//             ajaxFormPost(formData, '/upload-image/');
//         });
//         $('#uploadimageModal').modal('hide');
//     });
// });
// function ajaxFormPost(formData, actionURL){
//     $.ajax({
//         url: actionURL,
//         type: 'POST',
//         data: formData,
//         cache: false,
//         async: true,
//         processData: false,
//         contentType: false,
//         timeout: 5000,
//         beforeSend: function(){
//         },
//         success: function(response) {
//             if (response['status'] === 'success') {
//                 swal({
//                     title:'Success!',
//                     text: response['message'],
//                     type:'success',
//                     timer:2000
//                 }).then(function() {
//                     $('#cover_image').val("");
//                     $('#uploaded-image').attr('src', response['url']);
//                 },function(){
//                 });
//             } else {
//                 swal({
//                     title:'Failed!',
//                     text: response['message'],
//                     type:'error'
//                 });
//             }
//         },
//         complete: function(){
//         }
//     });
// }

// $(document).ready(function () {



window.addEventListener('DOMContentLoaded', function () {
    var avatar = document.getElementById('profile-img');
    var image = document.getElementById('uploadedAvatar');
    var input = document.getElementById('file-input');
    var cropBtn = document.getElementById('crop');
    var rotateRightBtn = document.getElementById('rotateRight');
    var rotateLeftBtn = document.getElementById('rotateLeft');

    var $modal = $('#cropAvatarmodal');
    var cropper;

    $('[data-toggle="tooltip"]').tooltip();

    input.addEventListener('change', function (e) {
        var files = e.target.files;
        var done = function (url) {
            // input.value = '';
            console.log(input.value)
            image.src = url;
            $modal.modal('show');
        };
        // var reader;
        // var file;
        // var url;

        if (files && files.length > 0) {
            let file = files[0];

            // done(URL.createObjectURL(file));
            // if (URL) {
            // }

            // else if (FileReader) {
            reader = new FileReader();
            reader.onload = function (e) {
                done(reader.result);
            };
            reader.readAsDataURL(file);
            // }
        }
    });

    $modal.on('shown.bs.modal', function () {
        cropper = new Cropper(image, {
            aspectRatio: 1,
            viewMode: 3,
        });
    }).on('hidden.bs.modal', function () {
        cropper.destroy();
        cropper = null;
    });

    rotateRightBtn.addEventListener('click', function () {
        console.log("rotated img by 90 degree");
        cropper.rotate(90);
    });

    rotateLeftBtn.addEventListener('click', function () {
        console.log("rotated img by -90 degree");
        cropper.rotate(-90);
    });

    cropBtn.addEventListener('click', function () {
        // var initialAvatarURL;
        var canvas;

        $modal.modal('hide');

        if (cropper) {
            canvas = cropper.getCroppedCanvas({
                width: 160,
                height: 160,
            });
            // initialAvatarURL = avatar.src;
            avatar.src = canvas.toDataURL();
        }
    });

});