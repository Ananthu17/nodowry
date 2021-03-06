function  bindImage(images) {
    $('#grid').empty();
    images.map(item => {
        image =    `<div class="item">
                            <img src="/media/${item.file}" id="img${item.id}" alt=""/>
                            <i class="fa fa-trash delete-button cursor-pointer" id="icon${item.id}"aria-hidden="true" onclick="DeleteImage(${item.id})"></i>
                     </div>`;
        $('#grid').append(image);
    })
}



function uploadPhoto() {
    $('#loader-round').show();
    $('#maximumImages').addClass('d-none');
    var $fileUpload = $("input[type='file']");
    if (parseInt($fileUpload.get(0).files.length)>10){
         $('#maximumImages').addClass('d-block');
    }else {

       var formData = new FormData($('#profileImage')[0])

        var request = $.ajax({
            url: "/upload-image",
            type: "POST",
            data:  formData ,
            cache : false,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#loader-round').hide();
                var profile_pic = response.profile_pic[0].profile_pic ;
                if($('.profile-details-pic').length == 0){
                    $('#prodile-picture').append(`<img class="profile-details-pic pb-2" src="/media/${profile_pic}" id="profile-details-pic">`);
                }
                bindImage(response.profile_images);
            }
         });

    }


}




function saveUserImage() {

    var queryString = $('#profileImage').serialize();
    console.log("THis is form data");
    console.log(queryString);
     // var $fileUpload = $("input[type='file']");
     // console.log(data)
     // var request = $.ajax({
     //    url: "/upload-image",
     //    type: "POST",
     //    data:  $("#profileImage").val() ,
     //    success: function (response) {
     //        console.log('Data submited')
     //    }
     // });

}

function DeleteImage(imgId) {
    $('#loader-round').show();
    console.log(imgId);
    $.post('/delete-image', {imgId: imgId});
    var request = $.ajax({
        url: "/delete-image",
        type: "POST",
        data: {imgId: imgId},
        success: function (response) {
            $('#loader-round').hide();
            bindImage(response.profile_images);
        }
    });
}

function hideSection1() {
    $('#section1').hide();
    $('#section2').fadeIn("slow");
}

function showSection1() {
    console.log("hello");
    $('#section1').fadeIn("slow");
    $('#section2').hide();
}

function showSection2() {
    $('#section2').fadeIn("slow");
    $('#section3').hide();
}

function hideSection2() {

    if ($('#address').val() == '') {
        $('#address-error').text('Please fill in this field');
    } else if ($('#state-dropdown').val() == null) {
        $('#state-error').text('Please select a value from the list');
    } else if ($('#dist-dropdown').val() == null) {
        $('#dist-error').text('Please select a value from the list');
    } else if ($('#city-dropdown').val() == null) {
        $('#city-error').text('Please select a value from the list');
    } else if ($('#religion-dropdown').val() == null) {
        $('#religion-error').text('Please select a value from the list');
    } else if ($('#cast-dropdown').val() == null) {
        $('#cast-error').text('Please select a value from the list');
    } else if ($("#height").val() == '')
        $('#height-error').text('Please fill in this field');
    else if ($("#weight").val() == '')
        $('#weight-error').text('Please fill in this field');
    else if ($("#about").val() == '')
        $('#about-error').text('Please fill in this field');
    else
        $.ajax({
            type: 'POST',
            url: '/profile-details',
            data: {
                'id': $('#userId').val(),
                'address': $('#address').val(),
                'state': $('#state-dropdown').val(),
                'dist': $('#dist-dropdown').val(),
                'city': $('#city-dropdown').val(),
                'religion': $('#religion-dropdown').val(),
                'cast': $('#cast-dropdown').val(),
                'subcast': $('#subcast-dropdown').val(),
                'gotra': $('#gotra-dropdown').val(),
                'star': $('#star-dropdown').val(),
                'dosh': $('#dosh-dropdown').val(),
                'body-type': $('#body-type').val(),
                'drinking': $('#drinking').val(),
                'smoking': $('#smoaking').val(),
                'eating': $('#eating').val(),
                'education': $('#education').val(),
                'profession': $('#professional-details').val(),
                'marital': $('#marital-status').val(),
                'physical': $('#physical-status').val(),
                'height': $('#height').val(),
                'weight': $('#weight').val(),
                'about': $('#about').val(),

            },
            success: function () {
                $('#section2').hide();
                $('#section3').fadeIn("slow");
            }
        });

}


function saveForm() {
    console.log("save method is called");
    $.ajax({
        type: 'POST',
        url: '/partner-details',
        data: {
            'id': $('#userId').val(),
            'bodyType': $('#bodyTypePartner').val(),
            'ageFrom': $('#ageFrom').val(),
            'ageTo': $('#ageTo').val(),
            'physicalstatus': $('#physicalParter').val(),
            'maritalstatus': $('#maritialParter').val(),
            'religion': $('#religion-dropdown-partner').val(),
            'cast': $('#cast-dropdown-partner').val(),
            'subcast': $('#subcast-dropdown-partner').val(),
            'gotram': $('#gotra-partner').val(),
            'star': $('#star-dropdown').val(),
            'dosh': $('#dosh-partner').val(),
            'mother_tongue': $('#mother-tongue-partner').val(),
        },
        success: function () {
            $("#modal-close-btn").click();
        }
    });
}


$(document).ready(function () {
    console.log("ready function");
    $("#religion-dropdown").trigger('change');
    $("#religion-dropdown-partner").trigger('change');

    let dropdown = $('#state-dropdown');
    dropdown.empty();
    dropdown.append('<option selected="true" value="select" disabled>Choose State/Province</option>');

    const url = 'static/frontend/docs/state-dist-dist.js';
    const getData = async () => {
        var y = await get_json();
        console.log(y);
    }
    getData();
    function get_json(){
    $.getJSON(url, function (data) {
        $.each(data, function (entry) {
            dropdown.append($('<option></option>').attr('value', entry).text(entry));
        })
        return 1;
    });
    }


    // $.getJSON(url, function (data) {
    //     console.log("data");
    //     $.each(data, function (entry) {
    //         console.log(entry);
    //         dropdown.append($('<option></option>').attr('value', entry).text(entry));
    //     })
    // });

    var request = $.ajax({
        url: "/select-education",
        type: 'GET',
        success: function (resultData) {
            $('#education').empty();
            $.each(resultData.data, function (entry, value) {
                console.log(value.field);
                $('#education').append($('<option></option>').attr('value', value.field).text(value.field));
            });
        }
    });

    var $selectagefrom = $(".agefrom");
    $selectagefrom.html("");
    $selectagefrom.append($('<option value="">Select Age</option>'));
    for (i = 18; i <= 50; i++) {
        console.log(i)
        $selectagefrom.append($('<option></option>').val(i).html(i))
    }

    var $ageto = $(".ageto");
    $ageto.html("");
    $ageto.append($('<option value="25">25</option>'));
    for (i = 18; i <= 50; i++) {
        $ageto.append($('<option></option>').val(i).html(i))
    }


    // $('#address').onkeypress(function() {
    //     console.log("hello");
    // })

    $('#address').keyup(function () {
        $('#address-error').empty();
    });

    $('#height').keyup(function () {
        $('#height-error').empty();
    });

    $('#weight').keyup(function () {
        $('#weight-error').empty();
    });

    $('#about').keyup(function () {
        $('#about-error').empty();
    });

    $("form[name='profileImage']").submit(function (e) {
        var formData = new FormData($(this)[0]);

        $.ajax({
            url: "/upload-image",
            type: "POST",
            data: formData,
            success: function (msg) {
                location.reload();
            },
            cache: false,
            contentType: false,
            processData: false
        });

        e.preventDefault();
    });


});

function selectDist() {
    $('#state-error').empty();
    value = $('#state-dropdown').val();
    const url = 'static/frontend/docs/state-dist-dist.js';
    $.getJSON(url, function (data) {
        $.each(data, function (entry) {
            if (entry == value) {
                $('#dist-dropdown').empty();
                let i;
                for (i in data[value]) {
                    $('#dist-dropdown').append($('<option></option>').attr('value', i).text(i));
                }
                $("#dist-dropdown").trigger('change');
            }
        })
    });
}

function selectCity() {
    valueState = $('#state-dropdown').val();
    valueDist = $('#dist-dropdown').val();
    const url = 'static/frontend/docs/state-dist-dist.js';
    $.getJSON(url, function (data) {
        $.each(data, function (entry) {
            if (entry == valueState) {
                let i;
                for (i in data[valueState]) {
                    if (i == valueDist) {
                        $('#city-dropdown').empty();
                        let x;
                        for (x in data[valueState][i]) {
                            $('#city-dropdown').append($('<option></option>').attr('value', data[valueState][i][x]).text(data[valueState][i][x]));
                        }
                    }
                }
            }
        })
    })
}

function selectCast() {
    $('#religion-error').empty();
    valueReligion = $('#religion-dropdown').val();

    var request = $.ajax({
        url: "/select-cast",
        type: 'POST',
        data: {religion: valueReligion},
        success: function (resultData) {
            $('#cast-dropdown').empty();
            $.each(resultData.data, function (entry, value) {
                $('#cast-dropdown').append($('<option></option>').attr('value', value.name).text(value.name));
            });
            $('#cast-dropdown').trigger('change');
        }
    });
}

function selectSubcast() {
    let valueCast = $('#cast-dropdown').val();
    var request = $.ajax({
        url: "/select-sub-cast",
        type: 'POST',
        data: {cast: valueCast},
        success: function (resultData) {
            $('#subcast-dropdown').empty();
            $.each(resultData.data, function (entry, value) {
                $('#subcast-dropdown').append($('<option></option>').attr('value', value.name).text(value.name));
            });
            $('#subcast-dropdown').trigger('change');
        }
    });
}


function selectCastPartner() {
    valueReligion = $('#religion-dropdown-partner').val();
    var request = $.ajax({
        url: "/select-cast",
        type: 'POST',
        data: {religion: valueReligion},
        success: function (resultData) {
            $('#cast-dropdown-partner').empty();
            $.each(resultData.data, function (entry, value) {
                $('#cast-dropdown-partner').append($('<option></option>').attr('value', value.name).text(value.name));
            });
            $('#cast-dropdown-partner').trigger('change');
        }
    });

}

function selectSubcastPartner() {
    let valueCast = $('#cast-dropdown-partner').val();
    var request = $.ajax({
        url: "/select-sub-cast",
        type: 'POST',
        data: {cast: valueCast},
        success: function (resultData) {
            $('#subcast-dropdown-partner').empty();
            $.each(resultData.data, function (entry, value) {
                $('#subcast-dropdown-partner').append($('<option></option>').attr('value', value.name).text(value.name));
            });
        }
    });
}


// function filterResults() {
//     let lang = $('#mother-tongue-partner').val(),
//      {% if user_profile.gender == "men" %}
//              gender = "woman";
//       {% else %}
//              gender = "men";
//      {% endif %}
//     var ageFrom =  $('#ageFrom').val();
//     var ageTo = $('#ageTo').val();
//
//      window.location = '/filter?gender='+gender+'&agefrom='+ageFrom+'&ageto='+ageTo+'&religion=1&language='+lang;
//  }
