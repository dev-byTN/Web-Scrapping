// Source - https://stackoverflow.com/a
// Posted by Stacey Reiman
// Retrieved 2025-12-16, License - CC BY-SA 3.0

/* I put your JSON into an external file, loaded from github */
var url = "../../ressource/fetchedTweets.json";

/* this tells the page to wait until jQuery has loaded, so you can use the Ajax call */

$(document).ready(function(){
  $.ajax({
    url: url,
    dataType: 'json',
      error: function(){
        console.log('JSON FAILED for data');
      },
    success:function(results){
      console.log(results);
  /* the results is your json, you can reference the elements directly by using it here, without creating any additional variables */
  
      var tweetsList = document.getElementById("tweetsList");

      results.forEach(function(element) {
      tweetsList.insertAdjacentHTML( 'beforeend',"<li>" + "name : " + element.username+ " </li>");
      }); // end of forEach
    }  // end of success fn
   }) // end of Ajax call
 }) // end of $(document).ready() function