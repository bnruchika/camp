  function get_checkbox_status(id){
      if($('#' + id).is(':checked')){
        return 1
      } else {
        return 0
      }
    }

    function update_data(){
      $.ajax({
        url:"/update_patient_symptoms/",
        type:"POST",
        data : {
          "doctor_reported_symptoms": $("#doctor_reported_symptoms").val(),
          "csrfmiddlewaretoken": csrf_token,
          "patient_id": patient_id,
          "event_id": event_id
        },
        dataType: 'json',
        success : function(data){
          alert("Success")
        },
        error: function(data){
          alert("error")
        }
      })

    $.ajax({
      url:"/update_patient_doctor_advice/",
      type:"POST",
      data : {
        "doctor_clinical_advice": $("#doctor_clinical_advice").val(),
        "csrfmiddlewaretoken": csrf_token,
        "patient_id": patient_id,
        "event_id": event_id
      },
      dataType: 'json',
      success : function(data){
        alert("Update clinical advice")
      },
      error: function(data){
        alert("error")
      }
    })

    $.ajax({
      url:"/update_doctor_notes/",
      type:"POST",
      data : {
        "doctor_notes": $("#doctor_notes").val(),
        "csrfmiddlewaretoken": csrf_token,
        "patient_id": patient_id,
        "event_id": event_id
      },
      dataType: 'json',
      success : function(data){
        alert("Success")
      },
      error: function(data){
        alert("error")
      }
    })

    $.ajax({
      url:"/get_patient_history_api/",
      type:"POST",
      data : {
        "tests": $("#tests").val(),
        "csrfmiddlewaretoken": csrf_token,
        "patient_id": patient_id,
        "event_id": event_id
      },
      dataType: 'json',
      success : function(data){
        alert("Success")
      },
      error: function(data){
        alert("efrror")
      }
    })


    $.ajax({
      url:"/update_patient_allergies/",
      type:"POST",
      data : {
        "patient_allergies": $("#patient_allergies").val(),
        "csrfmiddlewaretoken": csrf_token,
        "patient_id": patient_id,
        "event_id": event_id
      },
      dataType: 'json',
      success : function(data){
        alert("Success")
      },
      error: function(data){
        alert("efrror")
      }
    })
    }


  $("#save_patient_details").click(function(){
    update_data()
  })

    $("#add_medicine").click(function(){
      var med_name = $("#med_name").val()
      var med_dosage = $("#med_dosage").val()
      var morning = get_checkbox_status("morning").toString()
      var afternoon = get_checkbox_status("afternoon").toString()
      var night = get_checkbox_status("night").toString()
      var food = $("input[name='food']:checked"). val();
      var days = $("#days").val();

      $.ajax({
        url:"/update_patient_medicines/",
        type:"POST",
        data : {
          "med_name": med_name,
          "med_dosage": med_dosage,
          "med_cycle": morning+"-"+afternoon+"-"+night+" "+food,
          "days": days,
          "patient_id": patient_id,
          "event_id": event_id,
          "csrfmiddlewaretoken": csrf_token
        },
        dataType: 'json',
        success : function(data){
          var obj = $.parseJSON(data.status);
          var newRowContent = "<tr><th>"+obj.med_name+"</th><th>"+obj.dosage+"</th><th>"+obj.end_date+"</th><th>"+obj.cycle+"</th></tr>";
          $("#medicine_list tbody").append(newRowContent);
        },
        error: function(data){
          alert("error")
        }
      })


    })
    /*
    on click -> Get the values of medicine name , dosage .....
    and populate in the table.
    */
