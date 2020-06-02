jQuery(document).ready(function () {
	
	jQuery('nav > ul > li > a.mainitem').click(function (e) {
		jQuery(this).parents('li').toggleClass('active');
		jQuery(this).parents('li').children('ul').slideToggle(300);
		jQuery(this).children('span').toggleClass('active');
	});

	jQuery('a.menu-open').click(function (e) {
		jQuery(this).toggleClass('active');
		jQuery('main nav').toggleClass('active');
	});

	jQuery('div.edit span').click(function (e) {
		jQuery(this).closest('div.edit').toggleClass('active');
	});

	
	jQuery('li ul li.active').each(function() {
		jQuery(this).parent('ul').slideToggle(300);
	  });

	  jQuery(".reg-links input").focus(function(){
		if(this.value == this.defaultValue){
			this.select();
		}
	});

	  jQuery(".file-inp input").change(function(){
			 filename = jQuery(this).val().replace(/.*\\/, "");
			 if(filename != ''){
			 jQuery(this).siblings("span").text(filename);
			 jQuery(this).parent(".file-inp label").addClass('active');
			 }
			 else{
			 jQuery(this).siblings("span").text('Выберите файл');
			 jQuery(this).parent(".file-inp label").removeClass('active');
			 }
		});
	
})