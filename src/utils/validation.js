import validator from 'validator';
const required = (value) => {
  if (!value.toString().trim().length) {
    // We can return string or jsx as the 'error' prop for the validated Component
    return 'require';
  }
};
 


const demovalidator = (value) =>{
   var test = value
   test.split(" ")
   var error = "NONE";

   if(test.length <2 || test.length > 2){
     error = "Incorrect Demographic format. Enter deomographic as {age}-year-old {gender}"
   }
   test = test[0].split("-")
   if(test.length <3 || test.length > 3){
    error = "Incorrect Demographic format. Enter deomographic as {age}-year-old {gender}"
   }
   if(error !=="NONE"){
     return error 
   }
}
 