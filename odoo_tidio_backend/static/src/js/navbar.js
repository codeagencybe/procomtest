odoo.define('odoo_tidio_backend.navbar', function(require) {
   "use strict";
	

	var SystrayMenu = require('web.SystrayMenu');
	var Widget = require('web.Widget');
	var Dialog = require('web.Dialog');
	var chat_displayed = false;
 	var core = require('web.core');
   	var _t = core._t;

	var ActionMenu = Widget.extend({

	    template: 'odoo_tidio_backend.chat_icon',
	    
	    events: {
	    	'click .tidio_icon': 'onclick_myicon',
	    },
	    
	    onclick_myicon:function(){
	    	document.tidioIdentify = {
				distinct_id: this.getSession().uid, // Unique visitor ID in your system
				email: this.getSession().partner_email, // visitor email
				name: this.getSession().name, // Visitor name
				phone: this.getSession().partner_phone, // Visitor name
			};

			tidioChatApi.setVisitorData({
				name: this.getSession().name, // Visitor name
				phone: this.getSession().partner_phone, // Visitor name
			  	email: this.getSession().partner_email, // visitor email
			  	city: this.getSession().partner_city, 
			  	country: this.getSession().partner_country,
			});
	    	if (chat_displayed == false){
	    		if ($("#tidio-icon-box").hasClass('offline')){
	    			this.do_warn("Live chat support is currently not available.", 
	    				"Please submit your questions or issues to our helpdesk at support@codeagency.be.\nThanks for your understanding.");
	    			return false;
	    		}
	    		else{
	    			tidioChatApi.open();
		   	  		tidioChatApi.chatDisplay(true);
		   	  		chat_displayed = true;
	    		}
	    	}
	    	else{
	    		tidioChatApi.close();
	   	  		tidioChatApi.chatDisplay(false);	    		
	   	  		chat_displayed = false;
	    	}
	  	},
   	});
   
   SystrayMenu.Items.push(ActionMenu);
   return ActionMenu;

});
(function() {
  	function onTidioChatApiReady() {
    	tidioChatApi.display(false);
  	}
  	function onTidioChatsetStatus(ev){
		if (ev.data == 'offline'){
  			$("#fa-icon").html("<span><span style='color:red;'>●</span> Live support not available</span>");
  			$("#tidio-icon-box").addClass('offline');
  		}
  		else if(ev.data == 'online'){
  			$("#fa-icon").html("<span><span style='color:green;'>●</span> Live support available</span>")
  			$("#tidio-icon-box").removeClass('offline');
  		}
  	}
  	if (window.tidioChatApi) {
   		window.tidioChatApi.on("ready", onTidioChatApiReady);
  	} 
  	else {
    	document.addEventListener("tidioChat-ready", onTidioChatApiReady);
    	document.addEventListener("tidioChat-setStatus", onTidioChatsetStatus);
  	}
})();