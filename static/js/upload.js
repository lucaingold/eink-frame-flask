var Demo = (function() {

    function demoUpload() {
        let $uploadCrop;

        function readFile(input) {
            if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.upload-demo').addClass('ready');
                $uploadCrop.croppie('bind', {
                    url: e.target.result
                }).then(function(){
                    console.log('jQuery bind complete');
                });

            }

            reader.readAsDataURL(input.files[0]);
        }
        else {
            swal("Sorry - you're browser doesn't support the FileReader API");
        }
    }

    $uploadCrop = $('#upload-demo').croppie({
        viewport: {
            width: 100,
            height: 100,
            type: 'square'
        },
        enableExif: true
    });

    $('#upload').on('change', function () {
        alert(1);
        readFile(this);
    });

    $('.upload-result').on('click', function (ev) {
        $uploadCrop.croppie('result', {
            type: 'canvas',
            size: 'viewport'
        }).then(function (resp) {
            popupResult({
                src: resp
            });
        });
    });
}

function init() {
    demoUpload();
}

return {
    init: init
};
})();
