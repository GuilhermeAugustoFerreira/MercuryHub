<!DOCTYPE html><html lang="en" class=" ltr " data-doctype="true" dir="ltr" ontouchend="CustomEvent.fireAll('body_clicked', event);"><head><script>document.addEventListener('click', function (event) {
				CustomEvent.fireAll('body_clicked', event);
			});
			document.hasBodyClickedTrigger = 'true';</script><script type="text/javascript"></script><title>Outokumpu Servicenow</title><meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1"></meta><meta http-equiv="cache-control" content="public"></meta><meta name="viewport" content="initial-scale=1.0"></meta><script type="text/javascript" data-description="globals population">
	window.NOW = window.NOW || {};
	var g_loadTime = new Date();
	var lastActivity = new Date();
	var g_lang = 'en';
	var g_system_lang = 'en';
	var g_enhanced_activated = 'true';
	  var g_popup_timeout = parseInt(100);
	var g_export_warn_threshold = parseInt(10000);
	  var g_event_handler_ids = {};
	var g_event_handlers = [];
	var g_event_handlers_onLoad = [];
	var g_event_handlers_onSubmit = [];
	var g_event_handlers_onChange = [];
	var g_event_handlers_onCellEdit = {};
	var g_event_handlers_localCache = {};
	var g_event_handlers_queryTracking = true;
	var g_user_date_time_format = "yyyy-MM-dd HH:mm:ss";
	var g_user_date_format = "yyyy-MM-dd";
	var g_user_decimal_separator = ",";
	var g_user_grouping_separator = ".";
	var g_glide_list_separator = ", ";
	var g_allow_field_dependency_for_templates = ("true" === "true");
	var g_tz_offset = 10800000;
	  var g_tz_user_offset = true;
	var g_first_day_of_week = parseInt(1, 10);
	var g_date_picker_first_day_of_week = parseInt(2, 10);
	  var g_full_calendar_edit = true;
	var g_submitted = false;
	var g_max_table_length = 80;
	var g_fontSizePreference = "";
	var g_fontSize = "10pt";
	// use to be the sys_property glide.ui.js_error_notify, hard coded for PRB603998
	var g_jsErrorNotify = "true";
	var g_cancelPreviousTransaction = true;
	var g_text_direction = "ltr";
	var g_glide_list_filter_max_length =  parseInt("0", 10);
	var g_accessibility = false;
	var g_accessibility_tooltips = true;
	var g_accessibility_tooltip_duration = parseInt("60", 10);
	var g_accessibility_visual_patterns = false;
	var g_accessibility_screen_reader_table = false;
	var g_accessibility_date_format = false;
	var g_detail_row = false;
	var g_builddate = "08-07-2025_0908";
	// default values to be used in absence of user preferences are hard coded below
	// as well as in keyboardShortcuts.js and keyboard_preference_changer.xml
	window.g_keyboard_shortcuts = {};
	window.g_keyboard_shortcuts.allow_in_input_fields = false;
	window.g_keyboard_shortcuts.enabled = true;
	window.g_keyboard_shortcuts.global_search = {};
	window.g_keyboard_shortcuts.global_search.enabled = true;
	window.g_keyboard_shortcuts.global_search.key_combination = 'ctrl+alt+g';
	window.g_keyboard_shortcuts.main_frame = {};
	window.g_keyboard_shortcuts.main_frame.enabled = true;
	window.g_keyboard_shortcuts.main_frame.key_combination = 'ctrl+alt+p';
	window.g_keyboard_shortcuts.navigator_toggle = {};
	window.g_keyboard_shortcuts.navigator_toggle.enabled = true;
	window.g_keyboard_shortcuts.navigator_toggle.key_combination = 'ctrl+alt+c';
	window.g_keyboard_shortcuts.navigator_filter = {};
	window.g_keyboard_shortcuts.navigator_filter.enabled = true;
	window.g_keyboard_shortcuts.navigator_filter.key_combination = 'ctrl+alt+f';
	window.g_keyboard_shortcuts.impersonator = {}
	window.g_keyboard_shortcuts.impersonator.enabled = true;
	window.g_keyboard_shortcuts.impersonator.key_combination = 'ctrl+alt+i';
	// The `g_concourse_onmessage_enforce_same_origin` and `g_concourse_onmessage_enforce_same_origin_whitelist` variables
    // do not appear to be used anywhere other than the CustomEventManager, but leaving these for backwards compatability
	var g_concourse_onmessage_enforce_same_origin = 'true'.toLowerCase() === 'true';
	var g_concourse_onmessage_enforce_same_origin_whitelist = '';
	window.g_load_functions = [];
	window.g_render_functions = [];
	window.g_late_load_functions = [];
	window.g_tiny_url = {};
	window.g_tiny_url.use_tiny = 'true' === 'true';
	window.g_tiny_url.min_length = parseInt('1024');
	
	
	var g_ck = '10db4cd63bdc3ed0ec71e4bf55e45aba6541194a10c47cb078a1ba6990d307a0431af658';
	

	
	var g_acWaitTime = parseInt(250);
	

	var g_autoRequest = '';

	try {
		window.NOW.dateFormat = JSON.parse("{\"timeAgo\": false, \"dateBoth\": false}");
	} catch (e) {
		window.NOW.dateFormat = {timeAgo: false, dateBoth: false};
	}

	window.NOW.dateFormat.dateStringFormat = "yyyy-MM-dd";
	window.NOW.dateFormat.timeStringFormat = "HH:mm:ss";
	window.NOW.shortDateFormat = false;
	window.NOW.listTableWrap = true;
	window.NOW.compact = false;
  	window.NOW.templateToggle = false;
	window.NOW.tabbed = true;
	window.NOW.permalink = true;
	window.NOW.useSimpleStorage = true;
	window.NOW.httpRequestCompressionThreshold = 40000;
	window.NOW.httpRequestCompressionLevel = -1;
	window.NOW.httpRequestCompressionMemoryLevel = -1;
	window.NOW.httpRequestCompressionExcludeUrls = 'xmlhttp.do'.split(',');
	window.NOW.deferAmbConnection = false;
	window.NOW.deferredAmbConnectionTimeout = 10000;
	window.NOW.simpleStorageSynch = "8c3612223b003210ec71e4bf55e45a80";
	window.NOW.language =  'en';
	window.NOW.listOpenInAppTab = false;
	window.NOW.floatingScrollbars = 'false'.toLowerCase() === 'true';
	
	window.NOW.user = {};
	window.NOW.user.preferences = [];
	window.NOW.user.roles = 'problem_task_analyst,cmdb_ms_editor,sn_publications_recipients_user,x_pgo_happy_it_ex.happy_it_ex_data,viz_creator,app_service_user,x_pgo_happysignals.happy_data,workspace_user,cmdb_query_builder_read,global_tags_creator,sn_cmdb_user,sn_comm_management.comm_plan_viewer,knowledge,pa_viewer,contact_user,sn_sow.sow_user,snc_platform_rest_api_access,survey_reader,sn_sttrm_condition_read,cmdb_query_builder,cmdb_ot_viewer,sn_cim.improvement_requester,certification,agent_workspace_user,canvas_user,report_scheduler,report_user,sn_bm_client.benchmark_data_viewer,tracked_file_reader,sn_cmdb_editor,view_changer,itil,happy_agent,template_editor,u_cmdb_health_report_user,problem_coordinator,scrum_user,cmdb_ms_user,actsub_user,email_client_template_read,approver_user,knowledge_manager,email_composer,scrum_story_creator,sn_publications_recipients_list_user,template_read_global,interaction_agent,rm_scrum_task_admin,data_manager_user,cmdb_read,dependency_views,x_pgo_happysignals.happy_agent';
	window.NOW.user.allRoles = 'problem_task_analyst,cmdb_ms_editor,sn_publications_recipients_user,x_pgo_happy_it_ex.happy_it_ex_data,viz_creator,app_service_user,x_pgo_happysignals.happy_data,workspace_user,cmdb_query_builder_read,global_tags_creator,sn_cmdb_user,sn_comm_management.comm_plan_viewer,knowledge,pa_viewer,contact_user,sn_sow.sow_user,snc_platform_rest_api_access,survey_reader,sn_sttrm_condition_read,cmdb_query_builder,cmdb_ot_viewer,sn_cim.improvement_requester,certification,agent_workspace_user,canvas_user,report_scheduler,report_user,sn_bm_client.benchmark_data_viewer,tracked_file_reader,sn_cmdb_editor,view_changer,itil,happy_agent,template_editor,u_cmdb_health_report_user,problem_coordinator,scrum_user,cmdb_ms_user,actsub_user,email_client_template_read,approver_user,knowledge_manager,email_composer,scrum_story_creator,sn_publications_recipients_list_user,template_read_global,interaction_agent,rm_scrum_task_admin,data_manager_user,cmdb_read,dependency_views,x_pgo_happysignals.happy_agent';
	window.NOW.user.userID = '5136503cc611227c0183e96598c4f706';
	window.NOW.user.departmentID = '221db0edc611228401760aec06c9d929';
	window.NOW.user.firstName = 'Guest';
	window.NOW.user.lastName = 'user';
	window.NOW.user.name = 'guest';
  	window.NOW.user.isImpersonating = false;
	window.NOW.batch_glide_ajax_requests = 'true' === 'true';
	window.NOW.batch_glide_ajax_requests_max_time_in_queue = ~~'50';
	window.NOW.batch_glide_ajax_disable_time = ~~'1000';

	window.NOW.currency = {};
	window.NOW.currency.code = 'BRL';
	window.NOW.locale = {};
	window.NOW.locale.code = 'pt_BR';

	window.NOW.attachment = {};
	
	window.NOW.attachment.overflow_limit =  parseInt('3', 10);
	window.NOW.isPolarisEnabled = "false";
	window.NOW.polaris_page_info ={"canUsePolarisCSS":false,"canUsePolarisTemplates":false,"jvar_form_name":"auth_redirect"};</script><script data-comment="GlideUser initialization">(function() {
		 g_render_functions.push(setGlideUser);
		function setGlideUser() {
			if (window.g_user || !window.GlideUser)
		return;

		window.g_user = new GlideUser(NOW.user.name,
			  NOW.user.firstName,
			  NOW.user.lastName,
			  NOW.user.roles,
			  NOW.user.userID,
			  NOW.user.departmentID);
		window.g_user.setRoles(NOW.user.allRoles, true);
		}
	})();</script><script data-comment="Fiscal schedule constants">window.NOW.filter_globals = "[[\"This fiscal month\", \"javascript:gs.beginningOfThisSchedulePeriod(\'0ca8ae11d7222100738dc0da9e6103e3\',\'This fiscal month\')\", \"javascript:gs.endOfThisSchedulePeriod(\'0ca8ae11d7222100738dc0da9e6103e3\',\'This fiscal month\')\", \"javascript:gs.endOfThisSchedulePeriod(\'0ca8ae11d7222100738dc0da9e6103e3\',\'This fiscal month\')\"], [\"Last fiscal month\", \"javascript:gs.beginningOfLastSchedulePeriod(\'0ca8ae11d7222100738dc0da9e6103e3\',\'Last fiscal month\')\", \"javascript:gs.endOfLastSchedulePeriod(\'0ca8ae11d7222100738dc0da9e6103e3\',\'Last fiscal month\')\", \"javascript:gs.endOfLastSchedulePeriod(\'0ca8ae11d7222100738dc0da9e6103e3\',\'Last fiscal month\')\"], [\"Next fiscal month\", \"javascript:gs.beginningOfNextSchedulePeriod(\'0ca8ae11d7222100738dc0da9e6103e3\',\'Next fiscal month\')\", \"javascript:gs.endOfNextSchedulePeriod(\'0ca8ae11d7222100738dc0da9e6103e3\',\'Next fiscal month\')\", \"javascript:gs.endOfNextSchedulePeriod(\'0ca8ae11d7222100738dc0da9e6103e3\',\'Next fiscal month\')\"], [\"Last 3 fiscal months\", \"javascript:gs.beginningOfSchedulePeriodsAgo(3, \'0ca8ae11d7222100738dc0da9e6103e3\',\'Last 3 fiscal months\')\", \"javascript:gs.endOfSchedulePeriodsAgo(1, \'0ca8ae11d7222100738dc0da9e6103e3\',\'Last 3 fiscal months\')\", \"javascript:gs.beginningOfSchedulePeriodsAgo(3, \'0ca8ae11d7222100738dc0da9e6103e3\',\'Last 3 fiscal months\')\"], [\"Last 12 fiscal months\", \"javascript:gs.beginningOfSchedulePeriodsAgo(12, \'0ca8ae11d7222100738dc0da9e6103e3\',\'Last 12 fiscal months\')\", \"javascript:gs.endOfSchedulePeriodsAgo(1, \'0ca8ae11d7222100738dc0da9e6103e3\',\'Last 12 fiscal months\')\", \"javascript:gs.beginningOfSchedulePeriodsAgo(12, \'0ca8ae11d7222100738dc0da9e6103e3\',\'Last 12 fiscal months\')\"], [\"Next 3 fiscal months\", \"javascript:gs.beginningOfSchedulePeriodsAgo(-1, \'0ca8ae11d7222100738dc0da9e6103e3\',\'Next 3 fiscal months\')\", \"javascript:gs.endOfSchedulePeriodsAgo(-3, \'0ca8ae11d7222100738dc0da9e6103e3\',\'Next 3 fiscal months\')\", \"javascript:gs.endOfSchedulePeriodsAgo(-3, \'0ca8ae11d7222100738dc0da9e6103e3\',\'Next 3 fiscal months\')\"], [\"Next 12 fiscal months\", \"javascript:gs.beginningOfSchedulePeriodsAgo(-1, \'0ca8ae11d7222100738dc0da9e6103e3\',\'Next 12 fiscal months\')\", \"javascript:gs.endOfSchedulePeriodsAgo(-12, \'0ca8ae11d7222100738dc0da9e6103e3\',\'Next 12 fiscal months\')\", \"javascript:gs.endOfSchedulePeriodsAgo(-12, \'0ca8ae11d7222100738dc0da9e6103e3\',\'Next 12 fiscal months\')\"], [\"This fiscal quarter\", \"javascript:gs.beginningOfThisSchedulePeriod(\'b198ae11d7222100738dc0da9e6103d7\',\'This fiscal quarter\')\", \"javascript:gs.endOfThisSchedulePeriod(\'b198ae11d7222100738dc0da9e6103d7\',\'This fiscal quarter\')\", \"javascript:gs.endOfThisSchedulePeriod(\'b198ae11d7222100738dc0da9e6103d7\',\'This fiscal quarter\')\"], [\"Last fiscal quarter\", \"javascript:gs.beginningOfLastSchedulePeriod(\'b198ae11d7222100738dc0da9e6103d7\',\'Last fiscal quarter\')\", \"javascript:gs.endOfLastSchedulePeriod(\'b198ae11d7222100738dc0da9e6103d7\',\'Last fiscal quarter\')\", \"javascript:gs.endOfLastSchedulePeriod(\'b198ae11d7222100738dc0da9e6103d7\',\'Last fiscal quarter\')\"], [\"Last 4 fiscal quarters\", \"javascript:gs.beginningOfSchedulePeriodsAgo(4, \'b198ae11d7222100738dc0da9e6103d7\',\'Last 4 fiscal quarters\')\", \"javascript:gs.endOfSchedulePeriodsAgo(1, \'b198ae11d7222100738dc0da9e6103d7\',\'Last 4 fiscal quarters\')\", \"javascript:gs.beginningOfSchedulePeriodsAgo(4, \'b198ae11d7222100738dc0da9e6103d7\',\'Last 4 fiscal quarters\')\"], [\"Next fiscal quarter\", \"javascript:gs.beginningOfNextSchedulePeriod(\'b198ae11d7222100738dc0da9e6103d7\',\'Next fiscal quarter\')\", \"javascript:gs.endOfNextSchedulePeriod(\'b198ae11d7222100738dc0da9e6103d7\',\'Next fiscal quarter\')\", \"javascript:gs.endOfNextSchedulePeriod(\'b198ae11d7222100738dc0da9e6103d7\',\'Next fiscal quarter\')\"], [\"Next 4 fiscal quarters\", \"javascript:gs.beginningOfSchedulePeriodsAgo(-1, \'b198ae11d7222100738dc0da9e6103d7\',\'Next 4 fiscal quarters\')\", \"javascript:gs.endOfSchedulePeriodsAgo(-4, \'b198ae11d7222100738dc0da9e6103d7\',\'Next 4 fiscal quarters\')\", \"javascript:gs.endOfSchedulePeriodsAgo(-4, \'b198ae11d7222100738dc0da9e6103d7\',\'Next 4 fiscal quarters\')\"], [\"This fiscal year\", \"javascript:gs.beginningOfThisSchedulePeriod(\'3f682e11d7222100738dc0da9e610353\',\'This fiscal year\')\", \"javascript:gs.endOfThisSchedulePeriod(\'3f682e11d7222100738dc0da9e610353\',\'This fiscal year\')\", \"javascript:gs.endOfThisSchedulePeriod(\'3f682e11d7222100738dc0da9e610353\',\'This fiscal year\')\"], [\"Last fiscal year\", \"javascript:gs.beginningOfLastSchedulePeriod(\'3f682e11d7222100738dc0da9e610353\',\'Last fiscal year\')\", \"javascript:gs.endOfLastSchedulePeriod(\'3f682e11d7222100738dc0da9e610353\',\'Last fiscal year\')\", \"javascript:gs.endOfLastSchedulePeriod(\'3f682e11d7222100738dc0da9e610353\',\'Last fiscal year\')\"], [\"Next fiscal year\", \"javascript:gs.beginningOfNextSchedulePeriod(\'3f682e11d7222100738dc0da9e610353\',\'Next fiscal year\')\", \"javascript:gs.endOfNextSchedulePeriod(\'3f682e11d7222100738dc0da9e610353\',\'Next fiscal year\')\", \"javascript:gs.endOfNextSchedulePeriod(\'3f682e11d7222100738dc0da9e610353\',\'Next fiscal year\')\"]]" || "[]";</script><script data-description="NOW glide web analytics siteid and url">window.snWebaConfig = window.snWebaConfig || {};
		// glide web analytics config
		window.snWebaConfig.siteId = "0";
		window.snWebaConfig.trackerURL = "";
		window.snWebaConfig.webaScriptPath = "/scripts/piwik-3.1.1/thirdparty/piwik.min.js";
		window.snWebaConfig.ambClient = (window.g_ambClient) ? window.g_ambClient : ((window.amb)? window.amb.getClient(): "");
		window.snWebaConfig.subscribed = false;</script><script type="text/javascript" src="/ConditionalFocus.jsdbx?v=08-07-2025_0908&amp;c=32_814"></script><link href="fav_icon_outokumpu.ico" rel="shortcut icon"></link><script type="text/javascript" src="/scripts/doctype/xperf_timing.jsx?v=08-07-2025_0908"></script><link type="text/css" rel="stylesheet" href="/styles/css_includes_doctype.cssx?v=08-07-2025_0908&amp;c=0158750d3b903a90ec71e4bf55e45aad&amp;theme=system"></link><link type="text/css" rel="stylesheet" href="/styles/heisenberg/source_sans_pro.cssx?v=08-07-2025_0908&amp;c=0158750d3b903a90ec71e4bf55e45aad&amp;theme=system"></link><link type="text/css" rel="stylesheet" href="/styles/heisenberg/heisenberg_all.cssx?v=08-07-2025_0908&amp;c=0158750d3b903a90ec71e4bf55e45aad&amp;theme=system"></link><script>NOW.xperf.cssEnd = NOW.xperf.now();
			NOW.xperf.scriptBegin = NOW.xperf.now();</script><script src="/legacy_date_time_choices_processor.do?lang=en"></script><script type="text/javascript" src="/scripts/doctype/js_includes_doctype.jsx?v=08-07-2025_0908&amp;lp=Wed_Aug_27_03_39_54_PDT_2025&amp;c=32_814"></script><script type="text/javascript" src="/scripts/js_includes_customer.jsx?v=08-07-2025_0908&amp;lp=Wed_Aug_27_03_39_54_PDT_2025&amp;c=32_814"></script><script type="text/javascript" src="/scripts/doctype/history_across_tabs.jsx?v=08-07-2025_0908"></script><script type="text/javascript" src="/scripts/doctype/js_includes_legacy.jsx?v=08-07-2025_0908&amp;lp=Wed_Aug_27_03_39_54_PDT_2025&amp;c=32_814"></script><script type="text/javascript" data-comment="navpage layout preferences, onfocus observation">/**
	* Every window needs to observe these events.
	*/
	if (Prototype.Browser.IE && !isMSIE9) {
		document.onfocusout = function() { CustomEvent.fireTop(GlideEvent.WINDOW_BLURRED, window); };
		document.onfocusin = function() { CustomEvent.fireTop(GlideEvent.WINDOW_FOCUSED, window); };
	} else {
		Event.observe(window, 'blur', function() { CustomEvent.fireTop(GlideEvent.WINDOW_BLURRED, window); });
		Event.observe(window, 'focus', function() { CustomEvent.fireTop(GlideEvent.WINDOW_FOCUSED, window); });
	}</script><script type="text/javascript">g_swLoadTime = new StopWatch(g_loadTime);

    if (window.CustomEvent){
        CustomEvent.fireAll("ck_updated", "10db4cd63bdc3ed0ec71e4bf55e45aba6541194a10c47cb078a1ba6990d307a0431af658");
	    CustomEvent.fireTop("navigation.complete", window);
	}

    addLoadEvent( function() {

		if (isValidTouchDevice())
			addTouchScrollClassToBody();

      if (typeof g_ck != 'undefined') {
        CustomEvent.observe("ck_updated", function(ck) { g_ck = ck; });
        CustomEvent.fireAll("ck_updated", "10db4cd63bdc3ed0ec71e4bf55e45aba6541194a10c47cb078a1ba6990d307a0431af658");}try {
              var helpico = getTopWindow().document.getElementById("help_ico");

              if (helpico) {
                var urlname=window.location.pathname.split("?");
                var search_str = window.location.search;
                
                // if this is a form, extract the record's sys_id...
                var sys_id_loc = search_str.search(/sys_id=[0-9a-f]{32}/i);
                var sys_id_str = (sys_id_loc != -1) ? search_str.substr(sys_id_loc, 39) : null;
                
                // make the URL to our context help processor...
                var url_search = "?sysparm_url=" + urlname[0];
                if (sys_id_loc != -1)
                   url_search += "&" + sys_id_str;

               	helpico.href="context_help.do" + url_search;                	
              }
            } catch (exception) {}

      synchCache();
      pageLoaded();
    });
    
    function synchCache() {
      try {
        var w = getTopWindow();
        if (w.g_cache_message)
          w.g_cache_message.stamp("8c3612223b003210ec71e4bf55e45a80");
  
        if (w.g_cache_td)
          w.g_cache_td.stamp("080b00d63bdc3ed0ec71e4bf55e45a9f");
      } catch(e) {}
    }

    function isValidTouchDevice() {
		var navigator = window.navigator || {};
		var devices;
		try {
			devices = 'iPad,Android'.split(',');
		} catch(ex) {
			devices = [];
		}
		return devices.some(function(item) {return item.trim() === navigator.platform;});
	}

	function addTouchScrollClassToBody() {
		if ('ontouchstart' in window ||
				(navigator.maxTouchPoints !== 'undefined' && navigator.maxTouchPoints > 0) ||
				(navigator.msMaxTouchPoints !== 'undefined' && navigator.msMaxTouchPoints > 0)) {
			if (typeof document.body != undefined) {
				document.body.classList.add('touch_scroll');
			}
		}
	}
  </script><!--googleoff: all--><noscript>This site requires JavaScript to be enabled</noscript> <!--googleon: all--><script type="text/javascript" src="/scripts/app.guided_tours/js_guided_tours_includes.jsx?v=08-07-2025_0908"></script><script>NOW.xperf.scriptEnd = NOW.xperf.now();
				NOW.xperf.parseEnd = NOW.xperf.now();</script></head><body class="       windows chrome       " data-formName="auth_redirect"><span class="sr-only"><div id="html_page_aria_live_polite" role="region" aria-relevant="additions text" aria-atomic="false" aria-live="polite"></div><div id="html_page_aria_live_assertive" role="region" aria-relevant="additions text" aria-atomic="false" aria-live="assertive"></div></span><div class="outputmsg_div"><div id="output_messages" class="outputmsg_container outputmsg_hide"><button type="button" aria-label="Close Messages" id="close-messages-btn" class="btn btn-icon close icon-cross" onclick="GlideUI.get().onCloseMessagesButtonClick(this); return false;"></button><div class="outputmsg_div" aria-live="polite" role="region" data-server-messages="false"></div></div><script>addRenderEvent(function() {CustomEvent.fire('glide_optics_inspect_update_watchfield', '');});

			var accessibilityEnabled = Boolean(false);
			var hasMessages = false;
			if (accessibilityEnabled && hasMessages) {
				$j(function() {
					$j('#output_messages .btn.btn-icon.close').focus();
				});
			}</script><span class="ui_notification" data-type="session_change" data-text="" data-attr-session_domain="global"></span></div><div class="loading-container"><div class="loading-indicator icon-loading icon-lg"></div></div><script data-comment="loading_page redirect">setTimeout(function() {
				top.location.href = 'https://login.microsoftonline.com/973326df-c9da-42d3-b7d6-8941eaadcec4/saml2?SAMLRequest=lVJLb9swDP4rhu5%2BK4ktxAG8BMMCdF3QZDvsJkt0KkCWPFFOt38%2FV0nR7rAOOwmg%2BPF7kGvkgy5G1k7%2B0TzAjwnQRz8HbZBdfxoyOcMsR4XM8AGQecGO7ec7ViQZG531VlhNohYRnFfWbK3BaQB3BHdRAr4%2B3DXk0fsRWZpavBaT2xsb%2B5QIO6SGX0Z%2BhkRaEu1mCcrw51mvSG3PyiSDEs6i7b01WhkI0HpVlsVS9rGoJY9pIcu4W8llXNU0B86lAEHT4IVEH60TEKw2pOcagUT7XUOO99slpXSRd6sur4Tss6zjZV9lVV3DghZlPmP3eOCI6gKvUMQJ9gY9N74hRVYs4jyLs%2BKUlWxBGa2SKqffSXS4hfRBGanM%2Bf1Eu2sTsk%2Bn0yE%2BfDmewoCLkuDu5%2B7%2FDPMbOAxBzrPJZh1yYEG4e7vm9zXxl92Szb%2FI1%2BlbihvhyJ6V73cHq5X4FbVa26etA%2B5nN95NEBYzcP93FXmSh4qScR9aGQxc6VZKB4gk3dx4%2FzzkzW8%3D&RelayState=https%3A%2F%2Foservice.service-now.com%2Fsaml_redirector.do%3Fsysparm_nostack%3Dtrue%26sysparm_uri%3D%252Fnav_to.do%253Furi%253Dsys_attachment.do%25253Fsysparm_referring_url%25253Dtear_off%252526view%25253Dtrue%252526sys_id%25253Db7cef3cedbb334180b3f6e8cd39619dd';
			}, 0);</script><div style="border:none; visibility:hidden"><form name="sys_personalize" method="GET" action="slushbucket.do"><input type="hidden" name="sysparm_referring_url" value="auth_redirect.do?sysparm_stack=no@99@sysparm_url=https%3A%2F%2Flogin.microsoftonline.com%2F973326df-c9da-42d3-b7d6-8941eaadcec4%2Fsaml2%3FSAMLRequest%3DlVJLb9swDP4rhu5%252BK4ktxAG8BMMCdF3QZDvsJkt0KkCWPFFOt38%252FV0nR7rAOOwmg%252BPF7kGvkgy5G1k7%252B0TzAjwnQRz8HbZBdfxoyOcMsR4XM8AGQecGO7ec7ViQZG531VlhNohYRnFfWbK3BaQB3BHdRAr4%252B3DXk0fsRWZpavBaT2xsb%252B5QIO6SGX0Z%252BhkRaEu1mCcrw51mvSG3PyiSDEs6i7b01WhkI0HpVlsVS9rGoJY9pIcu4W8llXNU0B86lAEHT4IVEH60TEKw2pOcagUT7XUOO99slpXSRd6sur4Tss6zjZV9lVV3DghZlPmP3eOCI6gKvUMQJ9gY9N74hRVYs4jyLs%252BKUlWxBGa2SKqffSXS4hfRBGanM%252Bf1Eu2sTsk%252Bn0yE%252BfDmewoCLkuDu5%252B7%252FDPMbOAxBzrPJZh1yYEG4e7vm9zXxl92Szb%252FI1%252BlbihvhyJ6V73cHq5X4FbVa26etA%252B5nN95NEBYzcP93FXmSh4qScR9aGQxc6VZKB4gk3dx4%252FzzkzW8%253D%26RelayState%3Dhttps%253A%252F%252Foservice.service-now.com%252Fsaml_redirector.do%253Fsysparm_nostack%253Dtrue%2526sysparm_uri%253D%25252Fnav_to.do%25253Furi%25253Dsys_attachment.do%2525253Fsysparm_referring_url%2525253Dtear_off%25252526view%2525253Dtrue%25252526sys_id%2525253Db7cef3cedbb334180b3f6e8cd39619dd"></input><input type="hidden" name="sysparm_view" value=""></input></form></div><script type="text/javascript" src="/scripts/ui_page_footer.jsx?v=08-07-2025_0908"></script><span style="display:none" data-comments="js_includes_last_doctype"></span><script type="text/javascript" src="/scripts/thirdparty/dom_purify/purify.jsx?v=08-07-2025_0908&amp;sysparm_substitute=false"></script><script>NOW.xperf.lastDoctypeBegin = NOW.xperf.now();</script><script type="text/javascript" src="/scripts/doctype/js_includes_last_doctype.jsx?v=08-07-2025_0908&amp;lp=Wed_Aug_27_03_39_54_PDT_2025&amp;c=32_814"></script><script type="text/javascript" src="/scripts/heisenberg/heisenberg_all.jsx?v=08-07-2025_0908"></script><script type="text/javascript" src="/scripts/js_includes_list_edit_doctype.jsx?v=08-07-2025_0908&amp;lp=Wed_Aug_27_03_39_54_PDT_2025&amp;c=32_814"></script><script type="text/javascript" src="/scripts/transaction_scope_includes.jsx?v=08-07-2025_0908"></script><script>if ('') 
			GlideTransactionScope.setTransactionScope('');
		if ('') 
			GlideTransactionScope.setRecordScope('');
		if ('') 
			GlideTransactionScope.setTransactionUpdateSet('');
		if (typeof g_form != 'undefined')
			$(g_form.getFormElement()).fire('glidescope:initialized', {gts : GlideTransactionScope});</script><span style="display:none" data-comments="requires"></span><script>NOW.xperf.lastDoctypeEnd = NOW.xperf.now();</script><span style="display:none" data-comments="db_context_menu_script"></span><script>NOW.xperf.dbContextBegin = NOW.xperf.now();</script><script>NOW.xperf.dbContextEnd = NOW.xperf.now();</script><span style="display:none" data-comments="db_context_menu_script"></span><script data-description="MessagesTag">(function() {
 var messages = new GwtMessage();
messages.set('Timing Type');
messages.set('Time Range');
messages.set('Total Time');
messages.set('{0}ms');
messages.set('{0} ms');
messages.set('Browser response time');
messages.set('Server');
messages.set('Timing details');
messages.set('{0} of {1} {2}: {3}');
messages.set('{0} of {1} Other: {2}');
messages.set('{0} of {1} {2}: {3}');
messages.set('Show Timing Breakdown');
messages.set('Browser timing detail');
messages.set('Time');
messages.set('Other');
messages.set('Timing details breakdown');
messages.set('Response time(ms): {0}');
messages.set('Network: {0}');
messages.set('Network: {0}ms');
messages.set('Server: {0}');
messages.set('Server: {0}ms');
messages.set('Browser: {0}');
messages.set('Browser: {0}ms');
messages.set('Response time','Response Time');
messages.set('Close');
messages.set('Cache/DNS/TCP');
messages.set('DOM Processing');
messages.set('Script Load/Parse');
messages.set('CSS and JS Parse');
messages.set('Form Sections');
messages.set('UI Policy - On Load');
messages.set('Client Scripts - On Load');
messages.set('Client Scripts - On Change (initial load)');
messages.set('Browser processing before onload');
messages.set('DOMContentLoaded to LoadEventEnd');
messages.set('addLoadEvent functions');
messages.set('Related Lists');
messages.set('Related Lists (sync)');
messages.set('Related Lists (async)');
messages.set('onLoad');
messages.set('Unload');
})()</script><script type="text/javascript">var g_serverTime = parseInt("37") + parseInt("0");
            var g_logClientViewRoles = "";

			// do not do this for the navigation menu
            if (window.name != 'gsft_nav') {
				 addAfterPageLoadedEvent(function() {
					 if (window.performance)
						setTimeGraph();
					 else 
						firePageTimer();
				 });
			 }
			 
			function setTimeGraph() {
				if (window.performance.timing.loadEventEnd > 0)
			 		firePageTimer();
			 	else 
			 		setTimeout(setTimeGraph, 300);
			 }
			 
			function firePageTimer() {
				 if (window.performance && performance.timing.requestStart != performance.timing.responseStart) {
				 	var p = performance.timing;

				 	CustomEvent.fire('page_timing', { name: 'SERV', ms: p.responseEnd - p.requestStart});
				 	CustomEvent.fire('page_timing', { name: 'REND', ms: (p.loadEventEnd - p.responseEnd) });
				 	CustomEvent.fire('page_timing_network', { name: 'NETW', ms: (p.responseEnd - p.navigationStart) });
				 } else {
				    CustomEvent.fire('page_timing', { name: 'SERV', ms: g_serverTime });
					CustomEvent.fire('page_timing', { name: 'REND', startTime: g_loadTime });
					CustomEvent.fire('page_timing_network', { name: 'NETW', loadTime: g_loadTime });
				 }CustomEvent.fire('page_timing_show', {
						isFixed: '', 
						show: '' 
					 });var o = {};
	      o.types = {};o.types['SECT'] = true;o.types['RLV2'] = true;o.types['UIOL'] = true;o.types['CSOL'] = true;
	
	      o.transaction_id = 'a4db44d63bdc3ed0ec71e4bf55e45ab4';
	      o.table_name = '';
	      o.form_name = 'auth_redirect';
	      o.view_id = 'Default view';
	      o.logged_in = false;
	      o.win = window;
	      CustomEvent.fire('page_timing_client', o);}
			 
            // The following line is used to set the time when we start requesting a new page
            Event.observe(window, 'beforeunload', function() {
				new CookieJar({sameSite: 'strict'}).put('g_startTime', new Date().getTime());
                CustomEvent.fireTop('request_start', document);
            });

            // simple pages fire this (stats.do, etc.)
            CustomEvent.observe('simple_page.unload', function() {
				new CookieJar({sameSite: 'strict'}).put('g_startTime', new Date().getTime());
            }); 

            // indicate we have completed the request (used by RequestManager.js for cancel widget)
            addLoadEvent(function() {
            	CustomEvent.fireTop("request_complete", window.location);
            });</script><script type="text/javascript" src="/scripts/doctype/z_last_include.jsx?v=08-07-2025_0908"></script></body><script type="text/html" id="popup_template"><div class="popup popup_form" style=""><iframe src="$src" style=""></iframe></div></script></html>