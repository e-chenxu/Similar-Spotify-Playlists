/* javascript functions for the loading icon
first we have to check if the link is correct, similar to the python function, if it isn't,
then don't show the loading symbol */

if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}

function hideLoadSearch() {
  document.getElementById("loader_top").style.display = "none";
}


function showLoadSearch() {
  const value = document.getElementById("link").value;
  if (value.includes("open.spotify.com/playlist/"))
    document.getElementById("search_icon").className = "fa fa-circle-o-notch fa-spin";
}


function hideLoadRefresh() {
  document.getElementById("loader_bottom").style.display = "none";
}


function showLoadRefresh() {
  document.getElementById("loader_bottom").style.display = "block";
}