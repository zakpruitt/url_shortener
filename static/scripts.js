window.GenerateURL = function (url) {
  $.ajax({
    type: "POST",
    url: "/",
    dataType: "text",
    contentType: "application/json",
    async: false,
    data: JSON.stringify({
      original: url,
    }),
    success: function (data) {
      console.log("URL Handled Successfully.");
      document.getElementById("url").value = data;
    },
    error: function (jqXHR, textStatus, errorThrown) {
      alert("URL generation failed.");
    },
  });
};
