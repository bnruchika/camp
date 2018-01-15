  function get_checkbox_status(id) {
      if ($('#' + id).is(':checked')) {
          return 1
      } else {
          return 0
      }
  }

  function update_symptoms(symptom) {
      $.ajax({
          url: "/patient/update_symptoms/",
          type: "POST",
          data: {
              "doctor_reported_symptoms": symptom,
              "csrfmiddlewaretoken": csrf_token,
              "patient_id": patient_id,
              "event_id": event_id
          },
          dataType: 'json',
          success: function(data) {
              $("#patient_symptoms").append("<li>"+symptom+"</li>")
              $("#doctor_reported_symptoms").val("")
          },
          error: function(data) {
              alert("error")
          }
      })
  }
 function update_diseases(disease) {
      $.ajax({
          url: "/patient/update_diseases/",
          type: "POST",
          data: {
              "patient_diseases": disease,
              "csrfmiddlewaretoken": csrf_token,
              "patient_id": patient_id,
              "event_id": event_id
          },
          dataType: 'json',
          success: function(data) {
              $("#update_diseases").append("<li>"+disease+"</li>")
              $("#patient_diseases").val("")
          },
          error: function(data) {
              alert("error")	
	     console.log(data)
          }
      })
  }
 function update_tests(test) {
      $.ajax({
          url: "/patient/update_tests/",
          type: "POST",
          data: {
              "doctor_reported_tests": test,
              "csrfmiddlewaretoken": csrf_token,
              "patient_id": patient_id,
              "event_id": event_id
          },
          dataType: 'json',
          success: function(data) {
              $("#patient_tests").append("<li>"+test+"</li>")
              $("#doctor_reported_tests").val("")
          },
          error: function(data) {
              alert("error")
             console.log(data)
          }
      })
  }



  function update_data() {
      $.ajax({
          url: "/update_patient_doctor_advice/",
          type: "POST",
          data: {
              "doctor_clinical_advice": $("#doctor_clinical_advice").val(),
              "csrfmiddlewaretoken": csrf_token,
              "patient_id": patient_id,
              "event_id": event_id
          },
          dataType: 'json',
          success: function(data) {
              alert("Update clinical advice")
          },
          error: function(data) {
              alert("error")
          }
      })

      $.ajax({
          url: "/update_doctor_notes/",
          type: "POST",
          data: {
              "doctor_notes": $("#doctor_notes").val(),
              "csrfmiddlewaretoken": csrf_token,
              "patient_id": patient_id,
              "event_id": event_id
          },
          dataType: 'json',
          success: function(data) {
              alert("Success")
          },
          error: function(data) {
              alert("error")
          }
      })

      $.ajax({
          url: "/get_patient_history_api/",
          type: "POST",
          data: {
              "tests": $("#tests").val(),
              "csrfmiddlewaretoken": csrf_token,
              "patient_id": patient_id,
              "event_id": event_id
          },
          dataType: 'json',
          success: function(data) {
              alert("Success")
          },
          error: function(data) {
              alert("efrror")
          }
      })


      $.ajax({
          url: "/update_patient_allergies/",
          type: "POST",
          data: {
              "patient_allergies": $("#patient_allergies").val(),
              "csrfmiddlewaretoken": csrf_token,
              "patient_id": patient_id,
              "event_id": event_id
          },
          dataType: 'json',
          success: function(data) {
              alert("Success")
          },
          error: function(data) {
              alert("efrror")
          }
      })
  }


  $('#doctor_reported_symptoms').keyup(function(e) {
      if (e.which == 13) {
          update_symptoms(this.value)
      }
  });
 $('#doctor_reported_tests').keyup(function(e) {
      if (e.which == 13) {
          update_tests(this.value)
      }
  });

  $("#save_patient_details").click(function() {
      update_data()
  })
  $("#patient_diseases").keyup(function(e) {
      if (e.which == 13) {
          update_diseases(this.value)
      }
  });

  $("#add_medicine").click(function() {
      var med_name = $("#med_name").val()
      var med_dosage = $("#med_dosage").val()
      var morning = get_checkbox_status("morning").toString()
      var afternoon = get_checkbox_status("afternoon").toString()
      var night = get_checkbox_status("night").toString()
      var food = $("input[name='food']:checked").val();
      var days = $("#days").val();
      console.log(med_dosage, med_name, morning, afternoon, night, food, days)
      var med_cycle = morning + "-" + afternoon + "-" + night + " " + food
      $.ajax({
          url: "/patient/update_medicines/",
          type: "POST",
          data: {
              "med_name": med_name,
              "med_dosage": med_dosage,
              "med_cycle": med_cycle,
              "days": days,
              "patient_id": patient_id,
              "event_id": event_id,
              "csrfmiddlewaretoken": csrf_token
          },
          dataType: 'json',
          success: function(data) {
              var newRowContent = "<tr><th>" + med_name + "</th><th>" + med_dosage + "</th><th>" + days + " days</th><th>" + med_cycle + "</th></tr>";
              $("#medicine_list tbody").append(newRowContent);
          },
          error: function(data) {
              alert("error")
          }
      })


  })

  /*
  $("input:file").change(function (){
      var fp = $("#dcmimages")
      var len = fp[0].files.length
      for (var i = 0; i < len; i++) {
        $("#dcm_filelist").append("<li>"+fp[0].files[i].name+"</li>")
        file = fp[0].files[i];
        var formdata = new FormData();
        formdata.append('file_upload', file);
        $.ajax({
            type:"POST",
            url:"/patient/upload_dcm_image/",
            enctype: "multipart/form-data",
            data:formdata,
            dataType: 'json',
            success: function(data) {
                var newRowContent = "<tr><th>" + med_name + "</th><th>" + med_dosage + "</th><th>" + days + " days</th><th>" + med_cycle + "</th></tr>";
                $("#medicine_list tbody").append(newRowContent);
            },
            error: function(data) {
                alert("error")
            }
        })
      }
     });
  on click -> Get the values of medicine name , dosage .....
  and populate in the table.
  */
