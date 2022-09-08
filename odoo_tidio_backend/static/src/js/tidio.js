odoo.define('odoo_tidio_backend.backend_chant', function (require) {
var dom = require('web.dom');

const core = require('web.core');
var WebClient = require('web.WebClient');
// note: I know it's ugly to include the whole method without super call but  
// odoo `WebClient` don't provide an appropriate hook to override it. 
// it should provide hook like `get_dom_to_detach` :(
WebClient.include({
	toggleHomeMenu: async function (display) {
        // We check that the homeMenuManagerDisplayed variable is different from
        // the display argument to execute a toggle only when needed.
        if (display === this.homeMenuManagerDisplayed) {
            return;
        }

        if (display) {
            await this.clear_uncommitted_changes();
            core.bus.trigger('will_show_home_menu');

            // Potential changes have been discarded -> the home menu will be displayed
            this.homeMenuManagerDisplayed = true;

            // Save the current scroll position
            this.scrollPosition = this.getScrollPosition();

            // Detach the web_client contents
            const $to_detach = this.$el.contents()
                .not(this.menu.$el)
                .not('.o_loading')
                .not('.o_in_home_menu')
                .not('.o_notification_manager')
                .not('#tidio-chat')
                .not('#tidio-chat-code');
            this.web_client_content = document.createDocumentFragment();
            dom.detach([{ widget: this.action_manager }], { $to_detach: $to_detach }).appendTo(this.web_client_content);

            // Save and clear the url
            this.url = $.bbq.getState();
            if (location.hash) {
                this._ignore_hashchange = true;
                $.bbq.pushState('#home', 2); // merge_mode 2 to replace the current state
            }
            $.bbq.pushState({ cids: this.url.cids }, 0);

            // Attach the home_menu
            await this.homeMenuManager.mount(this.el);
            this.trigger_up('webclient_started');
            core.bus.trigger('show_home_menu');
        } else {
            this.homeMenuManagerDisplayed = false;

            // Detach the home_menu
            this.homeMenuManager.unmount();
            core.bus.trigger('will_hide_home_menu');

            dom.append(this.$el, [this.web_client_content], {
                in_DOM: true,
                callbacks: [{ widget: this.action_manager }],
            });
            delete this.web_client_content;
            this.trigger_up('scrollTo', this.scrollPosition);
            core.bus.trigger('hide_home_menu');
        }
        this.menu.toggle_mode(display, this.action_manager.getCurrentAction() !== null);
        this.el.classList.toggle("o_home_menu_background", display);
    },
});


	



});