// Setup slider
var slider = document.getElementById("transparency_slider");
var output = document.getElementById("transparency_val");
output.innerHTML = slider.value;

slider.oninput = function() {
    if (this.value < 10) {
    output.innerHTML = "0" + this.value;
    }
    else {
        output.innerHTML = this.value;
    }
};

function empty_processed() {
    // Removes processed img and hides the download button
    document.getElementById ('processed-img').src = "";
    document.getElementById('download-meme-btn').style.display = "none";
};

// Upload image from local and show
var loadFile = function(event) {
    var image = document.getElementById('base-image');
    image.style.width = "20%";
    image.src = "static/ajax-loader.gif";
    document.getElementById('base-img-url').value = "";

    image.src = URL.createObjectURL(event.target.files[0]);
    image.style.width = "100%";
    empty_processed();
};

// Get image from url
var getImgFromURL = function(event) {
    var image = document.getElementById('base-image');
    image.src = "static/ajax-loader.gif";
    image.style.width = "20%";
    var url = document.getElementById('base-img-url').value;
    if (url.length > 0) {
        image.src = url;
        image.style.width = "100%";
        document.getElementById('img_file').value = "";
        empty_processed();
    }
};

// Hijack input submit
$('form#inputform').submit(function(event) {
    // Stop form from submitting normally
    event.preventDefault();

    // Show spinner gif and hide the download button
    var proc_image = document.getElementById('processed-img');
    proc_image.style.width = "20%";
    proc_image.src = "static/ajax-loader.gif";
    document.getElementById('download-meme-btn').style.display = "none";


    var formData = new FormData(this);
    // Get some values from elements on the page:
    var $form = $( this );
    url = $form.attr( "action" );

    var posting = $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            cache: false,
            contentType: false,
            processData: false
        });

    // Put the results in a div
    posting.done(function( data ) {
        var proc_image = document.getElementById('processed-img');
        proc_image.src = data;
        proc_image.style.width = "100%";

        if (proc_image.src.length > 100 ) {
            document.getElementById('download-meme-btn').style.display = "block";
        }
    });
});

function download_meme() {
    var proc_image = document.getElementById('processed-img');
    var btn = document.getElementById('download-meme-btn');

    var a  = document.createElement('a');
    a.href = proc_image.src;
    a.download = 'meme_image.png';
    a.click();
};
