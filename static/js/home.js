var myVar;

function hideLoad() {
  document.getElementById("loader_top").style.display = "none";
}

function showLoad() {
  // first we have to check if the link is correct, similar to the python function, if it isnt,
  // then dont show the loading symbol
  var value = document.getElementById("link").value;
  if (value.includes("open.spotify.com/playlist/"))
    document.getElementById("loader_top").style.display = "block";
}

function hideLoad1() {
  document.getElementById("loader_bottom").style.display = "none";
}

function showLoad1() {
  // first we have to check if the link is correct, similar to the python function, if it isnt,
  // then dont show the loading symbol
  document.getElementById("loader_bottom").style.display = "block";
}