function togglepassword(){
  var chk = document.getElementById("password");
  if(chk.type === "password"){
    chk.type = "text";
  }
  else{
    chk.type = "password";
  }
}