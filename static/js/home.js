// javascript functions for the loading icon

function hideLoadSearch() {
  document.getElementById("loader_top").style.display = "none";
}

function showLoadSearch() {
  // first we have to check if the link is correct, similar to the python function, if it isnt,
  // then dont show the loading symbol
  var value = document.getElementById("link").value;
  if (value.includes("open.spotify.com/playlist/"))
    document.getElementById("loader_top").style.display = "block";
}

function hideLoadRefresh() {
  document.getElementById("loader_bottom").style.display = "none";
}

function showLoadRefresh() {
  // first we have to check if the link is correct, similar to the python function, if it isnt,
  // then dont show the loading symbol
  document.getElementById("loader_bottom").style.display = "block";
}