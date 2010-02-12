/* SYSTEM **************************************************/
$(document).ready(function(){
    var file = $("#file");
    var file_path = $("#file_path");
    file.change(function(){
        file_path.val($(this).val());
    });
    
    // TODO: editing the file_path will change the value of the file
    // file_path.live("keypress", function(){
    //     console.log("changed");
    //     file.val(this.value);
    //     console.log(this.value);
    // });
    
});