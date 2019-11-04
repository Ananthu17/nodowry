$( document ).ready(function() {
    $('#religion-dropdown-partner').trigger('change');

    var $selectagefrom = $("#ageFrom");
        for (i=18;i<=50;i++){
            $selectagefrom.append($('<option></option>').val(i).html(i))
        }

    var $ageto = $("#ageTo");
        for (i=18;i<=50;i++){
            $ageto.append($('<option></option>').val(i).html(i))
        }


});

function selectCastPartner() {
    valueReligion = $('#religion-dropdown-partner').val();
    var request = $.ajax({
          url: "/select-cast",
          type: 'POST',
          data: {religion : valueReligion},
          success: function(resultData) {
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
        data: {cast : valueCast},
        success: function(resultData) {
         $('#subcast-dropdown-partner').empty();
              $.each(resultData.data, function (entry, value) {
                  $('#subcast-dropdown-partner').append($('<option></option>').attr('value', value.name).text(value.name));
              });
        }
    });
}


function changeAge(val){
            var $selectageto = $("#ageTo");
            $selectageto.empty();
            for (i=val;i<=50;i++){
                $selectageto.append($('<option></option>').val(i).html(i))
            }
    }



